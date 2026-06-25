from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, Text, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Unit(Base):
    __tablename__ = "units"

    id: Mapped[int] = mapped_column(primary_key=True)

    module_id: Mapped[int] = mapped_column(
        ForeignKey("modules.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title_fr: Mapped[str] = mapped_column(String(255), nullable=False)
    title_en: Mapped[str] = mapped_column(String(255), nullable=False)

    description_fr: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    order:                  Mapped[int]      = mapped_column(Integer, nullable=False)
    estimated_duration_min: Mapped[int|None] = mapped_column(Integer, nullable=True)

    # ── Section type — Context Awareness Agent 1 ─────────────
    # Valeurs : "use_case" | "kpi" | "execution_content"
    #           "execution_task" | "kpi_measurement" | "progress_update"
    section_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True, index=True
    )

    # ── Timestamps par section — time-to-mastery V2 ──────────
    started_at:   Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    is_active:  Mapped[bool]     = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relations
    module = relationship("Module", back_populates="units")
    lessons = relationship(
        "Lesson",
        back_populates="unit",
        cascade="all, delete-orphan",
        order_by="Lesson.order",
    )