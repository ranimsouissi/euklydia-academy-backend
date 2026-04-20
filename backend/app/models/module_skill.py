from __future__ import annotations

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ModuleSkill(Base):
    __tablename__ = "module_skills"

    __table_args__ = (
        UniqueConstraint("module_id", "skill_id", name="uq_module_skill"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    module_id: Mapped[int] = mapped_column(
        ForeignKey("modules.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    module = relationship("Module", back_populates="skill_links")
    skill = relationship("Skill", back_populates="module_links")