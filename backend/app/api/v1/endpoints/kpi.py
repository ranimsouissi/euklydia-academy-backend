# app/api/v1/endpoints/kpi.py
"""
KPI Measurement Endpoints
=========================
POST /kpi/baseline
    → Enregistre la baseline (valeur Avant) pour chaque indicateur du module

POST /kpi/measurement
    → Met à jour la valeur finale (valeur Après) pour un indicateur

GET  /kpi/{module_id}
    → Retourne toutes les mesures KPI de l'apprenant pour un module donné
"""
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.user_kpi_measurement import UserKpiMeasurement

router = APIRouter()


# ── Schémas Pydantic ──────────────────────────────────────────────────────────

class KpiIndicatorIn(BaseModel):
    indicator:    str
    baseline_value: float
    target_label: Optional[str] = None
    unit:         Optional[str] = None


class KpiBaselineRequest(BaseModel):
    module_id:   int
    indicators:  List[KpiIndicatorIn]


class KpiMeasurementRequest(BaseModel):
    module_id:     int
    indicator:     str
    current_value: float


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/baseline", status_code=200)
def save_baseline(
    payload:      KpiBaselineRequest,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    """
    Enregistre ou met à jour la baseline (valeur Avant / J0)
    pour chaque indicateur du module.
    Appelé quand l'apprenant valide l'étape KPI.
    """
    saved = []
    for item in payload.indicators:
        existing = (
            db.query(UserKpiMeasurement)
            .filter_by(
                user_id=current_user.id,
                module_id=payload.module_id,
                indicator=item.indicator,
            )
            .first()
        )
        if existing:
            existing.baseline_value = item.baseline_value
            existing.target_label   = item.target_label
            existing.unit           = item.unit
            existing.updated_at     = datetime.utcnow()
        else:
            db.add(UserKpiMeasurement(
                user_id        = current_user.id,
                module_id      = payload.module_id,
                indicator      = item.indicator,
                baseline_value = item.baseline_value,
                target_label   = item.target_label,
                unit           = item.unit,
            ))
        saved.append(item.indicator)

    db.commit()
    return {"saved": saved, "module_id": payload.module_id}


@router.post("/measurement", status_code=200)
def save_measurement(
    payload:      KpiMeasurementRequest,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    """
    Met à jour la valeur finale (valeur Après) pour un indicateur.
    Appelé quand l'apprenant saisit sa mesure à l'étape KPI Measurement.
    """
    existing = (
        db.query(UserKpiMeasurement)
        .filter_by(
            user_id=current_user.id,
            module_id=payload.module_id,
            indicator=payload.indicator,
        )
        .first()
    )
    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Baseline non trouvée pour cet indicateur. Saisissez d'abord la baseline à l'étape KPI."
        )

    existing.current_value = payload.current_value
    existing.measured_at   = datetime.utcnow()
    existing.updated_at    = datetime.utcnow()
    db.commit()

    return {
        "indicator":     existing.indicator,
        "baseline_value": float(existing.baseline_value) if existing.baseline_value else None,
        "current_value": float(existing.current_value),
        "target_label":  existing.target_label,
        "measured_at":   existing.measured_at.isoformat(),
    }


@router.get("/{module_id}", status_code=200)
def get_kpi_measurements(
    module_id:    int,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    """
    Retourne toutes les mesures KPI de l'apprenant pour un module.
    Utilisé par le dashboard Avant/Après et les agents.
    """
    rows = (
        db.query(UserKpiMeasurement)
        .filter_by(user_id=current_user.id, module_id=module_id)
        .all()
    )
    return [
        {
            "indicator":      r.indicator,
            "baseline_value": float(r.baseline_value) if r.baseline_value else None,
            "current_value":  float(r.current_value)  if r.current_value  else None,
            "target_label":   r.target_label,
            "unit":           r.unit,
            "measured_at":    r.measured_at.isoformat() if r.measured_at else None,
        }
        for r in rows
    ]