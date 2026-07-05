# app/services/performance_service.py
"""
Performance Analysis Agent — Service
=====================================
Analyse les données d'engagement, mastery et drop-off d'un apprenant
et génère des insights actionnables avec top 3 blockers + interventions.

V2 — Améliorations suite à l'intégration tutorials + resources :
  - get_tutorials_data lit depuis section_content_fr.tutorials (priorité)
    puis tutorials_fr (fallback)
  - get_resources_data : nouvelle fonction pour les resources externes
  - generate_insights injecte tutorials ET resources dans le prompt LLM
  - Nouveau type d'intervention : read_resource
  - target_content retourne un titre concret au lieu de null

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

# ----------------------------------------------------------------
# STEP 2 – KPI structurés depuis user_kpi_measurements (V2)
# ----------------------------------------------------------------

def get_kpi_data(db: Session, user_id: int) -> list[dict]:
    """
    Lit les KPI réels depuis user_kpi_measurements.
    Calcule le delta et évalue l'atteinte de la cible.
    Fallback : user_module_progress.kpi_after si aucune mesure structurée.
    """
    rows = db.execute(text("""
        SELECT
            ukm.module_id,
            m.title_fr          AS module_title,
            ukm.indicator,
            ukm.baseline_value,
            ukm.current_value,
            ukm.target_label,
            ukm.unit,
            ukm.measured_at,
            ump.status,
            ump.progress_percent,
            ump.execution_task_submitted,
            ump.execution_task_difficulty
        FROM user_kpi_measurements ukm
        JOIN modules m ON m.id = ukm.module_id
        LEFT JOIN user_module_progress ump
            ON ump.module_id = ukm.module_id
            AND ump.user_id  = ukm.user_id
        WHERE ukm.user_id = :user_id
        ORDER BY ukm.module_id, ukm.indicator
    """), {"user_id": user_id}).fetchall()

    if rows:
        result = []
        for r in rows:
            baseline = float(r.baseline_value) if r.baseline_value is not None else None
            current  = float(r.current_value)  if r.current_value  is not None else None

            # Calcul du delta en %
            delta_pct = None
            if baseline is not None and current is not None and baseline != 0:
                delta_pct = round((current - baseline) / abs(baseline) * 100, 1)

            result.append({
                "module_id":                  r.module_id,
                "module_title":               r.module_title,
                "indicator":                  r.indicator,
                "baseline_value":             baseline,
                "current_value":              current,
                "delta_pct":                  delta_pct,
                "target_label":               r.target_label,
                "unit":                       r.unit,
                "measured":                   current is not None,
                "status":                     r.status,
                "progress_percent":           r.progress_percent,
                "execution_task_submitted":   r.execution_task_submitted,
                "execution_task_difficulty":  r.execution_task_difficulty,
            })
        return result

    # Fallback : ancienne saisie texte libre si pas de mesure structurée
    fallback_rows = db.execute(text("""
        SELECT
            m.id              AS module_id,
            m.title_fr        AS module_title,
            ump.kpi_after,
            ump.execution_task_submitted,
            ump.execution_task_difficulty,
            ump.status,
            ump.progress_percent
        FROM user_module_progress ump
        JOIN modules m ON m.id = ump.module_id
        WHERE ump.user_id  = :user_id
          AND ump.kpi_after IS NOT NULL
        ORDER BY ump.updated_at DESC
    """), {"user_id": user_id}).fetchall()

    return [dict(r._mapping) for r in fallback_rows] if fallback_rows else []


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
# FIX V2 : priorité à section_content_fr.tutorials, fallback tutorials_fr
# ----------------------------------------------------------------

def get_tutorials_data(db: Session, user_id: int) -> list[dict]:
    """
    Récupère les tutoriels des modules démarrés par l'apprenant.
    Priorité : section_content_fr.tutorials (nouvelle source avec steps)
    Fallback  : tutorials_fr (ancienne colonne)
    """
    rows = db.execute(text("""
        SELECT
            m.id              AS module_id,
            m.title_fr        AS module_title,
            m.tutorials_fr,
            m.section_content_fr
        FROM user_module_progress ump
        JOIN modules m ON m.id = ump.module_id
        WHERE ump.user_id = :user_id
    """), {"user_id": user_id}).fetchall()

    result = []
    for r in rows:
        # Priorité à section_content_fr.tutorials
        tutorials = []
        if r.section_content_fr:
            tutorials = r.section_content_fr.get("tutorials", [])
        # Fallback sur tutorials_fr si section_content vide
        if not tutorials and r.tutorials_fr:
            tutorials = r.tutorials_fr

        for tuto in tutorials:
            result.append({
                "module_id":    r.module_id,
                "module_title": r.module_title,
                "tutorial_id":  tuto.get("id"),
                "title":        tuto.get("title"),
                "tool":         tuto.get("tool"),
            })
    return result


# ----------------------------------------------------------------
# STEP 4c — Resources disponibles pour les modules de l'apprenant
# NOUVEAU V2 : resources externes (articles, outils, vidéos)
# ----------------------------------------------------------------

def get_resources_data(db: Session, user_id: int) -> list[dict]:
    """
    Récupère les resources externes des modules démarrés par l'apprenant.
    Source : section_content_fr.resources
    """
    rows = db.execute(text("""
        SELECT
            m.id              AS module_id,
            m.title_fr        AS module_title,
            m.section_content_fr
        FROM user_module_progress ump
        JOIN modules m ON m.id = ump.module_id
        WHERE ump.user_id = :user_id
          AND m.section_content_fr IS NOT NULL
    """), {"user_id": user_id}).fetchall()

    result = []
    for r in rows:
        resources = (r.section_content_fr or {}).get("resources", [])
        for res in resources:
            result.append({
                "module_id":    r.module_id,
                "module_title": r.module_title,
                "resource_id":  res.get("id"),
                "title":        res.get("title"),
                "type":         res.get("type"),
                "url":          res.get("url"),
            })
    return result

# ----------------------------------------------------------------
# STEP 5b — Calcul des moyennes KPI en Python (V2)
# ----------------------------------------------------------------

def compute_kpi_averages(kpi_data: list[dict]) -> tuple[float, float]:
    """
    Calcule kpi_before_avg et kpi_after_avg depuis les données structurées.
    Retourne le ratio current/baseline pour les indicateurs mesurés.
    """
    measured = [k for k in kpi_data if k.get("measured") and
                k.get("baseline_value") is not None and
                k.get("current_value") is not None and
                k.get("baseline_value") != 0]

    if not measured:
        return (0.0, 0.0)

    ratios = []
    for k in measured:
        baseline = k["baseline_value"]
        current  = k["current_value"]
        ratio = current / baseline
        ratios.append(ratio)

    kpi_before_avg = round(1.0, 2)
    kpi_after_avg  = round(sum(ratios) / len(ratios), 2)

    return (kpi_before_avg, kpi_after_avg)

# ----------------------------------------------------------------
# COHORT KPI — Agrégation KPI structurés par module (V2)
# ----------------------------------------------------------------

def get_cohort_kpi_data(db: Session, module_id: int) -> list[dict]:
    """
    Agrège les KPI structurés depuis user_kpi_measurements pour un module.
    Retourne par indicateur : baseline_avg, current_avg, delta_avg_pct,
    learners_measured, learners_total, target_label, unit.
    """
    rows = db.execute(text("""
        SELECT
            ukm.indicator,
            ukm.target_label,
            ukm.unit,
            AVG(ukm.baseline_value)                          AS baseline_avg,
            AVG(ukm.current_value)                           AS current_avg,
            COUNT(*)                                         AS learners_total,
            SUM(CASE WHEN ukm.current_value IS NOT NULL
                THEN 1 ELSE 0 END)                           AS learners_measured
        FROM user_kpi_measurements ukm
        WHERE ukm.module_id = :module_id
        GROUP BY ukm.indicator, ukm.target_label, ukm.unit
        ORDER BY ukm.indicator
    """), {"module_id": module_id}).fetchall()

    result = []
    for r in rows:
        baseline_avg = float(r.baseline_avg) if r.baseline_avg is not None else None
        current_avg  = float(r.current_avg)  if r.current_avg  is not None else None

        delta_avg_pct = None
        if baseline_avg and current_avg and baseline_avg != 0:
            delta_avg_pct = round(
                (current_avg - baseline_avg) / abs(baseline_avg) * 100, 1
            )

        result.append({
            "indicator":         r.indicator,
            "target_label":      r.target_label,
            "unit":              r.unit,
            "baseline_avg":      round(baseline_avg, 2) if baseline_avg else None,
            "current_avg":       round(current_avg, 2)  if current_avg  else None,
            "delta_avg_pct":     delta_avg_pct,
            "learners_measured": int(r.learners_measured),
            "learners_total":    int(r.learners_total),
            "measurement_rate":  round(
                int(r.learners_measured) / int(r.learners_total), 2
            ) if r.learners_total else 0,
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
    resources: list[dict] = [],
    scope:     str = "learner"
) -> dict:
    """
    Appelle GPT pour générer des insights actionnables.
    V2 : injecte tutorials ET resources dans le prompt.
    """
    prompt = f"""Tu es un analyste pédagogique expert pour la plateforme Euklydia.
Analyse ces données d'apprentissage et génère des insights actionnables.

--- ENGAGEMENT PAR MODULE ---
{json.dumps(engagement, ensure_ascii=False, default=str)}

--- KPI AVANT / APRÈS (données structurées) ---
{json.dumps(kpi_data, ensure_ascii=False, default=str)}
Note : chaque entrée contient indicator, baseline_value, current_value, delta_pct (variation en %), target_label (cible visée), measured (true si valeur finale saisie).
Si delta_pct est négatif → réduction (bon pour CAC, cycle). Si positif → augmentation (bon pour volume).
Compare delta_pct à target_label pour évaluer si la cible est atteinte.

--- MASTERY PAR SKILL ---
{json.dumps(mastery, ensure_ascii=False, default=str)}

--- DROP-OFF PAR SECTION ---
{json.dumps(dropoffs, ensure_ascii=False, default=str)}

--- TUTORIELS DISPONIBLES ---
{json.dumps(tutorials, ensure_ascii=False, default=str)}

--- RESOURCES DISPONIBLES ---
{json.dumps(resources, ensure_ascii=False, default=str)}

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
      "target_content": "OBLIGATOIRE si type=watch_tutorial ou read_resource : utilise EXACTEMENT le titre d'un tutoriel ou d'une resource des listes ci-dessus, sinon null",
      "type": "review_section|watch_tutorial|read_resource|coach_session",
      "reason": "pourquoi cette intervention",
      "priority": "high|medium|low"
    }}
  ],
  "trend": "improving|stagnant|declining"
}}

Règles :
- top_blockers : 3 items MAX, jamais le même skill
- interventions : 1 par blocker
- types disponibles : review_section | watch_tutorial | read_resource | coach_session
- Si type=watch_tutorial → target_content DOIT être le titre exact d'un tutoriel de TUTORIELS DISPONIBLES
- Si type=read_resource → target_content DOIT être le titre exact d'une resource de RESOURCES DISPONIBLES
- Si aucun tutoriel/resource disponible et type=watch_tutorial ou read_resource → utilise review_section
- target_content ne doit JAMAIS être null si type=watch_tutorial ou read_resource
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
    dropoffs:   list[dict],
    kpi_cohort: list[dict] = [],  # 🆕
) -> dict:
    client = _get_client()

    prompt = f"""Tu es un analyste pédagogique expert pour la plateforme Euklydia.
Analyse ces données d'engagement pour le module {module_id}.

--- ENGAGEMENT PAR MODULE ---
{json.dumps(engagement, ensure_ascii=False, default=str)}

--- DROP-OFF PAR SECTION ---
{json.dumps(dropoffs, ensure_ascii=False, default=str)}

--- KPI COHORTE (données structurées V2) ---
{json.dumps(kpi_cohort, ensure_ascii=False, default=str)}
Note : chaque entrée contient indicator, baseline_avg, current_avg, delta_avg_pct (variation moyenne en %),
target_label (cible visée), learners_measured (nombre d'apprenants ayant saisi leur valeur finale),
learners_total (nombre total), measurement_rate (taux de saisie).
Si delta_avg_pct est négatif → réduction (bon pour CAC, cycle). Si positif → augmentation (bon pour volume).
Compare delta_avg_pct à target_label pour évaluer si la cohorte atteint globalement ses objectifs.

Génère EXACTEMENT ce JSON (sans texte autour) :
{{
  "summary": "résumé exécutif en 2 phrases sur la cohorte",
  "completion_rate": 0.0 à 1.0,
  "execution_task_completion_rate": 0.0 à 1.0,
  "main_drop_off_section": "section_type ou null",
  "kpi_insights": {{
    "best_indicator": "indicateur avec le meilleur delta ou null",
    "worst_indicator": "indicateur le moins bien mesuré ou null",
    "avg_measurement_rate": 0.0 à 1.0,
    "comment": "commentaire en 1 phrase sur l'impact business global de la cohorte"
  }},
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
- Si kpi_cohort est vide → kpi_insights avec tous les champs à null et comment = "Aucune donnée KPI disponible"
- Réponds UNIQUEMENT avec le JSON valide"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1000  # augmenté car prompt plus riche
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
# ----------------------------------------------------------------
# ROLE INSIGHTS — Analyse LLM par rôle (V2)
# ----------------------------------------------------------------

def generate_role_insights(
    role:        str,
    modules:     list[dict],
    pain_points: list[dict] = [],
) -> dict:
    """
    Génère un summary + blockers + interventions pour un rôle entier.
    Appelé depuis GET /admin/cohort/role/{role}.
    """
    client = _get_client()

    prompt = f"""Tu es un analyste pédagogique expert pour la plateforme Euklydia.
Analyse les performances de la cohorte pour le rôle "{role}".

--- MODULES DU RÔLE ---
{json.dumps(modules, ensure_ascii=False, default=str)}
Note : chaque module contient learners (apprenants), avg_progress (progression moyenne),
avg_mastery (mastery moyenne en %), completion_rate (taux de complétion en %),
abandonments (abandons).

--- PAIN POINTS DÉTECTÉS ---
{json.dumps(pain_points, ensure_ascii=False, default=str)}

Génère EXACTEMENT ce JSON (sans texte autour) :
{{
  "summary": "résumé exécutif en 2 phrases sur la cohorte de ce rôle",
  "weakest_module": "titre exact du module avec le taux de complétion le plus faible",
  "strongest_module": "titre exact du module avec le meilleur taux de complétion",
  "top_blockers": [
    {{
      "rank": 1,
      "module": "titre exact du module concerné",
      "evidence": "preuve concrète basée sur les données",
      "impact": "impact pédagogique"
    }}
  ],
  "interventions": [
    {{
      "module": "titre exact du module concerné",
      "type": "content_revision|add_examples|simplify|add_checkpoint|coach_session",
      "reason": "pourquoi cette intervention",
      "priority": "high|medium|low"
    }}
  ],
  "trend": "improving|stagnant|declining"
}}

Règles :
- top_blockers : 3 items MAX, un par module différent
- interventions : 1 par blocker
- Base-toi uniquement sur les données fournies, pas d'invention
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
    
# ----------------------------------------------------------------
# ALERTS — Détection automatique des modules critiques (V2)
# ----------------------------------------------------------------

def get_cohort_alerts(db: Session) -> dict:
    """
    Détecte automatiquement les modules critiques sur toute la plateforme.
    Règles :
      🔴 high   : completion_rate < 20% OU drop_off_rate > 50%
      🟡 medium : measurement_rate = 0 OU avg_progress < 30% OU avg_mastery < 30%
    """
    # 1. Récupérer les stats de tous les modules actifs
    modules = db.execute(text("""
        SELECT
            m.id,
            m.title_fr,
            m.role,
            m.level,
            COUNT(DISTINCT ump.user_id)                         AS learners_count,
            AVG(ump.progress_percent)                           AS avg_progress,
            AVG(lsm.mastery_score)                              AS avg_mastery,
            SUM(CASE WHEN ump.status = 'completed'
                THEN 1 ELSE 0 END)                              AS completions
        FROM modules m
        LEFT JOIN user_module_progress ump ON ump.module_id = m.id
        LEFT JOIN module_skills ms         ON ms.module_id  = m.id
        LEFT JOIN learner_skill_mastery lsm
               ON lsm.skill_id = ms.skill_id
               AND lsm.user_id = ump.user_id
        WHERE m.is_active = true
        GROUP BY m.id, m.title_fr, m.role, m.level
        HAVING COUNT(DISTINCT ump.user_id) > 0
    """)).fetchall()

    # 2. Drop-off par module
    dropoffs = db.execute(text("""
        SELECT
            e.module_id,
            COUNT(DISTINCT e.user_id)                           AS users_with_dropoff,
            (SELECT COUNT(DISTINCT user_id)
             FROM user_module_progress
             WHERE module_id = e.module_id)                     AS total_users,
            MAX(e.section_type)                                 AS main_section
        FROM events e
        WHERE e.type = 'drop_off'
        GROUP BY e.module_id
    """)).fetchall()

    dropoff_map = {
        r.module_id: {
            "rate": round(r.users_with_dropoff / r.total_users, 2)
                    if r.total_users else 0,
            "section": r.main_section,
        }
        for r in dropoffs
    }

    # 3. KPI measurement rate par module
    kpi_rates = db.execute(text("""
        SELECT
            module_id,
            COUNT(*)                                            AS total,
            SUM(CASE WHEN current_value IS NOT NULL
                THEN 1 ELSE 0 END)                             AS measured
        FROM user_kpi_measurements
        GROUP BY module_id
    """)).fetchall()

    kpi_map = {
        r.module_id: round(r.measured / r.total, 2) if r.total else 0
        for r in kpi_rates
    }

    # 4. Appliquer les règles d'alerte
    critical = []
    medium   = []

    for m in modules:
        learners     = m.learners_count or 0
        avg_progress = float(m.avg_progress or 0)
        avg_mastery  = float(m.avg_mastery  or 0) * 100
        completion_rate = round(
            (m.completions or 0) / max(learners, 1) * 100, 1
        )
        drop_info       = dropoff_map.get(m.id, {"rate": 0, "section": None})
        kpi_rate        = kpi_map.get(m.id, None)

        base = {
            "module_id":       m.id,
            "module_title":    m.title_fr,
            "role":            m.role,
            "level":           m.level,
            "learners_count":  learners,
            "completion_rate": completion_rate,
            "avg_progress":    round(avg_progress, 1),
            "avg_mastery":     round(avg_mastery, 1),
            "drop_off_rate":   drop_info["rate"],
        }

        # 🔴 Alertes critiques
        if completion_rate < 20:
            critical.append({
                **base,
                "alert_type": "low_completion",
                "message":    f"Taux de complétion critique : {completion_rate}%",
                "severity":   "high",
            })
        elif drop_info["rate"] > 0.5:
            critical.append({
                **base,
                "alert_type": "high_dropoff",
                "message":    f"Drop-off élevé ({round(drop_info['rate']*100)}%) sur la section {drop_info['section']}",
                "severity":   "high",
            })

        # 🟡 Alertes medium
        else:
            reasons = []
            if kpi_rate is not None and kpi_rate == 0:
                reasons.append("Aucun KPI mesuré par les apprenants")
            if avg_progress < 30:
                reasons.append(f"Progression moyenne faible : {round(avg_progress, 1)}%")
            if avg_mastery < 30:
                reasons.append(f"Mastery moyenne faible : {round(avg_mastery, 1)}%")

            if reasons:
                medium.append({
                    **base,
                    "alert_type": "needs_attention",
                    "message":    " | ".join(reasons),
                    "severity":   "medium",
                })

    return {
        "total_alerts":  len(critical) + len(medium),
        "critical_count": len(critical),
        "medium_count":   len(medium),
        "critical":      critical,
        "medium":        medium,
    }
