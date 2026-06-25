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
    Mis à jour automatiquement après chaque Execution Task soumise
    et KPI Measurement complété.

    Sources V1 :
    - kpi_improvement_rate  → amélioration KPI before/after
    - execution_task soumis → signal de complétion
    - difficulty déclarée   → signal de blocage

    Mastery levels :
    0.0  - 0.39 → novice
    0.4  - 0.59 → beginner
    0.6  - 0.74 → practitioner
    0.75 - 0.89 → advanced
    0.9  - 1.0  → expert
    """
    __tablename__ = "learner_skill_mastery"

    __table_args__ = (
        UniqueConstraint("user_id", "skill_id",
                         name="uq_user_skill_mastery"),
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

    # ── Module source de la dernière mise à jour ─────────────
    module_id: Mapped[int | None] = mapped_column(
        ForeignKey("modules.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # ── Score de maîtrise : 0.0 → 1.0 ───────────────────────
    mastery_score: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )

    # ── Niveau textuel dérivé du score ───────────────────────
    # "novice" | "beginner" | "practitioner" | "advanced" | "expert"
    mastery_level: Mapped[str] = mapped_column(
        String(20), default="novice", nullable=False
    )

    # ── Taux d'amélioration KPI before/after ─────────────────
    # 0.0 = pas d'amélioration, 1.0 = amélioration maximale
    kpi_improvement_rate: Mapped[float | None] = mapped_column(
        Float, nullable=True, default=0.0
    )

    # ── Confiance du modèle dans ce score ────────────────────
    confidence: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )

    # ── Nombre de modules ayant contribué à ce score ─────────
    evidence_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )

    # ── Raison lisible de la dernière mise à jour ────────────
    # Ex : "execution_task_submitted + kpi_improved"
    #      "execution_task_submitted + kpi_stagnant"
    #      "execution_task_submitted + high_difficulty_declared"
    last_update_reason: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    last_updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relations
    user   = relationship("User")
    skill  = relationship("Skill")
    module = relationship("Module")