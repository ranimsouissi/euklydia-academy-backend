from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, Text, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Types : "video", "quiz", "exercise", "prompt_practice",
    #         "case_study", "forum_discussion", "tutorial"
    type: Mapped[str] = mapped_column(String(50), nullable=False)

    title_fr: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Contenu principal selon le type :
    # quiz     → {"questions": [...], "passing_score": 7}
    # exercise → {"consigne": "...", "criteres": {...}, "livrable": "..."}
    # prompt   → {"prompt": "...", "usage": "...", "titre": "..."}
    # case     → {"contexte": "...", "dilemme": "...", "analyse": "..."}
    # video    → {"url_fr": "...", "url_en": "...", "duration_min": 10}
    content_fr: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    content_en: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Score minimum pour passer à la suite (0 si pas de score)
    passing_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Obligatoire pour avancer dans la leçon
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Évaluée par le moteur adaptatif (vs simple consultation)
    is_assessed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Indique si cette activité peut fournir des hints
    has_hints: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Hints progressifs : [{"level": 1, "text": "..."}, {"level": 2, "text": "..."}]
    hints_fr: Mapped[list | None] = mapped_column(JSON, nullable=True)
    hints_en: Mapped[list | None] = mapped_column(JSON, nullable=True)

    # Rubrique pour l'évaluation LLM des réponses ouvertes
    rubric_fr: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    rubric_en: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relations
    lesson = relationship("Lesson", back_populates="activities")
    logs = relationship(
        "LearnerActivityLog",
        back_populates="activity",
        cascade="all, delete-orphan",
    )