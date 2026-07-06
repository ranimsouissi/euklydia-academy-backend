# app/services/sequencing_service.py
"""
Dynamic Content Sequencing Service
====================================
Recommande le module suivant basé sur :
- La mastery actuelle de l'apprenant par skill
- Les prérequis (niveau Fondation → Pratique → Expert)
- Le rôle de l'apprenant
- Les modules déjà complétés
- Le KPI before/after soumis
- L'Execution Task soumise
- Le temps disponible par semaine

Fallback : règle simple sans LLM si erreur OpenAI.
"""
import json
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from openai import OpenAI
from app.core.config import settings


def _get_client() -> OpenAI:
    return OpenAI(api_key=settings.OPENAI_API_KEY)


def get_learner_roadmap(db: Session, user_id: int) -> dict:
    """
    Récupère le roadmap complet de l'apprenant :
    - Tous les modules de son rôle
    - Mastery par skill
    - Modules complétés / en cours
    - KPI before/after + Execution Task
    - Temps disponible par semaine
    """
    rows = db.execute(text(
        "SELECT m.id, m.title_fr, m.level, m.display_order, m.role, "
        "m.kpi_before_fr AS kpi_before, "
        "ms.skill_id, s.name AS skill_name, "
        "lsm.mastery_score, lsm.mastery_level, "
        "ump.status            AS module_status, "
        "ump.progress_percent, "
        "ump.kpi_after, "
        "ump.execution_task_submitted, "
        "ump.execution_task_difficulty "
        "FROM modules m "
        "JOIN module_skills ms ON ms.module_id = m.id "
        "JOIN skills s ON s.id = ms.skill_id "
        "LEFT JOIN learner_skill_mastery lsm "
        "  ON lsm.skill_id = s.id AND lsm.user_id = :uid "
        "LEFT JOIN user_module_progress ump "
        "  ON ump.module_id = m.id AND ump.user_id = :uid "
        "WHERE m.is_active = true "
        "ORDER BY m.role, m.display_order"
    ), {"uid": user_id}).fetchall()

    modules = [dict(r._mapping) for r in rows]

    # ── Temps disponible par semaine — profil apprenant ──────
    profile_row = db.execute(text(
        "SELECT time_available_per_week "
        "FROM user_profiles "
        "WHERE user_id = :uid"
    ), {"uid": user_id}).fetchone()

    time_available = (
        int(profile_row.time_available_per_week)
        if profile_row and profile_row.time_available_per_week
        else None
    )

    return {
        "modules":                 modules,
        "user_id":                 user_id,
        "time_available_per_week": time_available
    }


def get_next_module_rule_based(
    roadmap:           dict,
    current_module_id: int
) -> Optional[dict]:
    """
    Fallback sans LLM — règles simples :
    1. Execution Task non soumise → soumettre d'abord
    2. KPI absent ou difficulté élevée → revoir Execution Content
    3. Mastery insuffisante → retry
    4. Module suivant dans le même rôle
    5. Skill le plus faible
    """
    modules = roadmap["modules"]
    current = next(
        (m for m in modules if m["id"] == current_module_id), None
    )
    if not current:
        return None

    current_mastery  = float(current.get("mastery_score") or 0)
    kpi_after        = current.get("kpi_after")
    task_submitted   = current.get("execution_task_submitted", False)
    difficulty       = current.get("execution_task_difficulty")

    # Règle 1 : Execution Task non soumise → soumettre d'abord
    if not task_submitted:
        return {
            "module_id":       current_module_id,
            "module_title":    current["title_fr"],
            "reason":          "Soumettez votre Execution Task avant de passer au module suivant.",
            "action":          "submit_execution_task",
            "section_to_review": "execution_task"
        }

    # Règle 2 : KPI absent ou difficulté élevée → revoir Execution Content
    if not kpi_after or (
        difficulty and difficulty.lower() in
        ("élevée", "haute", "difficile", "high", "hard")
    ):
        return {
            "module_id":         current_module_id,
            "module_title":      current["title_fr"],
            "reason":            "Difficulté déclarée ou KPI non mesuré — revoir l'Execution Content avant de continuer.",
            "action":            "review_section",
            "section_to_review": "execution_content"
        }

    # Règle 3 : mastery insuffisante → retry
    if current_mastery < 0.5:
        return {
            "module_id":         current_module_id,
            "module_title":      current["title_fr"],
            "reason":            f"Mastery de {round(current_mastery*100)}% insuffisante — consolidez ce module.",
            "action":            "retry_current",
            "section_to_review": "execution_content"
        }

    # Règle 4 : module suivant dans le même rôle
    same_role = sorted(
        [m for m in modules if m["role"] == current["role"]],
        key=lambda x: x["display_order"]
    )
    current_idx = next(
        (i for i, m in enumerate(same_role)
         if m["id"] == current_module_id), -1
    )

    if 0 <= current_idx < len(same_role) - 1:
        next_mod = same_role[current_idx + 1]
        return {
            "module_id":         next_mod["id"],
            "module_title":      next_mod["title_fr"],
            "reason":            f"Mastery suffisante ({round(current_mastery*100)}%) — passez au module suivant.",
            "action":            "next_module",
            "section_to_review": None
        }

    # Règle 5 : skill le plus faible
    weak = sorted(
        [m for m in modules if m.get("mastery_score") is not None],
        key=lambda x: float(x.get("mastery_score") or 0)
    )
    if weak:
        return {
            "module_id":         weak[0]["id"],
            "module_title":      weak[0]["title_fr"],
            "reason":            f"Renforcez votre compétence la plus faible : {weak[0]['skill_name']}.",
            "action":            "strengthen_weak",
            "section_to_review": None
        }

    return None


def generate_next_recommendation(
    db:                Session,
    user_id:           int,
    current_module_id: int
) -> dict:
    """
    Génère une recommandation intelligente du module suivant.
    Utilise le LLM si disponible, sinon fallback règle simple.
    """
    roadmap = get_learner_roadmap(db, user_id)
    modules = roadmap["modules"]

    if not modules:
        return {
            "recommendation": None,
            "reason":         "Aucun module disponible",
            "source":         "none"
        }

    current = next(
        (m for m in modules if m["id"] == current_module_id), None
    )

    mastery_summary = [
        f"- {m['title_fr']} ({m['level']}) : "
        f"mastery={round(float(m.get('mastery_score') or 0)*100)}%, "
        f"status={m.get('module_status') or 'not_started'}, "
        f"execution_task={m.get('execution_task_submitted', False)}, "
        f"kpi_after={m.get('kpi_after') or 'non renseigné'}"
        for m in modules
    ]

    try:
        client = _get_client()
        prompt = (
            "Tu es un conseiller pédagogique expert pour Euklydia.\n\n"
            f"Module venant d'être complété : "
            f"{current['title_fr'] if current else 'inconnu'}\n"
            f"Execution Task soumise : "
            f"{current.get('execution_task_submitted', False) if current else False}\n"
            f"KPI before : "
            f"{current.get('kpi_before', 'non renseigné') if current else 'non renseigné'}\n"
            f"KPI after  : "
            f"{current.get('kpi_after', 'non renseigné') if current else 'non renseigné'}\n"
            f"Difficulté déclarée : "
            f"{current.get('execution_task_difficulty', 'aucune') if current else 'aucune'}\n"
            f"Temps disponible/semaine : "
            f"{roadmap.get('time_available_per_week', 'non renseigné')} h\n\n"
            "ÉTAT ACTUEL DES COMPÉTENCES :\n"
            + "\n".join(mastery_summary) + "\n\n"
            "Recommande le prochain module OU la section à revoir.\n"
            "Réponds UNIQUEMENT avec ce JSON :\n"
            "{\n"
            '  "module_id": <id>,\n'
            '  "module_title": "<titre>",\n'
            '  "reason": "<Parce que... — 1-2 phrases>",\n'
            '  "action": "next_module|retry_current|strengthen_weak'
            '|review_section|submit_execution_task",\n'
            '  "section_to_review": '
            '"<use_case|kpi|execution_content|execution_task|kpi_measurement|null>"\n'
            "}"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=300
        )

        raw = (response.choices[0].message.content or "").strip()
        if raw.startswith("```"):
            raw = raw.strip("`").strip()
            if raw.lower().startswith("json"):
                raw = raw[4:].strip()

        recommendation = json.loads(raw)

        # ── Score de confiance ──────────────────────────────
        mastery_score = float(current.get("mastery_score") or 0) if current else 0
        kpi_after     = current.get("kpi_after") if current else None

        if mastery_score >= 0.6 and kpi_after:
            confidence = "high"
        elif mastery_score >= 0.3 or kpi_after:
            confidence = "medium"
        else:
            confidence = "low"

        recommendation["source"]     = "llm"
        recommendation["confidence"] = confidence
        return recommendation

    except Exception:
        fallback = get_next_module_rule_based(roadmap, current_module_id)
        if fallback:
            fallback["source"]     = "rule_based"
            fallback["confidence"] = "low"
            return fallback
        return {
            "recommendation": None,
            "reason":         "Aucune recommandation disponible",
            "source":         "none",
            "confidence":     "low"
        }