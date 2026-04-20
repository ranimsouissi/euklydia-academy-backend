from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel


# ─── Activity ────────────────────────────────────────────────────────────────

class ActivityRead(BaseModel):
    id: int
    lesson_id: int
    type: str
    title_fr: str | None = None
    title_en: str | None = None
    content_fr: dict | None = None
    content_en: dict | None = None
    order: int
    passing_score: int
    is_required: bool
    is_assessed: bool
    has_hints: bool
    hints_fr: list | None = None
    hints_en: list | None = None
    rubric_fr: dict | None = None
    rubric_en: dict | None = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Lesson ──────────────────────────────────────────────────────────────────

class LessonRead(BaseModel):
    id: int
    unit_id: int
    prerequisite_lesson_id: int | None = None
    title_fr: str
    title_en: str
    description_fr: str | None = None
    description_en: str | None = None
    format: str
    difficulty_level: int
    order: int
    estimated_duration_min: int | None = None
    video_url_fr: str | None = None
    video_url_en: str | None = None
    is_active: bool
    created_at: datetime
    activities: list[ActivityRead] = []

    class Config:
        from_attributes = True


class LessonReadShort(BaseModel):
    """Version courte sans activities — pour les listes"""
    id: int
    unit_id: int
    prerequisite_lesson_id: int | None = None
    title_fr: str
    title_en: str
    format: str
    difficulty_level: int
    order: int
    estimated_duration_min: int | None = None
    is_active: bool

    class Config:
        from_attributes = True


# ─── Unit ────────────────────────────────────────────────────────────────────

class UnitRead(BaseModel):
    id: int
    module_id: int
    title_fr: str
    title_en: str
    description_fr: str | None = None
    description_en: str | None = None
    order: int
    estimated_duration_min: int | None = None
    is_active: bool
    created_at: datetime
    lessons: list[LessonReadShort] = []

    class Config:
        from_attributes = True


class UnitReadWithLessons(BaseModel):
    """Version complète avec leçons et activités"""
    id: int
    module_id: int
    title_fr: str
    title_en: str
    description_fr: str | None = None
    description_en: str | None = None
    order: int
    estimated_duration_min: int | None = None
    is_active: bool
    created_at: datetime
    lessons: list[LessonRead] = []

    class Config:
        from_attributes = True