from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class LearnerPathLog(Base):
    """
    Historique auditable des changements de parcours.
    Répond à la question : "Pourquoi le parcours a-t-il changé ?"
    Le LLM planner écrit ici chaque fois qu'il redirige un apprenant.
    """
    __tablename__ = "learner_path_logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Leçon depuis laquelle le changement a été décidé
    from_lesson_id: Mapped[int | None] = mapped_column(
        ForeignKey("lessons.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Leçon recommandée par le moteur adaptatif
    to_lesson_id: Mapped[int | None] = mapped_column(
        ForeignKey("lessons.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Déclencheur du changement :
    # "quiz_failed", "quiz_passed", "checkpoint", "difficulty_adjusted",
    # "prerequisite_completed", "manual_override"
    trigger: Mapped[str] = mapped_column(String(50), nullable=False)

    # Raison lisible générée par le LLM planner
    # Ex : "Parce que tu as eu du mal avec les prompts de prospection
    #       (score 45%, 3 tentatives) → on renforce avec un exercice guidé"
    reason_fr: Mapped[str | None] = mapped_column(Text, nullable=True)
    reason_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Contexte complet du moment de la décision (pour audit)
    # {"mastery_scores": {...}, "last_activity_score": 45, "attempts": 3}
    context_snapshot: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Source de la décision
    # "llm_planner", "rule_engine", "fallback_rules", "manual"
    decision_source: Mapped[str] = mapped_column(
        String(30), default="rule_engine", nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relations
    user = relationship("User")
    from_lesson = relationship("Lesson", foreign_keys=[from_lesson_id])
    to_lesson = relationship("Lesson", foreign_keys=[to_lesson_id])