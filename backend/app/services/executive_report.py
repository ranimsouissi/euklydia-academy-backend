# app/services/executive_report.py
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import timedelta

from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.assessment_session import AssessmentSession
from app.models.skill import Skill
from app.models.user import User
from app.models.user_skill_score import UserSkillScore
from app.services.llm_service import generate_llm_narrative_v1

# =========================
# Config
# =========================
MAX_SCORE = 100.0


def round1(x: float) -> float:
    return float(f"{x:.1f}")


def percent_to_5(p: float) -> float:
    p = max(0.0, min(100.0, float(p)))
    return (p / 100.0) * 5.0


# =========================
# Name extraction (Google OAuth safe)
# =========================

def _extract_display_name(user) -> str:
    first = (getattr(user, "first_name", None) or "").strip()
    last  = (getattr(user, "last_name",  None) or "").strip()
    if first or last:
        return f"{first} {last}".strip().title()

    email_prefix = user.email.split("@")[0].lower()

    full = (getattr(user, "full_name", None) or "").strip()
    if full and full.lower() != email_prefix:
        return full.title()

    username = (getattr(user, "username", None) or "").strip()
    if username and username.lower() != email_prefix:
        return username.title()

    clean = re.sub(r'\d+$', '', email_prefix)
    clean = re.sub(r'[._\-]+', ' ', clean).strip()
    clean = re.sub(r'([a-z])([A-Z])', r'\1 \2', clean)
    clean = clean.title()
    return clean if clean else email_prefix


# =========================
# Maturity
# =========================

def maturity_level(score_percent: float) -> str:
    if score_percent < 40.0:
        return "Emerging"
    elif score_percent < 60.0:
        return "Developing"
    elif score_percent < 80.0:
        return "Advanced"
    else:
        return "Strategic"


def maturity_description(level: str) -> str:
    mapping = {
        "Emerging":   "AI usage is minimal and mostly experimental.",
        "Developing":  "AI capabilities are emerging but not yet consistently integrated into workflows.",
        "Advanced":   "AI is integrated into workflows and supports operational decisions.",
        "Strategic":  "AI is used strategically with strong governance and measurable business impact.",
    }
    return mapping.get(level or "", "")


# =========================
# Business risk mapping
# =========================
RISK_RULES: Dict[str, str] = {
    # Generic
    "AI Literacy":             "Limited understanding of AI capabilities reduces team confidence and slows adoption.",
    "Generative AI Basics":    "Underuse of generative AI for content and document drafting lowers productivity.",
    "AI Prompting":            "Poorly structured prompts produce low-quality outputs, increasing review time.",
    "AI Output Evaluation":    "Risk of deploying inaccurate AI outputs without sufficient human review.",
    "Responsible AI Use":      "Exposure to privacy, bias, and governance risks without ethical guardrails.",
    "AI Workflow Integration": "Lower productivity gains when AI tools are not embedded in daily workflows.",

    # AI Sales Specialist
    "Prospection AI":               "Inconsistent lead pipeline quality without AI-assisted prospecting.",
    "Prospection IA":               "Inconsistent lead pipeline quality without AI-assisted prospecting.",
    "CRM et Scoring de Leads":      "Lower lead conversion and manual CRM overhead without AI scoring.",
    "Communication et Emails AI":   "Slower response cycles and inconsistent messaging without AI-assisted email.",
    "Analyse des Donnees Ventes":   "Missed upsell signals when sales data is not analyzed with AI-powered tools.",
    "Analyse des Données Ventes":   "Missed upsell signals when sales data is not analyzed with AI-powered tools.",
    "Ethique AI dans la Vente":     "Reputational and compliance risks from ungoverned AI use in client interactions.",
    "Ethique IA dans la Vente":     "Reputational and compliance risks from ungoverned AI use in client interactions.",

    # AI Marketing Strategist
    "Creation de Contenu AI":       "Lower content output and inconsistent brand voice without AI generation.",
    "Création de Contenu AI":       "Lower content output and inconsistent brand voice without AI generation.",
    "Publicite et Ciblage AI":      "Higher ad spend and lower ROAS without AI-optimized targeting.",
    "Publicité et Ciblage AI":      "Higher ad spend and lower ROAS without AI-optimized targeting.",
    "SEO et Analytics AI":          "Reduced organic visibility without AI-powered SEO and analytics.",
    "Automatisation Marketing AI":  "Manual campaign overhead and missed personalization opportunities.",
    "Ethique et Donnees Marketing AI":  "Regulatory risks from non-compliant data practices in AI-driven marketing.",
    "Éthique et Données Marketing AI":  "Regulatory risks from non-compliant data practices in AI-driven marketing.",

    # AI Designer
    "Generation d'images AI":              "Slower visual production and culturally misaligned creatives for North Africa.",
    "Génération d'images AI":              "Slower visual production and culturally misaligned creatives for North Africa.",
    "Design UI/UX avec AI":                "Reduced UX quality and slower iteration without AI-assisted prototyping.",
    "Creation video et animation AI":      "Missed video content opportunities at scale without AI tools.",
    "Création vidéo et animation AI":      "Missed video content opportunities at scale without AI tools.",
    "Brand Assets avec AI":                "Inconsistent brand identity and higher costs without AI-generated assets.",
    "Ethique et propriete intellectuelle AI":  "Legal exposure from unlicensed or misused AI-generated content.",
    "Éthique et propriété intellectuelle AI":  "Legal exposure from unlicensed or misused AI-generated content.",

    # AI Project Manager
    "Planification de Projet AI":       "Slower project kickoff and manual planning overhead without AI.",
    "Planification de Projet IA":       "Slower project kickoff and manual planning overhead without AI.",
    "Gestion des Risques AI":           "Undetected risks and reactive mitigation without AI monitoring.",
    "Gestion des Risques IA":           "Undetected risks and reactive mitigation without AI monitoring.",
    "Collaboration et Communication AI": "Coordination gaps in distributed North Africa project teams.",
    "Collaboration et Communication IA": "Coordination gaps in distributed North Africa project teams.",
    "Automatisation des Workflows AI":  "Repetitive manual tasks persist without AI workflow automation.",
    "Automatisation des Workflows IA":  "Repetitive manual tasks persist without AI workflow automation.",
    "Reporting et Tableaux de Bord AI": "Limited executive visibility without AI-powered dashboards.",
    "Reporting et Tableaux de Bord IA": "Limited executive visibility without AI-powered dashboards.",
}


def infer_business_risk(skill_name: str) -> str:
    if skill_name in RISK_RULES:
        return RISK_RULES[skill_name]
    skill_lower = skill_name.lower().strip()
    for key, risk in RISK_RULES.items():
        if key.lower().strip() == skill_lower:
            return risk
    keywords_map = {
        "prospect":   "Inconsistent lead pipeline quality without AI-assisted prospecting.",
        "crm":        "Lower lead conversion and manual CRM overhead without AI scoring.",
        "email":      "Slower response cycles without AI-assisted email workflows.",
        "ethique":    "Compliance and reputational risks from ungoverned AI usage.",
        "image":      "Slower visual production and culturally misaligned creatives.",
        "design":     "Reduced UX quality and slower design iteration.",
        "video":      "Missed content engagement opportunities at scale.",
        "brand":      "Inconsistent brand identity and higher creative production costs.",
        "contenu":    "Lower content output and inconsistent brand voice.",
        "content":    "Lower content output and inconsistent brand voice.",
        "seo":        "Reduced organic visibility and slower data-driven decisions.",
        "analytic":   "Delayed insights and missed optimization opportunities.",
        "publicite":  "Higher ad spend and lower ROAS without AI targeting.",
        "planif":     "Slower project kickoff and manual planning overhead.",
        "risque":     "Undetected risks and reactive mitigation without AI monitoring.",
        "workflow":   "Manual task overhead and reduced team velocity.",
        "reporting":  "Limited executive visibility and slower decisions.",
        "collaborat": "Coordination gaps and communication delays in distributed teams.",
        "prompt":     "Low-quality AI outputs from unstructured prompts.",
    }
    for kw, risk in keywords_map.items():
        if kw in skill_lower:
            return risk
    return "Slower AI adoption and reduced operational value without targeted capability development."


# =========================
# Weights by role
# =========================
ROLE_WEIGHTS: Dict[str, Dict[str, float]] = {}


def get_weight(role_name: str, skill_name: str) -> float:
    return float(ROLE_WEIGHTS.get(role_name, {}).get(skill_name, 1.0))


# =========================
# Core models
# =========================
@dataclass
class SkillScore:
    skill_id: int
    skill_name: str
    score_percent: float


# =========================
# Scoring
# =========================

def compute_global_score(skill_scores: List[SkillScore], role_name: str) -> float:
    if not skill_scores:
        return 0.0
    weighted_sum = weight_total = 0.0
    for s in skill_scores:
        w = get_weight(role_name, s.skill_name)
        weighted_sum += s.score_percent * w
        weight_total += w
    return weighted_sum / max(weight_total, 1e-9)


def compute_priorities(skill_scores: List[SkillScore], role_name: str) -> List[Dict[str, Any]]:
    rows = []
    for s in skill_scores:
        w = get_weight(role_name, s.skill_name)
        rows.append({
            "skill_id":      s.skill_id,
            "skill":         s.skill_name,
            "score_percent": float(s.score_percent),
            "score_5":       percent_to_5(s.score_percent),
            "weight":        w,
            "priority":      float((MAX_SCORE - s.score_percent) * w),
            "risk":          infer_business_risk(s.skill_name),
        })
    rows.sort(key=lambda r: r["priority"], reverse=True)
    return rows


# =========================
# Roadmap
# =========================

def build_90_day_roadmap(priority_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not priority_rows:
        return []
    top1 = priority_rows[0]
    top2 = priority_rows[1] if len(priority_rows) > 1 else None
    top3 = priority_rows[2] if len(priority_rows) > 2 else None

    phases = [{
        "phase":           "Phase 1 (0-30 days)",
        "focus_skill":     top1["skill"],
        "objective":       "Close the highest-impact capability gap quickly",
        "expected_impact": "Immediate uplift on the most constrained capability",
        "recommended_modules": [],
    }]
    if top2:
        phases.append({
            "phase":           "Phase 2 (30-60 days)",
            "focus_skill":     top2["skill"],
            "objective":       "Increase operational leverage and repeatability",
            "expected_impact": "More predictable execution and measurable gains",
            "recommended_modules": [],
        })
    phases.append({
        "phase":           "Phase 3 (60-90 days)",
        "focus_skill":     top3["skill"] if top3 else "Measurement & Governance",
        "objective":       "Consolidate improvements and operationalize measurement",
        "expected_impact": "Sustained adoption and executive ROI visibility",
        "recommended_modules": [],
    })
    return phases


def build_radar_chart(priority_rows, top_n=4):
    n   = max(3, int(top_n))
    top = priority_rows[:n]
    return [{"label": r["skill"], "value": round1(r["score_percent"])} for r in top]


def build_learning_recommendations(strategic_gaps_rows):
    recs = []
    for i, r in enumerate(strategic_gaps_rows[:3]):
        recs.append({
            "title":          f"Module - {r['skill']}",
            "focus_skill":    r["skill"],
            "priority":       "High" if i == 0 else "Medium",
            "format":         "Micro-learning + Exercise + Deliverable",
            "estimated_time": "45-60 min",
            "why_this":       "Directly addresses the highest-priority capability gap.",
        })
    return recs


# =========================
# Public API
# =========================
def _select_insights_gaps(priority_rows, max_insights=2):
    HIGH_THRESHOLD = 50.0
    high_gaps   = [r for r in priority_rows if r["priority"] > HIGH_THRESHOLD]
    medium_gaps = [r for r in priority_rows if r["priority"] <= HIGH_THRESHOLD
                   and r["priority"] > 25.0]
    high_gaps   = sorted(high_gaps,   key=lambda r: (-r["priority"], r["skill_id"]))
    medium_gaps = sorted(medium_gaps, key=lambda r: (-r["priority"], r["skill_id"]))
    selected = high_gaps[:max_insights]
    if len(selected) < max_insights:
        selected += medium_gaps[:max_insights - len(selected)]
    return selected


def generate_executive_report_payload(db: Session, user_id: int, language: str = "en") -> Dict[str, Any]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    if not user.career_path_id:
        raise ValueError("User has no career_path_id")

    role_name = (
        (user.career_path.name if user.career_path else None)
        or (user.role.name if user.role else None)
        or "Unknown Role"
    )

    last_session = db.execute(
        select(AssessmentSession)
        .where(AssessmentSession.user_id == user_id)
        .where(AssessmentSession.career_path_id == user.career_path_id)
        .order_by(desc(AssessmentSession.created_at))
        .limit(1)
    ).scalar_one_or_none()

    if not last_session:
        raise ValueError("No assessment session found for this user")

    next_review = last_session.created_at + timedelta(days=90)

    score_rows = (
        db.query(UserSkillScore, Skill)
        .join(Skill, Skill.id == UserSkillScore.skill_id)
        .filter(UserSkillScore.assessment_session_id == last_session.id)
        .all()
    )

    skill_scores: List[SkillScore] = [
        SkillScore(skill_id=sk.id, skill_name=sk.name, score_percent=float(uss.score))
        for (uss, sk) in score_rows
    ]

    global_percent    = compute_global_score(skill_scores, role_name)
    level             = maturity_level(global_percent)
    level_desc        = maturity_description(level)
    priority_rows     = compute_priorities(skill_scores, role_name)

    strategic_gaps_rows = _select_insights_gaps(priority_rows, max_insights=2)
    strategic_gaps      = [r["skill"] for r in strategic_gaps_rows]

    strength_candidates = sorted(priority_rows, key=lambda r: r["score_percent"], reverse=True)
    strengths_rows: List[Dict[str, Any]] = []
    for r in strength_candidates:
        if r["skill"] not in strategic_gaps:
            strengths_rows.append(r)
        if len(strengths_rows) == 2:
            break
    if not strengths_rows:
        strengths_rows = strength_candidates[:2]
    strengths = [r["skill"] for r in strengths_rows]

    roadmap       = build_90_day_roadmap(priority_rows)
    radar_data    = build_radar_chart(priority_rows, top_n=5)
    learning_recs = build_learning_recommendations(strategic_gaps_rows)

    _full_name = _extract_display_name(user)

    payload: Dict[str, Any] = {
        "language": language,
        "leader": {
            "id":             user.id,
            "name":           _full_name,
            "full_name":      _full_name,
            "email":          user.email,
            "role":           role_name,
            "maturity_level": level,
        },
        "maturity_level_description": level_desc,
        "assessment": {
            "global_score_percent": round1(global_percent),
            "maturity_level":       level,
            "skill_breakdown": [
                {
                    "skill":         r["skill"],
                    "score_percent": round1(r["score_percent"]),
                    "risk":          r["risk"],
                    "priority":      round1(r["priority"]),
                }
                for r in priority_rows
            ],
            "strategic_gaps": strategic_gaps,
            "strengths":       strengths,
        },
        "roadmap_90_days":          roadmap,
        "radar_chart":              radar_data,
        "learning_recommendations": learning_recs,
        "meta": {
            "scale":                       "0..100",
            "version":                     "type_a_v1",
            "career_path_id":              user.career_path_id,
            "assessment_session_id":       last_session.id,
            "assessment_created_at":       last_session.created_at.isoformat(),
            "next_assessment_recommended": next_review.isoformat(),
        },
    }

    print("USE_LLM_REPORT:", settings.USE_LLM_REPORT)

    if settings.USE_LLM_REPORT:
        payload["llm_narrative"] = generate_llm_narrative_v1(
            role=role_name,
            global_score=round1(global_percent),
            level=level,
            gaps=strategic_gaps_rows,
            strengths=strengths_rows,
            breakdown=priority_rows[:4],
            roadmap_backend=roadmap,
            language=payload.get("language", "en"),
        )

    print("LLM NARRATIVE:", payload.get("llm_narrative"))
    import json
    print("ROADMAP_90_DAYS =", json.dumps(payload["roadmap_90_days"], indent=2, ensure_ascii=False))

    return payload