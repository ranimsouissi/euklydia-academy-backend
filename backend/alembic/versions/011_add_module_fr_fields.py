"""add tutorials_fr, references_fr, progress_update_fr to modules

Revision ID: 011
Revises: 010
Create Date: 2026-06-03

NOTE: colonnes presentes dans le modele mais jamais migrees (sync schema)
"""
from alembic import op
import sqlalchemy as sa

revision = "011"
down_revision = "010"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("modules", sa.Column("tutorials_fr", sa.JSON(), nullable=True))
    op.add_column("modules", sa.Column("references_fr", sa.JSON(), nullable=True))
    op.add_column("modules", sa.Column("progress_update_fr", sa.JSON(), nullable=True))


def downgrade():
    op.drop_column("modules", "progress_update_fr")
    op.drop_column("modules", "references_fr")
    op.drop_column("modules", "tutorials_fr")
