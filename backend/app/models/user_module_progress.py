from __future__ import annotations

from datetime import datetime
from sqlalchemy import (
    ForeignKey, DateTime, String, Integer,
    Boolean, Text, JSON, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserModuleProgress(Base):
    __tablename__ = "user_module_progress"

    __table_args__ = (
        UniqueConstraint("user_id", "module_id",
                         name="uq_user_module_progress"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    module_id: Mapped[int] = mapped_column(
        ForeignKey("modules.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="not_started"
    )
    progress_percent: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )

    # ── Progression par section ──────────────────────────────
    # {
    #   "use_case":          "completed",
    #   "kpi":               "completed",
    #   "execution_content": "in_progress",
    #   "execution_task":    "not_started",
    #   "kpi_measurement":   "not_started",
    #   "progress_update":   "not_started"
    # }
    section_progress: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )
    section_opened_at: Mapped[dict | None] = mapped_column(
    JSON, nullable=True
)

    # ── Execution Task soumission ────────────────────────────
    execution_task_submitted: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True, default=False
    )
    execution_task_url: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    execution_task_difficulty: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    execution_task_submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )

    # ── KPI after — mesuré par l'apprenant ──────────────────
    kpi_after: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    # ── Timestamps ───────────────────────────────────────────
    started_at:   Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user   = relationship("User")
    module = relationship("Module")