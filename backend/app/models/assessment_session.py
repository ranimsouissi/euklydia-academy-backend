from __future__ import annotations

from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    career_path_id: Mapped[int] = mapped_column(ForeignKey("career_paths.id"), nullable=False)

    global_score_percent: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # reverse relationship
    skill_scores = relationship("UserSkillScore", back_populates="assessment_session")