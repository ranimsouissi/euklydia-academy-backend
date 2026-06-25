# alembic/versions/009_update_intervention_type_constraint.py
"""update intervention_type_valid constraint with new values

Revision ID: 009
Revises: 008
Create Date: 2026-05-28

NOTE: neutralisee - table 'interventions' inexistante (reliquat obsolete)
"""
from alembic import op

revision = "009"
down_revision = "008"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
