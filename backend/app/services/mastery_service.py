# app/services/mastery_service.py
"""
Mastery Update Service
======================
Met à jour automatiquement learner_skill_mastery après chaque
Execution Task soumise et KPI Measurement complété.

Sources de données (nouvelle structure) :
  - kpi_before / kpi_after    → amélioration mesurable
  - execution_task_submitted  → signal de complétion
  - difficulty                → signal de blocage déclaré
  - section_progress          → progression par section

Mastery levels :
  0.0  - 0.39 → novice
  0.4  - 0.59 → beginner
  0.6  - 0.74 → practitioner
  0.75 - 0.89 → advanced
  0.9  - 1.0  → expert

Fallback sans LLM : règles simples basées sur
kpi_improvement + execution_task_submitted
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import text


def get_mastery_level(score: float) -> str:
    if score < 0.4:  return "novice"
    if score < 0.6:  return "beginner"
    if score < 0.75: return "practitioner"
    if score < 0.9:  return "advanced"
    return "expert"


def get_skill_for_module(
    db:        Session,
    module_id: int
) -> Optional[dict]:
    """
    Trouve le skill principal associé au module.
    Remplace get_skill_for_lesson — accès direct via module_id.
    """
    row = db.execute(text(
        "SELECT s.id AS skill_id, s.name AS skill_name "
        "FROM module_skills ms "
        "JOIN skills s ON s.id = ms.skill_id "
        "WHERE ms.module_id = :module_id "
        "LIMIT 1"
    ), {"module_id": module_id}).fetchone()
    return dict(row._mapping) if row else None


def calculate_kpi_improvement(
    kpi_before: Optional[str],
    kpi_after:  Optional[str]
) -> float:
    """
    Calcule un score d'amélioration KPI entre 0.0 et 1.0.
    """
    if not kpi_after:
        return 0.0
    if not kpi_before:
        return 0.3   # soumis sans baseline → amélioration partielle

    # Si les deux sont renseignés et différents → amélioration détectée
    if kpi_after.strip().lower() != kpi_before.strip().lower():
        return 0.6   # amélioration confirmée
    return 0.1       # kpi_after identique → peu d'évolution


def update_mastery_from_execution_task(
    db:                       Session,
    user_id:                  int,
    module_id:                int,
    kpi_before:               Optional[str],
    kpi_after:                Optional[str],
    execution_task_submitted: bool,
    difficulty:               Optional[str],
    reason:                   str = ""
) -> Optional[dict]:
    """
    Met à jour learner_skill_mastery après soumission
    de l'Execution Task ou complétion du KPI Measurement.

    Remplace update_mastery — plus de quiz/exercise/score.
    """
    skill = get_skill_for_module(db, module_id)
    if not skill:
        return None

    skill_id   = skill["skill_id"]
    skill_name = skill["skill_name"]

    # ── Récupérer mastery existante ──────────────────────────
    existing = db.execute(text(
        "SELECT mastery_score, evidence_count, confidence "
        "FROM learner_skill_mastery "
        "WHERE user_id = :user_id AND skill_id = :skill_id"
    ), {"user_id": user_id, "skill_id": skill_id}).fetchone()

    current_mastery  = float(existing.mastery_score) if existing else 0.3
    current_evidence = int(existing.evidence_count)  if existing else 0
    current_conf     = float(existing.confidence)    if existing else 0.5

    # ── Calcul du delta selon les nouvelles sources ──────────
    kpi_improvement = calculate_kpi_improvement(kpi_before, kpi_after)

    if execution_task_submitted and kpi_improvement >= 0.6:
        # Execution Task soumise + KPI amélioré → progression forte
        new_mastery   = min(1.0, current_mastery + 0.15)
        new_conf      = min(1.0, current_conf + 0.1)
        update_reason = "execution_task_submitted + kpi_improved"

    elif execution_task_submitted and kpi_improvement >= 0.3:
        # Execution Task soumise + KPI partiellement amélioré
        new_mastery   = min(1.0, current_mastery + 0.08)
        new_conf      = min(1.0, current_conf + 0.05)
        update_reason = "execution_task_submitted + kpi_partial"

    elif execution_task_submitted and kpi_improvement < 0.3:
        # Execution Task soumise mais KPI peu amélioré
        new_mastery   = min(1.0, current_mastery + 0.03)
        new_conf      = current_conf
        update_reason = "execution_task_submitted + kpi_stagnant"

    else:
        # Pas de soumission → pas de progression
        new_mastery   = current_mastery
        new_conf      = current_conf
        update_reason = "no_submission"

    # ── Pénalité si difficulté élevée déclarée ───────────────
    if difficulty and difficulty.strip().lower() in (
        "élevée", "haute", "difficile", "high", "hard"
    ):
        new_mastery   = max(0.0, new_mastery - 0.05)
        new_conf      = max(0.0, new_conf - 0.05)
        update_reason += " + high_difficulty_declared"

    new_mastery  = round(new_mastery, 4)
    new_level    = get_mastery_level(new_mastery)
    new_evidence = current_evidence + 1
    full_reason  = reason or update_reason

    # ── Upsert learner_skill_mastery ─────────────────────────
    db.execute(text(
        "INSERT INTO learner_skill_mastery "
        "(user_id, skill_id, module_id, mastery_score, mastery_level, "
        "kpi_improvement_rate, confidence, evidence_count, "
        "last_update_reason, last_updated_at, created_at) "
        "VALUES "
        "(:user_id, :skill_id, :module_id, :mastery_score, :mastery_level, "
        ":kpi_improvement_rate, :confidence, :evidence_count, "
        ":reason, NOW(), NOW()) "
        "ON CONFLICT (user_id, skill_id) DO UPDATE SET "
        "module_id            = :module_id, "
        "mastery_score        = :mastery_score, "
        "mastery_level        = :mastery_level, "
        "kpi_improvement_rate = :kpi_improvement_rate, "
        "confidence           = :confidence, "
        "evidence_count       = :evidence_count, "
        "last_update_reason   = :reason, "
        "last_updated_at      = NOW()"
    ), {
        "user_id":             user_id,
        "skill_id":            skill_id,
        "module_id":           module_id,
        "mastery_score":       new_mastery,
        "mastery_level":       new_level,
        "kpi_improvement_rate": round(kpi_improvement, 4),
        "confidence":          round(new_conf, 4),
        "evidence_count":      new_evidence,
        "reason":              full_reason[:500]
    })
    db.commit()

    return {
        "skill_id":            skill_id,
        "skill_name":          skill_name,
        "mastery_score":       new_mastery,
        "mastery_level":       new_level,
        "kpi_improvement_rate": round(kpi_improvement, 4),
        "confidence":          round(new_conf, 4),
        "evidence_count":      new_evidence,
        "reason":              full_reason
    }


def get_learner_mastery_summary(
    db:      Session,
    user_id: int
) -> list[dict]:
    """Résumé mastery de tous les skills de l'apprenant."""
    rows = db.execute(text(
        "SELECT lsm.skill_id, s.name AS skill_name, "
        "lsm.mastery_score, lsm.mastery_level, "
        "lsm.kpi_improvement_rate, lsm.confidence, "
        "lsm.evidence_count, lsm.last_update_reason, "
        "lsm.last_updated_at "
        "FROM learner_skill_mastery lsm "
        "JOIN skills s ON s.id = lsm.skill_id "
        "WHERE lsm.user_id = :user_id "
        "ORDER BY lsm.mastery_score ASC"
    ), {"user_id": user_id}).fetchall()
    return [dict(r._mapping) for r in rows]