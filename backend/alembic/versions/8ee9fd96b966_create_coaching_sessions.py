"""create coaching_sessions table

Revision ID: 8ee9fd96b966
Revises: 85187baf525c
Create Date: 2026-05-17

Contexte:
    Crée la table coaching_sessions pour stocker les sessions de chat
    avec le tuteur IA. Différente de diagnostic_sessions (quiz) :
    ici on stocke l'historique complet de la conversation jsonb
    ainsi que le contexte de leçon actif.

    Règles de sécurité :
    - Aucune donnée sensible dans messages jsonb (pas de mots de passe,
      pas d'infos personnelles — juste le contenu pédagogique).
    - ended_at nullable : NULL = session encore active.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


revision = "8ee9fd96b966"
down_revision = "85187baf525c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "coaching_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "lesson_id",
            sa.Integer(),
            sa.ForeignKey("lessons.id", ondelete="SET NULL"),
            nullable=True,
            comment="Leçon active au moment de la session (nullable si supprimée)",
        ),
        sa.Column(
            "module_id",
            sa.Integer(),
            sa.ForeignKey("modules.id", ondelete="SET NULL"),
            nullable=True,
            comment="Module actif — utile pour filtrer par rôle AI",
        ),
        sa.Column(
            "messages",
            JSONB,
            nullable=False,
            server_default="[]",
            comment="Historique complet [{role, content, citations, timestamp}]",
        ),
        sa.Column(
            "lang",
            sa.String(5),
            nullable=False,
            server_default="fr",
            comment="Langue de la session : fr | en",
        ),
        sa.Column(
            "started_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "ended_at",
            sa.DateTime(),
            nullable=True,
            comment="NULL = session encore active",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_coaching_sessions_user_id",
        "coaching_sessions",
        ["user_id"],
    )
    op.create_index(
        "ix_coaching_sessions_lesson_id",
        "coaching_sessions",
        ["lesson_id"],
    )
    op.create_index(
        "ix_coaching_sessions_started_at",
        "coaching_sessions",
        ["started_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_coaching_sessions_started_at", table_name="coaching_sessions")
    op.drop_index("ix_coaching_sessions_lesson_id", table_name="coaching_sessions")
    op.drop_index("ix_coaching_sessions_user_id", table_name="coaching_sessions")
    op.drop_table("coaching_sessions")
