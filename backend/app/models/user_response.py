from datetime import datetime
from sqlalchemy import ForeignKey, Integer, DateTime, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class UserResponse(Base):
    __tablename__ = "user_responses"
    __table_args__ = (
        UniqueConstraint("assessment_session_id", "question_id", name="uq_session_question"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    assessment_session_id: Mapped[int] = mapped_column(
        ForeignKey("assessment_sessions.id", ondelete="CASCADE"),
        nullable=True,
    )

    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)
    selected_option: Mapped[str] = mapped_column(String(1), nullable=False)  # "A","B","C","D"
    is_correct: Mapped[bool] = mapped_column(nullable=False, default=False)  # calculé auto
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    question = relationship("Question", back_populates="responses")