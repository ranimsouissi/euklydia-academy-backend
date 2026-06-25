from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, Text, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)

    unit_id: Mapped[int] = mapped_column(
        ForeignKey("units.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Prérequis : leçon qui doit être complétée avant celle-ci
    prerequisite_lesson_id: Mapped[int | None] = mapped_column(
        ForeignKey("lessons.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    title_fr: Mapped[str] = mapped_column(String(255), nullable=False)
    title_en: Mapped[str] = mapped_column(String(255), nullable=False)

    description_fr: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Format : "video", "quiz", "exercise", "tutorial", "case_study", "forum"
    format: Mapped[str] = mapped_column(String(50), nullable=False)

    # Niveau de difficulté 1 (très facile) → 5 (très difficile)
    # Utilisé par le LLM planner pour ajuster le parcours
    difficulty_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    order: Mapped[int] = mapped_column(Integer, nullable=False)
    estimated_duration_min: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Script vidéo ou contenu textuel principal
    video_script_fr: Mapped[str | None] = mapped_column(Text, nullable=True)
    video_script_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relations
    unit = relationship("Unit", back_populates="lessons")
    prerequisite = relationship("Lesson", remote_side="Lesson.id", foreign_keys=[prerequisite_lesson_id])
    activities = relationship(
        "Activity",
        back_populates="lesson",
        cascade="all, delete-orphan",
        order_by="Activity.order",
    )
    learner_logs = relationship("LearnerActivityLog", back_populates="lesson")