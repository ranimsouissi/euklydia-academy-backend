# app/api/v1/endpoints/recommendation.py
"""
Adaptive Recommendation Agent — Endpoints
==========================================
GET /recommendation/full/{module_id}
    → Recommandation complète (module suivant + section à revoir + plan + stagnation)

GET /recommendation/stagnation
    → Vérifie uniquement la stagnation (pour dashboard)
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.services import recommendation_service

router = APIRouter()


@router.get("/full/{module_id}")
def get_full_recommendation(
    module_id:    int,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    """
    Recommandation adaptative complète pour un module donné.

    Retourne :
    - next_module    : prochain module recommandé (avec raison)
    - section_review : section précise à revoir dans le module actuel
    - session_plan   : plan de micro-sessions basé sur le temps disponible
    - stagnation     : détection stagnation + message reset si nécessaire
    """
    return recommendation_service.get_full_recommendation(
        db, current_user.id, module_id
    )


@router.get("/stagnation")
def check_stagnation(
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    """
    Vérifie uniquement la stagnation de l'apprenant.
    Utile pour afficher une alerte sur le Dashboard.
    """
    return recommendation_service.detect_stagnation(db, current_user.id)


@router.get("/session-plan")
def get_session_plan(
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    """
    Retourne le plan de micro-sessions hebdomadaire.
    Utile si l'apprenant vient de mettre à jour son temps disponible.
    """
    return recommendation_service.get_weekly_session_plan(db, current_user.id)
@router.get("/history")
def get_recommendation_history(
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    """Retourne l'historique des recommandations de l'apprenant."""
    return recommendation_service.get_recommendation_history(
        db, current_user.id
    )
@router.post("/{recommendation_id}/feedback")
def submit_recommendation_feedback(
    recommendation_id: int,
    payload:           dict,
    db:                Session = Depends(get_db),
    current_user:      User    = Depends(get_current_user),
):
    """
    Enregistre le feedback de l'apprenant sur une recommandation.
    payload: { "feedback": "followed" | "not_relevant" }
    """
    feedback = payload.get("feedback")
    if feedback not in ("followed", "not_relevant"):
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="feedback doit être 'followed' ou 'not_relevant'")

    db.execute(text("""
        UPDATE user_recommendations
        SET feedback = :feedback
        WHERE id = :id AND user_id = :user_id
    """), {
        "feedback": feedback,
        "id":       recommendation_id,
        "user_id":  current_user.id
    })
    db.commit()
    return {"message": "Feedback enregistré", "id": recommendation_id, "feedback": feedback}