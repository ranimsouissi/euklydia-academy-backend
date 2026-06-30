# app/api/v1/endpoints/admin.py
"""
Admin — Cohort Analytics Endpoints
=====================================
Dashboard admin pour l'analyse de la cohorte d'apprenants.

Endpoints :
  GET /admin/cohort/overview            — stats globales tous rôles
  GET /admin/cohort/role/{role}         — stats par rôle
  GET /admin/cohort/module/{module_id}  — analyse détaillée d'un module

Utilise la logique existante dans performance_service.py +
sauvegarde dans cohort_insights (table créée en validation BD).

Sécurité : tous les endpoints requièrent is_admin=True sur l'utilisateur.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
import json
from datetime import datetime

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.services import performance_service

router = APIRouter()


# ----------------------------------------------------------------
# Guard — vérifie que l'utilisateur est admin
# ----------------------------------------------------------------

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Vérifie que l'utilisateur connecté est admin.
    """
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux administrateurs."
        )
    return current_user


# ----------------------------------------------------------------
# GET /admin/cohort/overview — Stats globales tous rôles
# ----------------------------------------------------------------

@router.get("/cohort/overview")
def get_cohort_overview(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Vue globale de la cohorte :
    - Nombre d'apprenants par rôle
    - Score moyen de mastery par rôle
    - Taux de complétion global
    - Modules les plus et moins performants
    """
    # Stats par rôle
    role_stats = db.execute(text("""
        SELECT
            m.role,
            COUNT(DISTINCT ump.user_id)          AS learners_count,
            AVG(lsm.mastery_score)               AS avg_mastery,
            AVG(ump.progress_percent)            AS avg_progress,
            SUM(CASE WHEN ump.status = 'completed' THEN 1 ELSE 0 END) AS completions
        FROM modules m
        LEFT JOIN user_module_progress ump ON ump.module_id = m.id
        LEFT JOIN module_skills ms         ON ms.module_id = m.id
        LEFT JOIN learner_skill_mastery lsm
               ON lsm.skill_id = ms.skill_id AND lsm.user_id = ump.user_id
        WHERE m.is_active = true
        GROUP BY m.role
        ORDER BY m.role
    """)).fetchall()

    # Top modules (meilleur taux de complétion)
    top_modules = db.execute(text("""
        SELECT
            m.id,
            m.title_fr,
            m.role,
            m.level,
            COUNT(DISTINCT ump.user_id) AS learners,
            AVG(ump.progress_percent)   AS avg_progress,
            SUM(CASE WHEN ump.status = 'completed' THEN 1 ELSE 0 END) AS completions
        FROM modules m
        LEFT JOIN user_module_progress ump ON ump.module_id = m.id
        WHERE m.is_active = true
        GROUP BY m.id, m.title_fr, m.role, m.level
        ORDER BY completions DESC, avg_progress DESC
        LIMIT 5
    """)).fetchall()

    # Stats globales
    global_stats = db.execute(text("""
        SELECT
            COUNT(DISTINCT u.id)                                        AS total_learners,
            COUNT(DISTINCT CASE WHEN ump.status = 'completed'
                           THEN ump.user_id END)                        AS learners_with_completion,
            AVG(lsm.mastery_score)                                      AS global_avg_mastery,
            COUNT(DISTINCT pp.id)                                       AS total_pain_points
        FROM users u
        LEFT JOIN user_module_progress ump ON ump.user_id = u.id
        LEFT JOIN learner_skill_mastery lsm ON lsm.user_id = u.id
        LEFT JOIN pain_points pp            ON pp.user_id  = u.id
    """)).fetchone()

    return {
        "global": {
            "total_learners":          global_stats.total_learners or 0,
            "learners_with_completion": global_stats.learners_with_completion or 0,
            "global_avg_mastery":      round(float(global_stats.global_avg_mastery or 0) * 100, 1),
            "total_pain_points":       global_stats.total_pain_points or 0,
        },
        "by_role": [
            {
                "role":           r.role,
                "learners_count": r.learners_count or 0,
                "avg_mastery":    round(float(r.avg_mastery or 0) * 100, 1),
                "avg_progress":   round(float(r.avg_progress or 0), 1),
                "completions":    r.completions or 0,
            }
            for r in role_stats
        ],
        "top_modules": [
            {
                "id":           m.id,
                "title":        m.title_fr,
                "role":         m.role,
                "level":        m.level,
                "learners":     m.learners or 0,
                "avg_progress": round(float(m.avg_progress or 0), 1),
                "completions":  m.completions or 0,
            }
            for m in top_modules
        ],
        "generated_at": datetime.utcnow().isoformat(),
    }


# ----------------------------------------------------------------
# GET /admin/cohort/role/{role} — Stats par rôle
# ----------------------------------------------------------------

@router.get("/cohort/role/{role}")
def get_cohort_by_role(
    role: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Stats détaillées pour un rôle spécifique.
    role : 'AI Sales Specialist' | 'AI Marketing Strategist' |
           'AI Designer' | 'AI Project Manager'
    """
    # Modules du rôle avec stats
    modules = db.execute(text("""
        SELECT
            m.id,
            m.title_fr,
            m.level,
            m.display_order,
            COUNT(DISTINCT ump.user_id)  AS learners,
            AVG(ump.progress_percent)    AS avg_progress,
            AVG(lsm.mastery_score)       AS avg_mastery,
            SUM(CASE WHEN ump.status = 'completed' THEN 1 ELSE 0 END) AS completions,
            SUM(CASE WHEN ump.status = 'abandoned' THEN 1 ELSE 0 END) AS abandonments
        FROM modules m
        LEFT JOIN user_module_progress ump ON ump.module_id = m.id
        LEFT JOIN module_skills ms         ON ms.module_id  = m.id
        LEFT JOIN learner_skill_mastery lsm
               ON lsm.skill_id = ms.skill_id AND lsm.user_id = ump.user_id
        WHERE m.is_active = true AND m.role = :role
        GROUP BY m.id, m.title_fr, m.level, m.display_order
        ORDER BY m.display_order
    """), {"role": role}).fetchall()

    if not modules:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucun module trouvé pour le rôle '{role}'."
        )

    # Pain points pour ce rôle
    pain_points = db.execute(text("""
        SELECT
            pp.category,
            COUNT(*)        AS count,
            AVG(pp.severity) AS avg_severity
        FROM pain_points pp
        JOIN users u ON u.id = pp.user_id
        GROUP BY pp.category
        ORDER BY count DESC
        LIMIT 5
    """)).fetchall()

    return {
        "role": role,
        "modules": [
            {
                "id":            m.id,
                "title":         m.title_fr,
                "level":         m.level,
                "learners":      m.learners or 0,
                "avg_progress":  round(float(m.avg_progress or 0), 1),
                "avg_mastery":   round(float(m.avg_mastery or 0) * 100, 1),
                "completions":   m.completions or 0,
                "abandonments":  m.abandonments or 0,
                "completion_rate": round(
                    (m.completions or 0) / max(m.learners or 1, 1) * 100, 1
                ),
            }
            for m in modules
        ],
        "pain_points": [
            {
                "category":     p.category,
                "count":        p.count,
                "avg_severity": round(float(p.avg_severity or 0), 1),
            }
            for p in pain_points
        ],
        "generated_at": datetime.utcnow().isoformat(),
    }


# ----------------------------------------------------------------
# GET /admin/cohort/module/{module_id} — Analyse détaillée d'un module
# ----------------------------------------------------------------

@router.get("/cohort/module/{module_id}")
def get_cohort_module_analysis(
    module_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Analyse détaillée de la cohorte sur un module spécifique :
    - Engagement par section (lesson)
    - Drop-off points
    - Insights LLM générés et sauvegardés dans cohort_insights
    """
    # Vérifier que le module existe
    module = db.execute(text("""
        SELECT id, title_fr, role, level FROM modules WHERE id = :mid
    """), {"mid": module_id}).fetchone()

    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module {module_id} introuvable."
        )

    # Récupérer engagement et drop-offs via performance_service
    engagement = performance_service.get_cohort_engagement(db, module_id)
    dropoffs   = performance_service.get_cohort_dropoffs(db, module_id)

    # Générer les insights LLM
    try:
        insights = performance_service.generate_cohort_insights(
            module_id=module_id,
            engagement=engagement,
            dropoffs=dropoffs,
        )
    except Exception as e:
        insights = {"error": str(e), "summary": "Génération d'insights indisponible."}

    # Sauvegarder dans cohort_insights
    try:
        db.execute(text("""
            INSERT INTO cohort_insights
                (cohort_name, role, metric_type, payload, period_start, period_end, generated_at)
            VALUES
                (:cohort_name, :role, 'module_analysis', CAST(:payload AS jsonb),
                 CURRENT_DATE - INTERVAL '30 days', CURRENT_DATE, NOW())
        """), {
            "cohort_name": f"Module {module_id} — {module.title_fr}",
            "role":        module.role,
            "payload":     json.dumps({
                "module_id":  module_id,
                "insights":   insights,
                "engagement": engagement,
                "dropoffs":   dropoffs,
            }, ensure_ascii=False, default=str),
        })
        db.commit()
    except Exception:
        db.rollback()  # Non bloquant — on retourne quand même les insights

    return {
        "module": {
            "id":    module.id,
            "title": module.title_fr,
            "role":  module.role,
            "level": module.level,
        },
        "engagement":    engagement,
        "dropoffs":      dropoffs,
        "insights":      insights,
        "generated_at":  datetime.utcnow().isoformat(),
    }