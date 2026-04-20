from __future__ import annotations

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ✅ Renommé : role_id → career_path_id (clarté sémantique)
    career_path_id: Mapped[int | None] = mapped_column(
        ForeignKey("career_paths.id"), nullable=True
    )

    # ✅ Renommé : role → career_path
    career_path = relationship("CareerPath", back_populates="skills")

    questions = relationship(
        "Question",
        back_populates="skill",
        cascade="all, delete-orphan",
    )

    module_links = relationship(
        "ModuleSkill",
        back_populates="skill",
        cascade="all, delete-orphan",
    )