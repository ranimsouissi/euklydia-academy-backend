from __future__ import annotations

from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Owner
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("User")  # optional back_populates later

    # Type/versioning
    report_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g. "type_a"
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="type_a_v1")

    # Snapshot of assessment at generation time
    global_score_percent: Mapped[float] = mapped_column(Float, nullable=False)
    maturity_level: Mapped[str] = mapped_column(String(30), nullable=False)

    # Storage info (file path or later url)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)