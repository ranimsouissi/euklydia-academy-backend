# app/api/v1/endpoints/sequencing.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.services import sequencing_service
from app.services import feedback_service

router = APIRouter()


# ----------------------------------------------------------------
# GET /sequencing/next/{module_id} — Module suivant recommandé
# ----------------------------------------------------------------

@router.get("/next/{module_id}")
def get_next_recommendation(
    module_id:    int,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    """
    Recommande le prochain module basé sur :
    - Mastery de l'apprenant
    - KPI before/after soumis
    - Execution Task soumise
    - Temps disponible par semaine

    Utilise LLM si disponible, sinon fallback règle simple.
    """
    recommendation = sequencing_service.generate_next_recommendation(
        db, current_user.id, module_id
    )

    # ── Alerte pacing si stagnation détectée ─────────────────
    roadmap    = sequencing_service.get_learner_roadmap(db, current_user.id)
    modules    = roadmap.get("modules", [])

    modules_without_improvement = sum(
        1 for m in modules
        if m.get("execution_task_submitted")
        and not m.get("kpi_after")
    )

    pacing_alert = feedback_service.generate_pacing_alert(
        modules_without_improvement=modules_without_improvement,
        last_difficulty=next(
            (m.get("execution_task_difficulty")
             for m in modules
             if m.get("id") == module_id),
            None
        ),
        time_available_per_week=roadmap.get("time_available_per_week")
    )

    return {
        **recommendation,
        "pacing_alert": pacing_alert   # None si pas d'alerte
    }


# ----------------------------------------------------------------
# GET /sequencing/roadmap — Roadmap complet de l'apprenant
# ----------------------------------------------------------------

@router.get("/roadmap")
def get_roadmap(
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    """
    Retourne le roadmap complet de l'apprenant avec :
    - Mastery par module
    - KPI before/after
    - Execution Task soumise
    - Temps disponible par semaine
    """
    roadmap = sequencing_service.get_learner_roadmap(db, current_user.id)
    return roadmap