# app/api/v1/endpoints/performance.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.performance import PerformanceRequest, PerformanceResponse
from app.services import performance_service

router = APIRouter()


# ----------------------------------------------------------------
# POST /performance/analyze — Analyse par apprenant
# ----------------------------------------------------------------

@router.post("/analyze", response_model=PerformanceResponse)
def analyze_performance(
    req:          PerformanceRequest,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    user_id = current_user.id

    engagement = performance_service.get_engagement_data(db, user_id)
    kpi_data   = performance_service.get_kpi_data(db, user_id)
    mastery    = performance_service.get_mastery_data(db, user_id)
    dropoffs   = performance_service.get_dropoff_data(db, user_id)
    tutorials  = performance_service.get_tutorials_data(db, user_id)
    resources  = performance_service.get_resources_data(db, user_id)  # 🆕 V2

    insights = performance_service.generate_insights(
        engagement=engagement,
        mastery=mastery,
        dropoffs=dropoffs,
        kpi_data=kpi_data,
        tutorials=tutorials,
        resources=resources,   # 🆕 V2
        scope=req.scope
    )

    if "error" in insights:
        raise HTTPException(
            status_code=500,
            detail="Erreur génération insights"
        )

    performance_service.save_insights(db, user_id, insights, req.scope)
    performance_service.save_interventions(db, user_id, insights)

    return PerformanceResponse(
        user_id=user_id,
        scope=req.scope,
        summary=insights.get("summary", ""),
        engagement_rate=insights.get("engagement_rate", 0.0),
        kpi_before_avg=insights.get("kpi_before_avg"),
        kpi_after_avg=insights.get("kpi_after_avg"),
        execution_task_completion_rate=insights.get(
            "execution_task_completion_rate"
        ),
        main_drop_off_section=insights.get("main_drop_off_section"),
        top_blockers=insights.get("top_blockers", []),
        interventions=insights.get("interventions", []),
        trend=insights.get("trend", "stagnant"),
    )


# ----------------------------------------------------------------
# POST /performance/cohort/{module_id} — Analyse cohorte
# ----------------------------------------------------------------

@router.post("/cohort/{module_id}")
def analyze_cohort(
    module_id:    int,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    engagement = performance_service.get_cohort_engagement(db, module_id)
    dropoffs   = performance_service.get_cohort_dropoffs(db, module_id)
    insights   = performance_service.generate_cohort_insights(
        module_id, engagement, dropoffs
    )

    if "error" in insights:
        raise HTTPException(
            status_code=500,
            detail="Erreur génération insights cohorte"
        )

    return {
        "module_id":                      module_id,
        "summary":                        insights.get("summary", ""),
        "completion_rate":                insights.get("completion_rate", 0.0),
        "execution_task_completion_rate": insights.get(
            "execution_task_completion_rate", 0.0
        ),
        "main_drop_off_section":          insights.get("main_drop_off_section"),
        "top_blockers":                   insights.get("top_blockers", []),
        "interventions":                  insights.get("interventions", []),
        "trend":                          insights.get("trend", "stagnant"),
        "scope":                          "cohort"
    }


# ----------------------------------------------------------------
# GET /performance/insights/{user_id}
# ----------------------------------------------------------------

@router.get("/insights/{user_id}")
def get_insights_history(
    user_id:      int,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès refusé")

    from sqlalchemy import text
    rows = db.execute(text("""
        SELECT id, scope, insight_type, payload, generated_at
        FROM   performance_insights
        WHERE  user_id = :user_id
        ORDER  BY generated_at DESC
        LIMIT  10
    """), {"user_id": user_id}).fetchall()
    return [dict(r._mapping) for r in rows]


# ----------------------------------------------------------------
# GET /performance/interventions/{user_id}
# ----------------------------------------------------------------

@router.get("/interventions/{user_id}")
def get_interventions(
    user_id:      int,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès refusé")

    from sqlalchemy import text
    rows = db.execute(text("""
        SELECT
            i.id,
            i.type,
            i.section_type,
            i.target_content,
            i.reason,
            i.status,
            i.created_at,
            s.name AS skill_name
        FROM   interventions i
        LEFT JOIN skills s ON s.id = i.skill_id
        WHERE  i.user_id = :user_id
          AND  i.status  = 'pending'
        ORDER  BY i.created_at DESC
    """), {"user_id": user_id}).fetchall()
    return [dict(r._mapping) for r in rows]