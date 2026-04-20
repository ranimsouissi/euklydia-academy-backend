from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class ModuleRead(BaseModel):
    id: int

    title_en: str
    title_fr: str | None = None

    description_en: str | None = None
    description_fr: str | None = None

    learning_objective_en: str | None = None
    learning_objective_fr: str | None = None

    level: str
    estimated_duration_min: int | None = None
    format: str | None = None

    role: str | None = None
    journey_stage: str | None = None
    display_order: int | None = None

    expected_outcome_en: str | None = None
    expected_outcome_fr: str | None = None

    key_concepts_en: list[str] | None = None
    key_concepts_fr: list[str] | None = None

    role_based_example_en: str | None = None
    role_based_example_fr: str | None = None

    takeaway_en: str | None = None
    takeaway_fr: str | None = None

    action_point_en: str | None = None
    action_point_fr: str | None = None

    practical_application_en: str | None = None
    practical_application_fr: str | None = None

    recommended_when_en: str | None = None
    recommended_when_fr: str | None = None

    why_this_module_en: str | None = None
    why_this_module_fr: str | None = None

    next_recommended_module_en: str | None = None
    next_recommended_module_fr: str | None = None

    infographic_en_url: str | None = None
    infographic_fr_url: str | None = None
    video_en_url: str | None = None
    video_fr_url: str | None = None
    quiz_url: str | None = None
    status: str | None = "not_started"
    progress_percent: int | None = 0
    comparison_tables_en: dict | None = None
    comparison_tables_fr: dict | None = None

    quiz_questions_en: list | None = None
    quiz_questions_fr: list | None = None

    prompt_examples_en: list | None = None
    prompt_examples_fr: list | None = None
    section_content_en: dict | None = None
    section_content_fr: dict | None = None
    practical_exercise_en: dict | None = None
    practical_exercise_fr: dict | None = None

    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True