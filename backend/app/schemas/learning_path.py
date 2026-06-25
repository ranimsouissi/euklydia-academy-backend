# app/schemas/learning_path.py
from __future__ import annotations
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel


class SkillCovered(BaseModel):
    skill_id:   int
    skill_name: str
    score:      int
    level:      str
    priority:   str


class SectionProgressItem(BaseModel):
    """Progression détaillée par section du module"""
    section_type: Literal[
                    "use_case",
                    "kpi",
                    "execution_content",
                    "execution_task",
                    "kpi_measurement",
                    "progress_update"
                  ]
    status:       Literal["not_started", "in_progress", "completed"] = "not_started"
    started_at:   Optional[datetime] = None   # timestamp pour time-to-mastery V2
    completed_at: Optional[datetime] = None


class ExecutionTaskSubmissionOut(BaseModel):
    """Soumission de l'Execution Task — lecture"""
    submitted:  bool              = False
    url:        Optional[str]     = None   # lien du livrable
    kpi_after:  Optional[str]     = None   # KPI mesuré après
    difficulty: Optional[str]     = None   # difficulté déclarée
    submitted_at: Optional[datetime] = None


class LearningPathItemOut(BaseModel):
    # ── Module ──────────────────────────────────────────────
    module_id:              int
    module_title:           str
    module_title_fr:        Optional[str] = None
    module_description:     Optional[str] = None
    module_description_fr:  Optional[str] = None
    module_level:           str
    journey_stage:          Optional[str] = None
    estimated_duration_min: Optional[int] = None
    format:                 Optional[str] = None

    # Champs enrichis pour le frontend
    key_concepts_en:             Optional[list[str]] = None
    key_concepts_fr:             Optional[list[str]] = None
    why_this_module_en:          Optional[str] = None
    why_this_module_fr:          Optional[str] = None
    takeaway_en:                 Optional[str] = None
    takeaway_fr:                 Optional[str] = None
    next_recommended_module_en:  Optional[str] = None
    next_recommended_module_fr:  Optional[str] = None

    # ── Skill principal ──────────────────────────────────────
    skill_id:   int
    skill_name: str
    score:      int
    level:      str
    priority:   str
    status:     str = "not_started"

    # ── Use Case + KPI ───────────────────────────────────────
    use_case_name:           Optional[str] = None
    kpi_before:              Optional[str] = None   # KPI baseline
    kpi_after:               Optional[str] = None   # KPI cible
    blueprint_name:          Optional[str] = None
    use_case_display_order:  Optional[int] = None

    # ── Progression globale ──────────────────────────────────
    progress_percent: Optional[float] = None         # 0-100

    # ── Progression par section ──────────────────────────────
    section_progress: list[SectionProgressItem] = []

    # ── Execution Task soumission ────────────────────────────
    execution_task: Optional[ExecutionTaskSubmissionOut] = None

    # ── Mastery ──────────────────────────────────────────────
    mastery_last_updated: Optional[datetime] = None  # pour time-to-mastery V2

    # ── Skills couverts ──────────────────────────────────────
    covered_skills: list[SkillCovered] = []


class RoadmapSummaryOut(BaseModel):
    profile:        str
    profile_fr:     str
    role_fr:        Optional[str] = None
    role_en:        Optional[str] = None
    description_en: str
    description_fr: str
    cta_en:         Optional[str] = None
    cta_fr:         Optional[str] = None
    recommended_focus_en: Optional[str] = None
    recommended_focus_fr: Optional[str] = None
    global_score:   float
    high_count:     int = 0
    medium_count:   int = 0
    low_count:      int = 0

    # ── Adaptive Engine ──────────────────────────────────────
    next_recommended_module_id: Optional[int]  = None  # module suivant
    stagnation_detected:        bool           = False  # détection stagnation
    time_available_per_week:    Optional[int]  = None  # heures/semaine


class LearningPathOut(BaseModel):
    items:              list[LearningPathItemOut]
    modules_completed:  int   = 0
    modules_total:      int   = 0
    roadmap_progress:   int   = 0
    total_duration_min: int   = 0
    summary:            Optional[RoadmapSummaryOut] = None