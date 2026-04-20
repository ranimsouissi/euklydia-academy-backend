from __future__ import annotations

from datetime import datetime
from sqlalchemy import String, Text, Integer, Boolean, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(primary_key=True)

    title_en: Mapped[str] = mapped_column(String(255), nullable=False)
    title_fr: Mapped[str | None] = mapped_column(String(255), nullable=True)

    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_fr: Mapped[str | None] = mapped_column(Text, nullable=True)

    learning_objective_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    learning_objective_fr: Mapped[str | None] = mapped_column(Text, nullable=True)

    level: Mapped[str] = mapped_column(String(50), nullable=False)
    estimated_duration_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    format: Mapped[str | None] = mapped_column(String(50), nullable=True)

    role: Mapped[str | None] = mapped_column(String(100), nullable=True)
    journey_stage: Mapped[str | None] = mapped_column(String(50), nullable=True)
    display_order: Mapped[int | None] = mapped_column(Integer, nullable=True)

    expected_outcome_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    expected_outcome_fr: Mapped[str | None] = mapped_column(Text, nullable=True)

    key_concepts_en: Mapped[list | None] = mapped_column(JSON, nullable=True)
    key_concepts_fr: Mapped[list | None] = mapped_column(JSON, nullable=True)

    role_based_example_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    role_based_example_fr: Mapped[str | None] = mapped_column(Text, nullable=True)

    takeaway_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    takeaway_fr: Mapped[str | None] = mapped_column(Text, nullable=True)

    action_point_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    action_point_fr: Mapped[str | None] = mapped_column(Text, nullable=True)

    practical_application_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    practical_application_fr: Mapped[str | None] = mapped_column(Text, nullable=True)

    recommended_when_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    recommended_when_fr: Mapped[str | None] = mapped_column(Text, nullable=True)

    why_this_module_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    why_this_module_fr: Mapped[str | None] = mapped_column(Text, nullable=True)

    next_recommended_module_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    next_recommended_module_fr: Mapped[str | None] = mapped_column(String(255), nullable=True)

    infographic_en_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    infographic_fr_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    video_en_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    video_fr_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    quiz_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    comparison_tables_en: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    comparison_tables_fr: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    quiz_questions_en: Mapped[list | None] = mapped_column(JSON, nullable=True)
    quiz_questions_fr: Mapped[list | None] = mapped_column(JSON, nullable=True)

    prompt_examples_en: Mapped[list | None] = mapped_column(JSON, nullable=True)
    prompt_examples_fr: Mapped[list | None] = mapped_column(JSON, nullable=True)

    section_content_en: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    section_content_fr: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    practical_exercise_en: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    practical_exercise_fr: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # ── Relations existantes ──────────────────────────────────────────────────
    skill_links = relationship(
        "ModuleSkill",
        back_populates="module",
        cascade="all, delete-orphan",
    )

    # ── Nouvelle relation vers les unités ─────────────────────────────────────
    # Permet de naviguer : module.units → unit.lessons → lesson.activities
    # Nécessaire pour le moteur d'apprentissage adaptatif
    units = relationship(
        "Unit",
        back_populates="module",
        cascade="all, delete-orphan",
        order_by="Unit.order",
    )