"""create pain_points table

Revision ID: 64cccc35f164
Revises: 8ee9fd96b966
Create Date: 2026-05-17

Contexte:
    Crée la table pain_points pour la collecte stratégique des
    problèmes business détectés silencieusement par le tuteur IA
    pendant les sessions de coaching.

    Règles de confidentialité :
    - summary : résumé du problème business UNIQUEMENT — pas de nom,
      pas d'email, pas d'info personnelle dans ce champ.
    - user_id conservé pour permettre à l'équipe Euklydia de
      recontacter l'utilisateur si pertinent (opt-in future).
    - category : tag automatique généré par le LLM (ex: "prospection",
      "automatisation", "reporting", "gestion projet").
    - role : copié depuis career_paths au moment de la capture pour
      éviter les jointures et garder l'historique stable.

    Accès :
    - Réservé à l'équipe interne Euklydia (pas de RLS user standard).
    - À protéger via une policy Postgres séparée si Supabase utilisé.
"""

from alembic import op
import sqlalchemy as sa


revision = "64cccc35f164"
down_revision = "8ee9fd96b966"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "pain_points",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
            comment="Conservé pour recontact futur — jamais affiché en clair",
        ),
        sa.Column(
            "session_id",
            sa.Integer(),
            sa.ForeignKey("coaching_sessions.id", ondelete="SET NULL"),
            nullable=True,
            comment="Session d'où provient le pain point",
        ),
        sa.Column(
            "summary",
            sa.Text(),
            nullable=False,
            comment="Résumé du problème business détecté — aucune donnée personnelle",
        ),
        sa.Column(
            "category",
            sa.String(100),
            nullable=True,
            comment="Tag LLM: prospection | automatisation | reporting | gestion_projet | autre",
        ),
        sa.Column(
            "role",
            sa.String(50),
            nullable=True,
            comment="Rôle AI de l'utilisateur au moment de la capture: sales | marketing | design | pm",
        ),
        sa.Column(
            "confidence_score",
            sa.Float(),
            nullable=True,
            comment="Score 0-1 : confiance du LLM dans la détection du pain point",
        ),
        sa.Column(
            "raw_message",
            sa.Text(),
            nullable=True,
            comment="Message brut source (optionnel, pour validation interne Euklydia)",
        ),
        sa.Column(
            "captured_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_pain_points_user_id",
        "pain_points",
        ["user_id"],
    )
    op.create_index(
        "ix_pain_points_category",
        "pain_points",
        ["category"],
    )
    op.create_index(
        "ix_pain_points_role",
        "pain_points",
        ["role"],
    )
    op.create_index(
        "ix_pain_points_captured_at",
        "pain_points",
        ["captured_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_pain_points_captured_at", table_name="pain_points")
    op.drop_index("ix_pain_points_role", table_name="pain_points")
    op.drop_index("ix_pain_points_category", table_name="pain_points")
    op.drop_index("ix_pain_points_user_id", table_name="pain_points")
    op.drop_table("pain_points")
