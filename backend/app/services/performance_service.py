# app/services/performance_service.py
"""
Performance Analysis Agent — Service
=====================================
Analyse les données d'engagement, mastery et drop-off d'un apprenant
et génère des insights actionnables avec top 3 blockers + interventions.

V1 — Sources de données :
  - user_module_progress  → progression + section_progress + kpi_after
  - learner_skill_mastery → mastery par skill
  - events                → drop-off par section_type
  - pain_points           → frictions détectées par le TutorChat
"""
import json
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


# ----------------------------------------------------------------
# STEP 1 — Engagement réel depuis user_module_progress + events
# ----------------------------------------------------------------

def get_engagement_data(db: Session, user_id: int) -> dict:
    module_rows = db.execute(text("""
        SELECT
            m.id              AS module_id,
            m.title_fr        AS module_title,
            m.level,
            ump.status,
            ump.progress_percent,
            ump.section_progress,
            ump.execution_task_submitted,
            ump.kpi_after,
            ump.started_at,
            ump.completed_at,
            ump.updated_at
        FROM user_module_progress ump
        JOIN modules m ON m.id = ump.module_id
        WHERE ump.user_id = :user_id
        ORDER BY ump.updated_at DESC
    """), {"user_id": user_id}).fetchall()

    event_rows = db.execute(text("""
        SELECT
            e.type,
            e.module_id,
            m.title_fr  AS module_title,
            e.section_type,
            COUNT(*)    AS count
        FROM events e
        LEFT JOIN modules m ON m.id = e.module_id
        WHERE e.user_id = :user_id
        GROUP BY e.type, e.module_id, m.title_fr, e.section_type
        ORDER BY count DESC
        LIMIT 10
    """), {"user_id": user_id}).fetchall()

    pain_rows = db.execute(text("""
        SELECT summary, category, severity, captured_at
        FROM pain_points
        WHERE user_id = :user_id
        ORDER BY captured_at DESC
        LIMIT 5
    """), {"user_id": user_id}).fetchall()

    engagement = []
    for r in module_rows:
        engagement.append({
            "module_id":                r.module_id,
            "module_title":             r.module_title,
            "level":                    r.level,
            "status":                   r.status,
            "progress_percent":         r.progress_percent,
            "section_progress":         r.section_progress,
            "execution_task_submitted": r.execution_task_submitted,
            "kpi_after":                r.kpi_after,
            "started_at":               str(r.started_at)   if r.started_at   else None,
            "completed_at":             str(r.completed_at) if r.completed_at else None,
        })

    if not engagement:
        return {
            "message":           "Aucun module démarré — première session",
            "modules_started":   0,
            "modules_completed": 0,
        }

    return {
        "modules":           engagement,
        "events":            [dict(r._mapping) for r in event_rows],
        "pain_points":       [dict(r._mapping) for r in pain_rows],
        "modules_started":   len([m for m in engagement
                                  if m["status"] in ("in_progress", "completed")]),
        "modules_completed": len([m for m in engagement
                                  if m["status"] == "completed"]),
    }


# ----------------------------------------------------------------
# STEP 2 — KPI before / after depuis user_module_progress
# ----------------------------------------------------------------

def get_kpi_data(db: Session, user_id: int) -> list[dict]:
    rows = db.execute(text("""
        SELECT
            m.id              AS module_id,
            m.title_fr        AS module_title,
            m.kpi_before_fr   AS kpi_before,
            ump.kpi_after,
            ump.execution_task_submitted,
            ump.execution_task_difficulty,
            ump.status,
            ump.progress_percent
        FROM user_module_progress ump
        JOIN modules m ON m.id = ump.module_id
        WHERE ump.user_id = :user_id
        ORDER BY ump.updated_at DESC
    """), {"user_id": user_id}).fetchall()

    return [dict(r._mapping) for r in rows] if rows else []


# ----------------------------------------------------------------
# STEP 3 — Mastery réelle depuis learner_skill_mastery
# ----------------------------------------------------------------

def get_mastery_data(db: Session, user_id: int) -> list[dict]:
    rows = db.execute(text("""
        SELECT
            lsm.skill_id,
            s.name              AS skill_name,
            s.use_case_name,
            lsm.mastery_score,
            lsm.mastery_level,
            lsm.kpi_improvement_rate,
            lsm.confidence,
            lsm.evidence_count,
            lsm.last_update_reason
        FROM learner_skill_mastery lsm
        LEFT JOIN skills s ON s.id = lsm.skill_id
        WHERE lsm.user_id = :user_id
        ORDER BY lsm.mastery_score ASC
    """), {"user_id": user_id}).fetchall()

    if rows:
        return [dict(r._mapping) for r in rows]

    diag_rows = db.execute(text("""
        SELECT
            uss.skill_id,
            s.name          AS skill_name,
            s.use_case_name,
            uss.score / 100.0 AS mastery_score,
            CASE
                WHEN uss.score < 40  THEN 'novice'
                WHEN uss.score < 60  THEN 'beginner'
                WHEN uss.score < 75  THEN 'practitioner'
                WHEN uss.score < 90  THEN 'advanced'
                ELSE 'expert'
            END AS mastery_level,
            0.0 AS kpi_improvement_rate,
            0.5 AS confidence,
            0   AS evidence_count,
            'diagnostic_score' AS last_update_reason
        FROM user_skill_scores uss
        JOIN skills s ON s.id = uss.skill_id
        WHERE uss.user_id = :user_id
        ORDER BY uss.score ASC
        LIMIT 10
    """), {"user_id": user_id}).fetchall()

    return [dict(r._mapping) for r in diag_rows] if diag_rows else []


# ----------------------------------------------------------------
# STEP 4 — Drop-off par section_type depuis events
# ----------------------------------------------------------------

def get_dropoff_data(db: Session, user_id: int) -> list[dict]:
    rows = db.execute(text("""
        SELECT
            e.module_id,
            m.title_fr      AS module_title,
            e.section_type,
            COUNT(*)        AS drop_off_count
        FROM events e
        JOIN modules m ON m.id = e.module_id
        WHERE e.user_id   = :user_id
          AND e.type      = 'drop_off'
        GROUP BY e.module_id, m.title_fr, e.section_type
        ORDER BY drop_off_count DESC
        LIMIT 5
    """), {"user_id": user_id}).fetchall()

    return [dict(r._mapping) for r in rows] if rows else []


# ----------------------------------------------------------------
# STEP 4b — Tutoriels disponibles pour les modules de l'apprenant
# ----------------------------------------------------------------

def get_tutorials_data(db: Session, user_id: int) -> list[dict]:
    """Récupère les tutoriels des modules démarrés par l'apprenant."""
    rows = db.execute(text("""
        SELECT m.id AS module_id, m.title_fr AS module_title, m.tutorials_fr
        FROM user_module_progress ump
        JOIN modules m ON m.id = ump.module_id
        WHERE ump.user_id = :user_id
          AND m.tutorials_fr IS NOT NULL
    """), {"user_id": user_id}).fetchall()

    result = []
    for r in rows:
        for tuto in (r.tutorials_fr or []):
            result.append({
                "module_id":    r.module_id,
                "module_title": r.module_title,
                "tutorial_id":  tuto.get("id"),
                "title":        tuto.get("title"),
                "tool":         tuto.get("tool"),
            })
    return result


# ----------------------------------------------------------------
# STEP 5 — Appel LLM pour générer les insights
# ----------------------------------------------------------------

def generate_insights(
    engagement,
    mastery:   list[dict],
    dropoffs:  list[dict],
    kpi_data:  list[dict],
    tutorials: list[dict] = [],
    scope:     str = "learner"
) -> dict:
    """
    Appelle GPT pour générer des insights actionnables.
    """
    prompt = f"""Tu es un analyste pédagogique expert pour la plateforme Euklydia.
Analyse ces données d'apprentissage et génère des insights actionnables.

--- ENGAGEMENT PAR MODULE ---
{json.dumps(engagement, ensure_ascii=False, default=str)}

--- KPI BEFORE / AFTER + EXECUTION TASK ---
{json.dumps(kpi_data, ensure_ascii=False, default=str)}

--- MASTERY PAR SKILL ---
{json.dumps(mastery, ensure_ascii=False, default=str)}

--- DROP-OFF PAR SECTION ---
{json.dumps(dropoffs, ensure_ascii=False, default=str)}

--- TUTORIELS DISPONIBLES ---
{json.dumps(tutorials, ensure_ascii=False, default=str)}

Génère EXACTEMENT ce JSON (sans texte autour) :
{{
  "summary": "résumé exécutif en 2 phrases max",
  "engagement_rate": 0.0 à 1.0,
  "kpi_before_avg": 0.0 à 1.0,
  "kpi_after_avg": 0.0 à 1.0,
  "execution_task_completion_rate": 0.0 à 1.0,
  "main_drop_off_section": "section_type ou null",
  "top_blockers": [
    {{
      "rank": 1,
      "skill": "nom du skill",
      "section_type": "use_case|kpi|execution_content|execution_task|kpi_measurement",
      "mastery_score": 0.0 à 1.0,
      "kpi_improvement_rate": 0.0 à 1.0,
      "drop_off_rate": 0.0 à 1.0,
      "evidence": "preuve concrète",
      "impact": "impact business"
    }}
  ],
  "interventions": [
    {{
      "skill": "nom du skill",
      "section_type": "section concernée",
      "target_content": "OBLIGATOIRE si type=watch_tutorial : utilise EXACTEMENT le titre d'un tutoriel de la liste TUTORIELS DISPONIBLES ci-dessus, sinon null",
      "type": "review_section|watch_tutorial|coach_session",
      "reason": "pourquoi cette intervention",
      "priority": "high|medium|low"
    }}
  ],
  "trend": "improving|stagnant|declining"
}}

Règles :
- top_blockers : 3 items MAX, jamais le même skill
- interventions : 1 par blocker
- type : review_section | watch_tutorial | coach_session
- Si type=watch_tutorial, target_content DOIT contenir le titre exact d'un tutoriel de la liste TUTORIELS DISPONIBLES — jamais null
- Si aucun tutoriel disponible et type=watch_tutorial, utilise review_section à la place
- Réponds UNIQUEMENT avec le JSON valide"""

    client = _get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=800
    )

    raw = (response.choices[0].message.content or "").strip()
    if raw.startswith("```"):
        raw = raw.strip("`").strip()
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "Parsing failed", "_raw": raw[:500]}


# ----------------------------------------------------------------
# STEP 6 — Sauvegarder insights + interventions
# ----------------------------------------------------------------

def save_insights(
    db: Session,
    user_id: int,
    insights: dict,
    scope: str = "learner"
):
    db.execute(text("""
        INSERT INTO performance_insights
          (user_id, scope, insight_type, payload, generated_at)
        VALUES
          (:user_id, :scope, 'blocker', CAST(:payload AS jsonb), NOW())
    """), {
        "user_id": user_id,
        "scope":   scope,
        "payload": json.dumps(insights, ensure_ascii=False)
    })
    db.commit()


def save_interventions(db: Session, user_id: int, insights: dict):
    for item in insights.get("interventions", []):
        row = db.execute(text("""
            SELECT id FROM skills
            WHERE name ILIKE :name LIMIT 1
        """), {"name": f"%{item.get('skill', '')}%"}).fetchone()

        skill_id = row[0] if row else None

        db.execute(text("""
            INSERT INTO interventions
              (user_id, skill_id, section_type, target_content,
               type, reason, evidence, status, created_at)
            VALUES
              (:user_id, :skill_id, :section_type, :target_content,
               :type, :reason, CAST(:evidence AS jsonb), 'pending', NOW())
        """), {
            "user_id":        user_id,
            "skill_id":       skill_id,
            "section_type":   item.get("section_type", "execution_content"),
            "target_content": item.get("target_content"),
            "type":           item.get("type", "review_section"),
            "reason":         item.get("reason", ""),
            "evidence":       json.dumps({
                                  "priority": item.get("priority", "medium")
                              })
        })
    db.commit()


# ----------------------------------------------------------------
# COHORT ANALYSIS
# ----------------------------------------------------------------

def get_cohort_engagement(db: Session, module_id: int) -> list[dict]:
    rows = db.execute(text("""
        SELECT
            m.id              AS module_id,
            m.title_fr        AS module_title,
            COUNT(DISTINCT ump.user_id)  AS learners_count,
            AVG(ump.progress_percent)    AS avg_progress,
            SUM(CASE WHEN ump.status = 'completed'   THEN 1 ELSE 0 END) AS completed_count,
            SUM(CASE WHEN ump.status = 'in_progress' THEN 1 ELSE 0 END) AS in_progress_count,
            SUM(CASE WHEN ump.status = 'not_started' THEN 1 ELSE 0 END) AS not_started_count,
            AVG(CASE WHEN ump.kpi_after IS NOT NULL
                THEN 1.0 ELSE 0.0 END)  AS kpi_completion_rate,
            SUM(CASE WHEN ump.execution_task_submitted = true
                THEN 1 ELSE 0 END)      AS execution_task_count
        FROM modules m
        LEFT JOIN user_module_progress ump ON ump.module_id = m.id
        WHERE m.id = :module_id
        GROUP BY m.id, m.title_fr
    """), {"module_id": module_id}).fetchall()

    if rows:
        return [dict(r._mapping) for r in rows]

    return [{
        "module_id":              module_id,
        "learners_count":         0,
        "avg_progress":           0,
        "completed_count":        0,
        "in_progress_count":      0,
        "not_started_count":      0,
        "kpi_completion_rate":    0,
        "execution_task_count":   0,
    }]


def get_cohort_dropoffs(db: Session, module_id: int) -> list[dict]:
    rows = db.execute(text("""
        SELECT
            e.section_type,
            COUNT(*)                  AS drop_off_count,
            COUNT(DISTINCT e.user_id) AS unique_users,
            ROUND(
                COUNT(DISTINCT e.user_id)::numeric /
                NULLIF((
                    SELECT COUNT(DISTINCT user_id)
                    FROM user_module_progress
                    WHERE module_id = :module_id
                ), 0), 2
            ) AS drop_off_rate
        FROM events e
        WHERE e.module_id = :module_id
          AND e.type      = 'drop_off'
        GROUP BY e.section_type
        ORDER BY drop_off_count DESC
    """), {"module_id": module_id}).fetchall()

    return [dict(r._mapping) for r in rows] if rows else []


def generate_cohort_insights(
    module_id:  int,
    engagement: list[dict],
    dropoffs:   list[dict]
) -> dict:
    client = _get_client()

    prompt = f"""Tu es un analyste pédagogique expert pour la plateforme Euklydia.
Analyse ces données d'engagement pour le module {module_id}.

--- ENGAGEMENT PAR MODULE ---
{json.dumps(engagement, ensure_ascii=False, default=str)}

--- DROP-OFF PAR SECTION ---
{json.dumps(dropoffs, ensure_ascii=False, default=str)}

Génère EXACTEMENT ce JSON (sans texte autour) :
{{
  "summary": "résumé exécutif en 2 phrases sur la cohorte",
  "completion_rate": 0.0 à 1.0,
  "execution_task_completion_rate": 0.0 à 1.0,
  "main_drop_off_section": "section_type ou null",
  "top_blockers": [
    {{
      "rank": 1,
      "section_type": "use_case|kpi|execution_content|execution_task|kpi_measurement",
      "drop_off_rate": 0.0 à 1.0,
      "evidence": "preuve concrète",
      "impact": "impact pédagogique"
    }}
  ],
  "interventions": [
    {{
      "section_type": "section concernée",
      "type": "content_revision|add_examples|simplify|add_checkpoint",
      "reason": "pourquoi cette intervention",
      "priority": "high|medium|low"
    }}
  ],
  "trend": "improving|stagnant|declining"
}}

Règles :
- top_blockers : 3 items MAX
- interventions : 1 par blocker
- Réponds UNIQUEMENT avec le JSON valide"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=800
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