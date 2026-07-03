from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    ForeignKey, DateTime, String, Integer,
    Numeric, UniqueConstraint, Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserKpiMeasurement(Base):
    __tablename__ = "user_kpi_measurements"

    __table_args__ = (
        UniqueConstraint(
            "user_id", "module_id", "indicator",
            name="uq_user_module_indicator"
        ),
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

    # ── L'indicateur KPI ──────────────────────────────────────────
    # ex: "CAC moyen", "Volume de créas testées par mois"
    indicator: Mapped[str] = mapped_column(String(200), nullable=False)

    # ── Valeurs saisies par l'apprenant ──────────────────────────
    # baseline_value : saisie à l'étape KPI — Avant/Après (J0)
    # current_value  : saisie à l'étape KPI Measurement (valeur finale)
    baseline_value: Mapped[Decimal | None] = mapped_column(
        Numeric, nullable=True
    )
    current_value: Mapped[Decimal | None] = mapped_column(
        Numeric, nullable=True
    )

    # ── Métadonnées d'affichage ───────────────────────────────────
    # target_label : copié depuis le contenu du module, pour l'affichage
    # ex: "Réduction de 20 à 30 %", "Multiplié par 5 à 10"
    target_label: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ex: "TND", "%", "jours"
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # ── Timestamps ───────────────────────────────────────────────
    # measured_at : horodatage de la dernière saisie de current_value
    measured_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # ── Relations ────────────────────────────────────────────────
    user = relationship("User")
    module = relationship("Module")