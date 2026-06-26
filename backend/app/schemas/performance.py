# app/schemas/performance.py
from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class PerformanceRequest(BaseModel):
    scope:     Literal["learner", "cohort"] = "learner"
    module_id: Optional[int] = None          # filtrer par module


class BlockerItem(BaseModel):
    rank:                 int
    skill:                str
    section_type:         Optional[str]   = None
    mastery_score:        float           = 0.0
    kpi_improvement_rate: Optional[float] = None   # ← corrigé
    drop_off_rate:        float           = 0.0
    evidence:             Optional[str]   = None
    impact:               Optional[str]   = None


class InterventionItem(BaseModel):
    skill:          str
    section_type:   Literal[
                      "use_case",
                      "kpi",
                      "execution_content",
                      "execution_task",
                      "kpi_measurement"
                    ]                         # section à revoir
    target_content: Optional[str] = None     # ex: "revoir Workflows Section 3"
    type:           Literal[
                      "review_section",
                      "watch_tutorial",
                      "read_resource",   # 🆕 V2
                      "coach_session"

                    ]                         # type d'intervention
    reason:         str
    priority:       Literal["high", "medium", "low"]


class PerformanceResponse(BaseModel):
    user_id:                         int
    scope:                           str
    summary:                         str
    engagement_rate:                 float
    kpi_before_avg:                  Optional[float] = None
    kpi_after_avg:                   Optional[float] = None
    execution_task_completion_rate:  Optional[float] = None
    main_drop_off_section:           Optional[str]   = None
    top_blockers:                    list[BlockerItem]
    interventions:                   list[InterventionItem]
    trend:                           Literal["improving", "stagnant", "declining"]