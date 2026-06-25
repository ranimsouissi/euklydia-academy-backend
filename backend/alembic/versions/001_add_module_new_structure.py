# alembic/versions/001_add_module_new_structure.py
"""add kpi + execution_task + kpi_measurement to modules

Revision ID: 001
Revises:
Create Date: 2026-05-28
"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = '64cccc35f164'
branch_labels = None
depends_on = None


def upgrade():
    # KPI before / after
    op.add_column('modules', sa.Column('kpi_before_en', sa.Text(), nullable=True))
    op.add_column('modules', sa.Column('kpi_before_fr', sa.Text(), nullable=True))
    op.add_column('modules', sa.Column('kpi_after_en',  sa.Text(), nullable=True))
    op.add_column('modules', sa.Column('kpi_after_fr',  sa.Text(), nullable=True))

    # Execution Task
    op.add_column('modules', sa.Column('execution_task_en', sa.JSON(), nullable=True))
    op.add_column('modules', sa.Column('execution_task_fr', sa.JSON(), nullable=True))

    # KPI Measurement
    op.add_column('modules', sa.Column('kpi_measurement_en', sa.JSON(), nullable=True))
    op.add_column('modules', sa.Column('kpi_measurement_fr', sa.JSON(), nullable=True))


def downgrade():
    op.drop_column('modules', 'kpi_before_en')
    op.drop_column('modules', 'kpi_before_fr')
    op.drop_column('modules', 'kpi_after_en')
    op.drop_column('modules', 'kpi_after_fr')
    op.drop_column('modules', 'execution_task_en')
    op.drop_column('modules', 'execution_task_fr')
    op.drop_column('modules', 'kpi_measurement_en')
    op.drop_column('modules', 'kpi_measurement_fr')