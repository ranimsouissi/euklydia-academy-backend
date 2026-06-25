# alembic/versions/004_add_execution_task_to_progress.py
"""add section_progress + execution_task + kpi_after to user_module_progress

Revision ID: 004
Revises: 003
Create Date: 2026-05-28
"""
from alembic import op
import sqlalchemy as sa

revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    # Progression par section
    op.add_column('user_module_progress', sa.Column(
        'section_progress', sa.JSON(), nullable=True
    ))

    # Execution Task soumission
    op.add_column('user_module_progress', sa.Column(
        'execution_task_submitted',
        sa.Boolean(), nullable=True, server_default='false'
    ))
    op.add_column('user_module_progress', sa.Column(
        'execution_task_url', sa.Text(), nullable=True
    ))
    op.add_column('user_module_progress', sa.Column(
        'execution_task_difficulty', sa.String(100), nullable=True
    ))
    op.add_column('user_module_progress', sa.Column(
        'execution_task_submitted_at', sa.DateTime(), nullable=True
    ))

    # KPI after — mesuré par l'apprenant
    op.add_column('user_module_progress', sa.Column(
        'kpi_after', sa.Text(), nullable=True
    ))


def downgrade():
    op.drop_column('user_module_progress', 'section_progress')
    op.drop_column('user_module_progress', 'execution_task_submitted')
    op.drop_column('user_module_progress', 'execution_task_url')
    op.drop_column('user_module_progress', 'execution_task_difficulty')
    op.drop_column('user_module_progress', 'execution_task_submitted_at')
    op.drop_column('user_module_progress', 'kpi_after')