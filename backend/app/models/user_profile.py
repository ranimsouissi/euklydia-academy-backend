from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    language: Mapped[str] = mapped_column(String(10), default="en")
    onboarding_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="profile")