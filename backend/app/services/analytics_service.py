# app/services/analytics_service.py
"""
Learning Analytics — Content Effectiveness Scoring Agent
=========================================================
Analyse l'efficacité du contenu des modules pour l'équipe Euklydia (admin).

Métriques calculées :
  1. KPI improvement rate par module
     → % apprenants qui améliorent leur kpi_after vs kpi_before
  2. Time-to-mastery par skill
     → section_opened_at["use_case"] → execution_task_submitted_at
  3. Section drop-off detection
     → quelle section du module bloque le plus d'apprenants
  4. Flagging automatique des modules peu performants
     → KPI after insuffisant + drop-off élevé + difficulté déclarée
  5. Recommandations d'amélioration de contenu basées sur les preuves

Sources de données :
  - user_module_progress  → section_progress, section_opened_at,
                            execution_task_submitted_at, kpi_after,
                            execution_task_difficulty
  - modules               → kpi_before_fr, kpi_after_fr, title_fr
  - learner_skill_mastery → kpi_improvement_rate par skill
"""
import json
from datetime import datetime
from typing import Optional
from openai import OpenAI
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings

_client: Optional[OpenAI] = None

def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY manquant dans .env")
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


# ────────────────────────────────────────────────────────────────
# STEP 1 — KPI improvement rate par module
# ────────────────────────────────────────────────────────────────
def get_kpi_improvement_data(db: Session, module_id: int) -> dict:
    """
    Calcule le KPI improvement rate pour un module donné.
    Un learner "améliore" son KPI si kpi_after est renseigné
    (on ne peut pas comparer textuellement — on délègue au LLM).
    """
    rows = db.execute(text("""
        SELECT
            ump.user_id,
            ump.kpi_after,
            ump.execution_task_submitted,
            ump.execution_task_difficulty,
            m.kpi_before_fr,
            m.kpi_after_fr   AS kpi_target,
            m.title_fr       AS module_title
        FROM user_module_progress ump
        JOIN modules m ON m.id = ump.module_id
        WHERE ump.module_id = :module_id
    """), {"module_id": module_id}).fetchall()

    total = len(rows)
    submitted = sum(1 for r in rows if r.execution_task_submitted)
    with_kpi_after = sum(1 for r in rows if r.kpi_after)

    difficulties = {}
    for r in rows:
        if r.execution_task_difficulty:
            d = r.execution_task_difficulty
            difficulties[d] = difficulties.get(d, 0) + 1

    return {
        "module_id": module_id,
        "module_title": rows[0].module_title if rows else None,
        "kpi_before_reference": rows[0].kpi_before_fr if rows else None,
        "kpi_target": rows[0].kpi_target if rows else None,
        "total_learners": total,
        "execution_task_submitted": submitted,
        "execution_task_completion_rate": round(submitted / total, 2) if total else 0,
        "learners_with_kpi_after": with_kpi_after,
        "kpi_measurement_rate": round(with_kpi_after / total, 2) if total else 0,
        "difficulty_distribution": difficulties,
        "kpi_after_samples": [
            {"user_id": r.user_id, "kpi_after": r.kpi_after}
            for r in rows if r.kpi_after
        ][:10],
    }


# ────────────────────────────────────────────────────────────────
# STEP 2 — Time-to-mastery par module
# ────────────────────────────────────────────────────────────────
def get_time_to_mastery_data(db: Session, module_id: int) -> dict:
    """
    Calcule le temps entre l'ouverture de la première section
    et la soumission de l'Execution Task.
    """
    rows = db.execute(text("""
        SELECT
            ump.user_id,
            ump.section_opened_at,
            ump.execution_task_submitted_at,
            ump.execution_task_submitted
        FROM user_module_progress ump
        WHERE ump.module_id = :module_id
          AND ump.section_opened_at IS NOT NULL
          AND ump.execution_task_submitted_at IS NOT NULL
    """), {"module_id": module_id}).fetchall()

    durations_minutes = []
    for r in rows:
        try:
            opened = r.section_opened_at
            # section_opened_at est un dict JSON — on prend use_case ou la première section
            if isinstance(opened, dict):
                first_key = next(iter(opened), None)
                if first_key:
                    first_ts = datetime.fromisoformat(opened[first_key])
                    submitted_ts = r.execution_task_submitted_at
                    if submitted_ts:
                        delta = submitted_ts - first_ts
                        minutes = delta.total_seconds() / 60
                        if minutes > 0:
                            durations_minutes.append(round(minutes, 1))
        except Exception:
            continue

    if durations_minutes:
        avg = round(sum(durations_minutes) / len(durations_minutes), 1)
        min_time = min(durations_minutes)
        max_time = max(durations_minutes)
    else:
        avg = min_time = max_time = None

    return {
        "module_id": module_id,
        "learners_with_full_data": len(durations_minutes),
        "avg_time_to_mastery_minutes": avg,
        "min_time_minutes": min_time,
        "max_time_minutes": max_time,
        "durations": durations_minutes,
    }


# ────────────────────────────────────────────────────────────────
# STEP 3 — Section drop-off detection
# ────────────────────────────────────────────────────────────────
def get_dropoff_data(db: Session, module_id: int) -> dict:
    """
    Analyse section_progress pour détecter où les apprenants s'arrêtent.
    Drop-off = section "not_started" alors que les sections précédentes
    sont "completed" ou "in_progress".
    """
    rows = db.execute(text("""
        SELECT
            ump.user_id,
            ump.section_progress,
            ump.status
        FROM user_module_progress ump
        WHERE ump.module_id = :module_id
          AND ump.section_progress IS NOT NULL
    """), {"module_id": module_id}).fetchall()

    SECTION_ORDER = [
        "use_case", "kpi", "execution_content",
        "execution_task", "kpi_measurement", "progress_update"
    ]

    section_counts = {s: {"completed": 0, "in_progress": 0, "not_started": 0}
                      for s in SECTION_ORDER}
    drop_off_at = {}

    for r in rows:
        sp = r.section_progress or {}
        # Trouver la première section not_started après une section active
        found_drop = False
        for i, section in enumerate(SECTION_ORDER):
            status = sp.get(section, "not_started")
            section_counts[section][status] += 1
            if not found_drop and status == "not_started" and i > 0:
                prev = sp.get(SECTION_ORDER[i - 1], "not_started")
                if prev in ("completed", "in_progress"):
                    drop_off_at[section] = drop_off_at.get(section, 0) + 1
                    found_drop = True

    total = len(rows)
    completion_by_section = {
        s: round(section_counts[s]["completed"] / total, 2) if total else 0
        for s in SECTION_ORDER
    }

    main_drop_off = max(drop_off_at, key=drop_off_at.get) if drop_off_at else None

    return {
        "module_id": module_id,
        "total_learners": total,
        "completion_by_section": completion_by_section,
        "drop_off_counts": drop_off_at,
        "main_drop_off_section": main_drop_off,
        "main_drop_off_rate": round(
            drop_off_at.get(main_drop_off, 0) / total, 2
        ) if main_drop_off and total else 0,
    }


# ────────────────────────────────────────────────────────────────
# STEP 4 — LLM : scoring + recommandations
# ────────────────────────────────────────────────────────────────
def generate_effectiveness_score(
    db: Session,
    module_id: int,
    kpi_data: dict,
    mastery_data: dict,
    dropoff_data: dict,
) -> dict:
    """
    Génère un score d'efficacité et des recommandations d'amélioration
    basées sur les 3 métriques combinées.
    """
    client = _get_client()

    prompt = f"""Tu es un analyste pédagogique expert pour la plateforme Euklydia Academy.
Analyse l'efficacité du contenu du module {module_id} pour l'équipe Euklydia (usage admin interne).

--- KPI IMPROVEMENT DATA ---
{json.dumps(kpi_data, ensure_ascii=False, default=str)}

--- TIME-TO-MASTERY DATA ---
{json.dumps(mastery_data, ensure_ascii=False, default=str)}

--- SECTION DROP-OFF DATA ---
{json.dumps(dropoff_data, ensure_ascii=False, default=str)}

Génère EXACTEMENT ce JSON (sans texte autour) :
{{
  "module_id": {module_id},
  "effectiveness_score": 0 à 100,
  "performance_flag": "good|needs_improvement|critical",
  "summary": "résumé exécutif en 2 phrases pour l'équipe Euklydia",
  "kpi_analysis": {{
    "completion_rate": 0.0 à 1.0,
    "kpi_measurement_rate": 0.0 à 1.0,
    "assessment": "bon|insuffisant|critique",
    "evidence": "preuve concrète basée sur les données"
  }},
  "time_to_mastery_analysis": {{
    "avg_minutes": nombre ou null,
    "assessment": "rapide|normal|lent|pas_de_données",
    "evidence": "preuve concrète"
  }},
  "drop_off_analysis": {{
    "main_drop_off_section": "section ou null",
    "drop_off_rate": 0.0 à 1.0,
    "assessment": "faible|modéré|élevé",
    "evidence": "preuve concrète"
  }},
  "recommendations": [
    {{
      "priority": "high|medium|low",
      "section": "section concernée",
      "type": "simplify_content|add_examples|add_checkpoint|redesign_task|improve_kpi_measurement",
      "action": "action concrète à prendre",
      "evidence": "données qui justifient cette recommandation"
    }}
  ],
  "flags": []
}}

Règles :
- effectiveness_score : 0-100 basé sur completion_rate + kpi_measurement_rate + drop_off
- performance_flag "critical" si score < 40, "needs_improvement" si 40-70, "good" si > 70
- recommendations : 1 à 3 items MAX, triées par priorité
- flags : liste de string pour signaler des anomalies (ex: "pas_de_données_kpi", "drop_off_élevé")
- Réponds UNIQUEMENT avec le JSON valide"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1000
    )
    raw = (response.choices[0].message.content or "").strip()
    if raw.startswith("```"):
        raw = raw.strip("`").strip()
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()
    try:
        return json.loads(raw)
    except Exception:
        return {"error": "Parsing failed", "_raw": raw[:500]}


# ────────────────────────────────────────────────────────────────
# MAIN — Point d'entrée : analyse complète d'un module
# ────────────────────────────────────────────────────────────────
def analyze_module_effectiveness(db: Session, module_id: int) -> dict:
    """
    Orchestre les 4 étapes et retourne l'analyse complète d'un module.
    """
    kpi_data     = get_kpi_improvement_data(db, module_id)
    mastery_data = get_time_to_mastery_data(db, module_id)
    dropoff_data = get_dropoff_data(db, module_id)

    score = generate_effectiveness_score(
        db=db,
        module_id=module_id,
        kpi_data=kpi_data,
        mastery_data=mastery_data,
        dropoff_data=dropoff_data,
    )

    return {
        "module_id":   module_id,
        "raw_data": {
            "kpi":     kpi_data,
            "mastery": mastery_data,
            "dropoff": dropoff_data,
        },
        "analysis":    score,
    }


# ────────────────────────────────────────────────────────────────
# ADMIN — Analyse de tous les modules d'un rôle
# ────────────────────────────────────────────────────────────────
def analyze_all_modules(db: Session, role_id: int) -> list:
    """
    Analyse tous les modules d'un rôle et retourne la liste
    triée par effectiveness_score (les moins performants en premier).
    """
    module_rows = db.execute(text("""
        SELECT m.id
        FROM modules m
        WHERE m.career_path_id = :role_id
          AND m.is_active = true
        ORDER BY m.display_order ASC
    """), {"role_id": role_id}).fetchall()

    results = []
    for row in module_rows:
        try:
            result = analyze_module_effectiveness(db, row.id)
            results.append(result)
        except Exception as e:
            results.append({
                "module_id": row.id,
                "error": str(e)
            })

    # Trier par effectiveness_score (les plus critiques en premier)
    results.sort(
        key=lambda x: x.get("analysis", {}).get("effectiveness_score", 100)
    )
    return results