"""enrich skills with use case fields

Revision ID: a1b2c3d4e5f6
Revises: 227a563576b8
Create Date: 2026-05-10 22:50:00.000000

Enrichit la table `skills` avec 5 colonnes business :
  - use_case_name      : Nom marketing du use case (ex: "Qualification automatisée des leads")
  - kpi_before         : KPI avant adoption IA (ex: "Faible taux de conversion (~10–15%)")
  - kpi_after          : KPI projeté après adoption IA (ex: "+25–40% de leads qualifiés")
  - blueprint_name     : Nom du Blueprint Euklydia (ex: "AI Lead Scoring Agent Blueprint")
  - display_order      : Ordre d'affichage des use cases par rôle

Conformément à la décision architecturale : 1 use case = 1 skill (relation 1:1),
donc les métadonnées business du use case vivent au niveau de la skill.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = "227a563576b8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("skills", sa.Column("use_case_name", sa.String(length=255), nullable=True))
    op.add_column("skills", sa.Column("kpi_before", sa.String(length=255), nullable=True))
    op.add_column("skills", sa.Column("kpi_after", sa.String(length=255), nullable=True))
    op.add_column("skills", sa.Column("blueprint_name", sa.String(length=255), nullable=True))
    op.add_column("skills", sa.Column("display_order", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("skills", "display_order")
    op.drop_column("skills", "blueprint_name")
    op.drop_column("skills", "kpi_after")
    op.drop_column("skills", "kpi_before")
    op.drop_column("skills", "use_case_name")
