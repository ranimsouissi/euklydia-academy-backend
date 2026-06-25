# alembic/versions/010_add_time_available_to_profile.py
"""add time_available_per_week to user_profiles

Revision ID: 010
Revises: 009
Create Date: 2026-05-28
"""
from alembic import op
import sqlalchemy as sa

revision = '010'
down_revision = '009'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user_profiles',
        sa.Column('time_available_per_week', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('user_profiles', 'time_available_per_week')