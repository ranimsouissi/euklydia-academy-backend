from __future__ import annotations
from datetime import datetime
from sqlalchemy import (
    String, Integer, DateTime, ForeignKey,
    Float, UniqueConstraint, Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class LearnerSkillMastery(Base):
    """
    Score de maîtrise par skill pour chaque apprenant.
    Mis à jour automatiquement après chaque activité évaluée.
    C'est ici que le moteur adaptatif lit pour décider le prochain module/leçon.
    """
    __tablename__ = "learner_skill_mastery"

    __table_args__ = (
        UniqueConstraint("user_id", "skill_id", name="uq_user_skill_mastery"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Score de maîtrise : 0.0 (débutant) → 1.0 (expert)
    # Calculé à partir des scores des activités + temps + tentatives
    mastery_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Niveau textuel dérivé du score
    # "beginner" (0-0.33), "intermediate" (0.34-0.66), "advanced" (0.67-1.0)
    mastery_level: Mapped[str] = mapped_column(
        String(20), default="beginner", nullable=False
    )

    # Confiance du modèle dans ce score (0.0-1.0)
    # Faible au début (peu de données), augmente avec les activités
    confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Nombre d'activités évaluées ayant contribué à ce score
    evidence_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Raison lisible de la dernière mise à jour
    # Ex : "Score 85% au quiz Unité 3 + 2 tentatives → maîtrise intermédiaire"
    last_update_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    last_updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relations
    user = relationship("User")
    skill = relationship("Skill")