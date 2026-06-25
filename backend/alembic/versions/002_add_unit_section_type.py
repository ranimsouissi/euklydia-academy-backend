# alembic/versions/002_add_unit_section_type.py
"""add section_type + timestamps to units

Revision ID: 002
Revises: 001
Create Date: 2026-05-28
"""
from alembic import op
import sqlalchemy as sa

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Section type — Context Awareness Agent 1
    op.add_column('units', sa.Column(
        'section_type', sa.String(50), nullable=True
    ))
    op.create_index('ix_units_section_type', 'units', ['section_type'])

    # Timestamps — time-to-mastery V2
    op.add_column('units', sa.Column('started_at',   sa.DateTime(), nullable=True))
    op.add_column('units', sa.Column('completed_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_index('ix_units_section_type', table_name='units')
    op.drop_column('units', 'section_type')
    op.drop_column('units', 'started_at')
    op.drop_column('units', 'completed_at')