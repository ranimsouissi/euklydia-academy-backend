# app/services/llm_service.py
import json
from typing import Any, Dict, Optional, List

from openai import OpenAI
from app.core.config import settings

# ── Base system prompt (language-agnostic) ───────────────────────────────────
_SYSTEM_BASE = """You are a strategic AI transformation advisor writing executive-level reports.

Audience: senior executive.

Geographic context: North Africa (Tunisia, Morocco, Algeria, Egypt).
When generating examples, quick wins, key actions, and business context:
- Reference realities relevant to North African organizations: SME digitalization,
  public sector AI adoption, French/Arabic professional environments.
- Prioritize tools and approaches that are accessible and cost-effective for
  growing businesses in the region (avoid assuming enterprise-grade budgets).
- Avoid references specific to Gulf markets (UAE, Saudi Arabia) or Western
  enterprise contexts unless directly relevant to the skill being assessed.

Style rules:
- Use specific numbers from the input (scores/percentages) at least twice.
- Avoid generic consulting filler (e.g., "reduce measurable impact", "benchmark against industry standards").
- Do not repeat the same risk sentence across items.
- Be concise, analytical, decision-oriented.
- No marketing or motivational tone.

Return ONLY valid JSON. No extra text.
"""

# ── Language-specific instructions ──────────────────────────────────────────
_LANG_INSTRUCTIONS = {
    "fr": (
        "IMPORTANT: You MUST write the entire response in French. "
        "Every field in the JSON must be in French — executive_summary, "
        "strategic_risk_overview, why_it_matters, risk, business_leverage, "
        "quick_win, objective, key_actions, success_metrics, expected_impact. "
        "No English words except proper nouns, tool names, and skill names."
    ),
    "en": (
        "Write the entire response in English."
    ),
}


def _build_system_prompt(language: str = "en") -> str:
    lang = language.lower() if language else "en"
    lang_instr = _LANG_INSTRUCTIONS.get(lang, _LANG_INSTRUCTIONS["en"])
    return f"{_SYSTEM_BASE}\nLANGUAGE INSTRUCTION:\n{lang_instr}"


SCHEMA = {
    "executive_summary": "string",
    "strategic_risk_overview": "string",
    "capability_insights": [
        {
            "skill": "string",
            "why_it_matters": "string",
            "risk": "string",
            "business_leverage": "string",
            "quick_win": "string",
        }
    ],
    "roadmap": {
        "phase_1": {
            "focus": "string",
            "objective": "string",
            "key_actions": ["string"],
            "success_metrics": ["string"],
            "expected_impact": "string",
        },
        "phase_2": {
            "focus": "string",
            "objective": "string",
            "key_actions": ["string"],
            "success_metrics": ["string"],
            "expected_impact": "string",
        },
        "phase_3": {
            "focus": "string",
            "objective": "string",
            "key_actions": ["string"],
            "success_metrics": ["string"],
            "expected_impact": "string",
        },
    },
}

_client: Optional[OpenAI] = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is missing in settings/.env")
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


def _safe_json(text: str) -> Optional[Dict[str, Any]]:
    t = (text or "").strip()
    if t.startswith("```"):
        t = t.strip("`").strip()
        if t.lower().startswith("json"):
            t = t[4:].strip()
    try:
        return json.loads(t)
    except Exception:
        return None


def _compact_skill_rows(rows: List[Dict[str, Any]], limit: int = 4) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for r in (rows or [])[:limit]:
        out.append({
            "skill":         r.get("skill"),
            "score_percent": r.get("score_percent"),
            "priority":      r.get("priority"),
            "risk":          r.get("risk"),
        })
    return out


def generate_llm_narrative_v1(
    role: str,
    global_score: float,
    level: str,
    gaps: list,
    strengths: list,
    breakdown: list,
    roadmap_backend: list,
    language: str = "en",       # ← nouveau paramètre
) -> Dict[str, Any]:

    gaps_c      = _compact_skill_rows(gaps, limit=2)
    strengths_c = _compact_skill_rows(strengths, limit=2)
    breakdown_c = _compact_skill_rows(breakdown, limit=4)

    roadmap_skeleton = []
    for p in (roadmap_backend or [])[:3]:
        roadmap_skeleton.append({
            "phase":           p.get("phase"),
            "focus_skill":     p.get("focus_skill"),
            "objective":       p.get("objective"),
            "expected_impact": p.get("expected_impact"),
        })

    lang = language.lower() if language else "en"
    lang_label = "French" if lang == "fr" else "English"

    prompt = f"""
INPUT DATA (do not invent anything not supported by this data):

Role: {role}
Global Score: {global_score}%
Maturity Level: {level}
Output Language: {lang_label}

Top Gaps (highest priority):
{json.dumps(gaps_c, ensure_ascii=False)}

Top Strengths:
{json.dumps(strengths_c, ensure_ascii=False)}

Top Capability Breakdown (top 4 by priority):
{json.dumps(breakdown_c, ensure_ascii=False)}

Backend Roadmap Skeleton:
{json.dumps(roadmap_skeleton, ensure_ascii=False)}

TASKS:
1) executive_summary: 2-4 sentences.
   - Must mention: global score ({global_score}%) and maturity ({level})
   - Mention at least one gap skill by name with its score

2) strategic_risk_overview: 2-3 sentences
   - Must reference BOTH gap skills by name
   - Must include at least ONE number from the input (gap score_percent or priority)
   - Must express business exposure in terms of cost, speed, quality, or ROI visibility
   - Avoid generic phrases; be specific to the role

3) capability_insights: EXACTLY 2 items (one per top gap)
   For each item:
   - skill: gap skill name (keep original name, do not translate skill names)
   - why_it_matters: role-specific (1 sentence)
   - risk: rewrite using provided risk; must be distinct
   - business_leverage: 1 sentence on ROI / productivity / decision speed
   - quick_win: concrete action to start within 2 weeks (max 12 words)

4) roadmap: 3 phases (0-30, 30-60, 60-90 days)
   - Use the backend phase focus_skill as "focus" (keep original skill name)
   - Each phase:
     * objective: 1 sentence (max 18 words)
     * key_actions: EXACTLY 3 bullets, each <= 10 words, starts with a verb
     * success_metrics: EXACTLY 2 bullets, measurable (%, time, count)
     * expected_impact: 1 sentence (max 18 words)

MATURITY ADAPTATION:
- Emerging: fundamentals & adoption
- Developing: structured skill-building & tool enablement
- Advanced: scaling, governance, KPIs
- Strategic: optimization, portfolio ROI, operating model

STRICT RULES:
- Write ALL text fields in {lang_label}. Skill names and tool names keep their original form.
- No filler phrases like "benchmark against industry standards".
- Use at least two specific numbers (scores/priority) from the input.
- Return ONLY valid JSON matching the structure below exactly.

OUTPUT JSON SCHEMA:
{json.dumps(SCHEMA, ensure_ascii=False)}
""".strip()

    system_prompt = _build_system_prompt(lang)

    client = _get_client()
    resp = client.chat.completions.create(
        model=settings.OPENAI_MODEL_REPORT,
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": prompt},
        ],
    )
    parsed = _safe_json(resp.choices[0].message.content or "")
    if not parsed:
        return {
            "executive_summary":       None,
            "strategic_risk_overview": None,
            "capability_insights":     None,
            "roadmap":                 None,
            "_raw": (resp.choices[0].message.content or "")[:2000],
        }

    return parsed