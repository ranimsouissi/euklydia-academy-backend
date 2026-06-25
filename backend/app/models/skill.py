from __future__ import annotations

from sqlalchemy import String, Text, Integer, ForeignKey
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

    # ═══════════════════════════════════════════════════════════════════
    # ✅ NOUVEAU : Métadonnées du USE CASE (1 use case = 1 skill)
    # ═══════════════════════════════════════════════════════════════════
    # Nom marketing du use case, distinct du `name` technique de la skill.
    # Ex: skill.name = "Qualification IA des leads"
    #     skill.use_case_name = "Lead Qualification Automation"
    use_case_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # KPI business AVANT adoption IA — court, affichable en badge.
    # Ex: "Faible taux de conversion (~10–15%)"
    kpi_before: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # KPI business APRÈS adoption IA — court, affichable en badge.
    # Ex: "+25–40% de leads qualifiés"
    kpi_after: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Nom du Blueprint Euklydia associé à ce use case.
    # Ex: "AI Lead Scoring Agent Blueprint"
    blueprint_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Ordre d'affichage des use cases (1, 2, 3) au sein d'un même rôle.
    display_order: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # ═══════════════════════════════════════════════════════════════════
    # Relations existantes
    # ═══════════════════════════════════════════════════════════════════
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