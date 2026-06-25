# app/schemas/learning_content.py
from __future__ import annotations
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel


# ─── Activity ────────────────────────────────────────────────────────────────

class ActivityRead(BaseModel):
    id:       int
    lesson_id: int
    type:     Literal[
                "template",
                "workflow",
                "tool",
                "tutorial",    # dette technique — à activer avant V2
                "video"
              ]
    title_fr: Optional[str] = None
    title_en: Optional[str] = None
    content_fr: Optional[dict] = None
    content_en: Optional[dict] = None
    order:    int
    is_required: bool
    is_active:   bool
    created_at:  datetime

    class Config:
        from_attributes = True


# ─── Lesson ──────────────────────────────────────────────────────────────────

class LessonRead(BaseModel):
    id:      int
    unit_id: int
    prerequisite_lesson_id: Optional[int] = None
    title_fr: str
    title_en: str
    description_fr: Optional[str] = None
    description_en: Optional[str] = None
    format:          str
    difficulty_level: int
    order:            int
    estimated_duration_min: Optional[int] = None
    video_url_fr: Optional[str] = None
    video_url_en: Optional[str] = None
    is_active:    bool
    created_at:   datetime
    activities:   list[ActivityRead] = []

    class Config:
        from_attributes = True


class LessonReadShort(BaseModel):
    """Version courte sans activities — pour les listes"""
    id:      int
    unit_id: int
    prerequisite_lesson_id: Optional[int] = None
    title_fr: str
    title_en: str
    format:          str
    difficulty_level: int
    order:            int
    estimated_duration_min: Optional[int] = None
    is_active: bool

    class Config:
        from_attributes = True


# ─── Unit ────────────────────────────────────────────────────────────────────

class UnitRead(BaseModel):
    id:        int
    module_id: int
    title_fr:  str
    title_en:  str
    description_fr: Optional[str] = None
    description_en: Optional[str] = None
    order:     int
    estimated_duration_min: Optional[int] = None

    # Section type — indispensable pour le Context Awareness Agent 1
    section_type: Optional[Literal[
                    "use_case",
                    "kpi",
                    "execution_content",
                    "execution_task",
                    "kpi_measurement",
                    "progress_update"
                  ]] = None

    # Timestamps pour time-to-mastery V2
    started_at:   Optional[datetime] = None
    completed_at: Optional[datetime] = None

    is_active:  bool
    created_at: datetime
    lessons:    list[LessonReadShort] = []

    class Config:
        from_attributes = True


class UnitReadWithLessons(BaseModel):
    """Version complète avec leçons et activités"""
    id:        int
    module_id: int
    title_fr:  str
    title_en:  str
    description_fr: Optional[str] = None
    description_en: Optional[str] = None
    order:     int
    estimated_duration_min: Optional[int] = None

    section_type: Optional[Literal[
                    "use_case",
                    "kpi",
                    "execution_content",
                    "execution_task",
                    "kpi_measurement",
                    "progress_update"
                  ]] = None

    started_at:   Optional[datetime] = None
    completed_at: Optional[datetime] = None

    is_active:  bool
    created_at: datetime
    lessons:    list[LessonRead] = []

    class Config:
        from_attributes = True