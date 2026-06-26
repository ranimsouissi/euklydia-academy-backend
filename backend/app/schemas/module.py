# app/schemas/module.py
from __future__ import annotations

from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel


class ExecutionTaskSubmission(BaseModel):
    """Soumission de l'Execution Task par l'apprenant"""
    url:        str                    # lien du livrable
    kpi_after:  str                    # KPI mesuré après
    difficulty: Optional[str] = None  # difficulté déclarée


class SectionProgress(BaseModel):
    """Progression par section du module"""
    use_case:          Literal["not_started", "in_progress", "completed"] = "not_started"
    kpi:               Literal["not_started", "in_progress", "completed"] = "not_started"
    execution_content: Literal["not_started", "in_progress", "completed"] = "not_started"
    execution_task:    Literal["not_started", "in_progress", "completed"] = "not_started"
    kpi_measurement:   Literal["not_started", "in_progress", "completed"] = "not_started"
    progress_update:   Literal["not_started", "in_progress", "completed"] = "not_started"


class ModuleRead(BaseModel):
    id: int

    title_en: str
    title_fr: Optional[str] = None

    description_en: Optional[str] = None
    description_fr: Optional[str] = None

    learning_objective_en: Optional[str] = None
    learning_objective_fr: Optional[str] = None

    level: str
    estimated_duration_min: Optional[int] = None
    format: Optional[str] = None

    role: Optional[str] = None
    journey_stage: Optional[str] = None
    display_order: Optional[int] = None

    expected_outcome_en: Optional[str] = None
    expected_outcome_fr: Optional[str] = None

    key_concepts_en: Optional[list[str]] = None
    key_concepts_fr: Optional[list[str]] = None

    role_based_example_en: Optional[str] = None
    role_based_example_fr: Optional[str] = None

    takeaway_en: Optional[str] = None
    takeaway_fr: Optional[str] = None

    action_point_en: Optional[str] = None
    action_point_fr: Optional[str] = None

    practical_application_en: Optional[str] = None
    practical_application_fr: Optional[str] = None

    recommended_when_en: Optional[str] = None
    recommended_when_fr: Optional[str] = None

    why_this_module_en: Optional[str] = None
    why_this_module_fr: Optional[str] = None

    next_recommended_module_en: Optional[str] = None
    next_recommended_module_fr: Optional[str] = None

    infographic_en_url: Optional[str] = None
    infographic_fr_url: Optional[str] = None
    video_en_url: Optional[str] = None
    video_fr_url: Optional[str] = None

    # ── KPI before / after ──────────────────────────────────
    kpi_before_en: Optional[str] = None    # KPI baseline (avant)
    kpi_before_fr: Optional[str] = None
    kpi_after_en:  Optional[str] = None    # KPI cible (après)
    kpi_after_fr:  Optional[str] = None

    # ── Skills mappés ────────────────────────────────────────
    skills_mapped: Optional[list[str]] = None

    # ── Execution Content ────────────────────────────────────
    templates_en:  Optional[list] = None
    templates_fr:  Optional[list] = None
    workflows_en:  Optional[list] = None
    workflows_fr:  Optional[list] = None
    tools_en:      Optional[list] = None
    tools_fr:      Optional[list] = None
    # tutorials : dette technique — à ajouter avant V2
    # tutorials_en: Optional[list] = None
    # tutorials_fr: Optional[list] = None
    references_fr:         Optional[list] = None

    # ── Execution Task ───────────────────────────────────────
    execution_task_en: Optional[dict] = None   # description de la tâche
    execution_task_fr: Optional[dict] = None
    execution_task_submission: Optional[ExecutionTaskSubmission] = None

    # ── KPI Measurement ──────────────────────────────────────
    kpi_measurement_en: Optional[dict] = None
    kpi_measurement_fr: Optional[dict] = None
    # ── Contenu pédagogique riche (depuis le model Module) ───
    practical_exercise_en: Optional[dict] = None
    practical_exercise_fr: Optional[dict] = None
    tutorials_fr:          Optional[list] = None
    progress_update_fr:    Optional[dict] = None

    # ── Mastery du skill principal (attaché par l'endpoint) ──
    skill_mastery: Optional[dict] = None

    # ── Alias pour compatibilité frontend ───────────────────
    module_status: Optional[str] = None
    # ── Progress ─────────────────────────────────────────────
    status:           Optional[str]            = "not_started"
    progress_percent: Optional[int]            = 0
    section_progress: Optional[SectionProgress] = None

    # ── Métadonnées ──────────────────────────────────────────
    comparison_tables_en: Optional[dict] = None
    comparison_tables_fr: Optional[dict] = None
    prompt_examples_en:   Optional[list] = None
    prompt_examples_fr:   Optional[list] = None
    section_content_en:   Optional[dict] = None
    section_content_fr:   Optional[dict] = None

    is_active:  bool
    created_at: datetime

    class Config:
        from_attributes = True
