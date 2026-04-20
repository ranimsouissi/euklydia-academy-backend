from __future__ import annotations
from datetime import datetime
from sqlalchemy import (
    String, Integer, Boolean, DateTime, ForeignKey,
    JSON, Float, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class LearnerActivityLog(Base):
    """
    Enregistre chaque interaction d'un apprenant avec une activité.
    C'est la table principale que lit le moteur adaptatif pour :
    - mettre à jour la maîtrise par skill
    - décider la prochaine leçon recommandée
    - générer le feedback LLM
    """
    __tablename__ = "learner_activity_logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Dénormalisé pour requêtes rapides sans jointures
    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Score obtenu (0-100)
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Nombre de tentatives sur cette activité
    attempts: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Temps passé en secondes — signal clé pour le mastery model
    time_on_task_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Nombre de hints demandés — signal de difficulté
    hints_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Statut : "started", "completed", "passed", "failed", "skipped"
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="started")

    # Réponse brute de l'apprenant (pour évaluation LLM)
    learner_response: Mapped[str | None] = mapped_column(String(5000), nullable=True)

    # Feedback généré par le LLM (rubric-based)
    llm_feedback_fr: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    llm_feedback_en: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    # Résultats détaillés du quiz
    # {"answers": [{"q_id": 1, "answer": "B", "correct": true}, ...]}
    detailed_results: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    started_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relations
    user = relationship("User")
    activity = relationship("Activity", back_populates="logs")
    lesson = relationship("Lesson", back_populates="learner_logs")