# app/api/v1/endpoints/analytics.py
"""
Learning Analytics — Content Effectiveness Scoring
===================================================
Endpoints admin pour analyser l'efficacité du contenu des modules.
Accès réservé aux admins (role_id = 2).
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, require_admin
from app.models.user import User
from app.services import analytics_service

router = APIRouter()


# ----------------------------------------------------------------
# GET /analytics/module/{module_id} — Analyse d'un module
# ----------------------------------------------------------------

@router.get("/module/{module_id}")
def get_module_effectiveness(
    module_id: int,
    db:        Session = Depends(get_db),
    _:         User    = Depends(require_admin),
):
    """
    Analyse l'efficacité du contenu d'un module spécifique.
    Retourne : KPI improvement, time-to-mastery, drop-off, score 0-100.
    """
    result = analytics_service.analyze_module_effectiveness(db, module_id)

    if not result or result.get("raw_data", {}).get("kpi", {}).get("total_learners", 0) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Aucune donnée pour le module {module_id}."
        )

    if "error" in result.get("analysis", {}):
        raise HTTPException(
            status_code=500,
            detail="Erreur génération analyse"
        )

    return result


# ----------------------------------------------------------------
# GET /analytics/role/{role_id} — Analyse tous les modules d'un rôle
# ----------------------------------------------------------------

@router.get("/role/{role_id}")
def get_role_effectiveness(
    role_id: int,
    db:      Session = Depends(get_db),
    _:       User    = Depends(require_admin),
):
    """
    Analyse tous les modules d'un rôle.
    Retourne la liste triée par effectiveness_score (critiques en premier).
    """
    results = analytics_service.analyze_all_modules(db, role_id)

    return {
        "role_id":          role_id,
        "total_modules":    len(results),
        "critical_modules": [
            r for r in results
            if r.get("analysis", {}).get("performance_flag") == "critical"
        ],
        "modules": results,
    }


# ----------------------------------------------------------------
# GET /analytics/module/{module_id}/raw — Données brutes (debug)
# ----------------------------------------------------------------

@router.get("/module/{module_id}/raw")
def get_module_raw_data(
    module_id: int,
    db:        Session = Depends(get_db),
    _:         User    = Depends(require_admin),
):
    """
    Retourne les données brutes sans appel LLM — utile pour debug.
    """
    kpi_data     = analytics_service.get_kpi_improvement_data(db, module_id)
    mastery_data = analytics_service.get_time_to_mastery_data(db, module_id)
    dropoff_data = analytics_service.get_dropoff_data(db, module_id)

    if kpi_data.get("total_learners", 0) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Aucune donnée pour le module {module_id}."
        )

    return {
        "module_id": module_id,
        "kpi":       kpi_data,
        "mastery":   mastery_data,
        "dropoff":   dropoff_data,
    }