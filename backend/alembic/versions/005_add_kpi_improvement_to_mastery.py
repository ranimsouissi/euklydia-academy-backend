# alembic/versions/005_add_kpi_improvement_to_mastery.py
"""add module_id + kpi_improvement_rate to learner_skill_mastery

Revision ID: 005
Revises: 004
Create Date: 2026-05-28
"""
from alembic import op
import sqlalchemy as sa

revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade():
    # Module source de la mise à jour
    op.add_column('learner_skill_mastery', sa.Column(
        'module_id', sa.Integer(),
        sa.ForeignKey('modules.id', ondelete='SET NULL'),
        nullable=True
    ))
    op.create_index(
        'ix_learner_skill_mastery_module_id',
        'learner_skill_mastery', ['module_id']
    )

    # KPI improvement rate — source mastery principale
    op.add_column('learner_skill_mastery', sa.Column(
        'kpi_improvement_rate', sa.Float(), nullable=True
    ))

    # Correction valeur default mastery_level
    op.alter_column(
        'learner_skill_mastery', 'mastery_level',
        server_default='novice'
    )


def downgrade():
    op.drop_index(
        'ix_learner_skill_mastery_module_id',
        table_name='learner_skill_mastery'
    )
    op.drop_column('learner_skill_mastery', 'module_id')
    op.drop_column('learner_skill_mastery', 'kpi_improvement_rate')
    op.alter_column(
        'learner_skill_mastery', 'mastery_level',
        server_default='beginner'
    )