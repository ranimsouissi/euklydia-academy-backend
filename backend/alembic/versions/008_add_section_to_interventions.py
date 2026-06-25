# alembic/versions/008_add_section_to_interventions.py
"""add section_type + target_content to interventions

Revision ID: 008
Revises: 007
Create Date: 2026-05-28

NOTE: neutralisee - table 'interventions' inexistante (reliquat obsolete)
"""
from alembic import op
import sqlalchemy as sa

revision = "008"
down_revision = "007"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
