"""add user_kpi_measurements table

Revision ID: 636befc74984
Revises: c7d15f659093
Create Date: 2026-07-03 12:48:05.836395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '636befc74984'
down_revision: Union[str, None] = 'c7d15f659093'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_kpi_measurements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('module_id', sa.Integer(), nullable=False),
        sa.Column('indicator', sa.String(length=200), nullable=False),
        sa.Column('baseline_value', sa.Numeric(), nullable=True),
        sa.Column('current_value', sa.Numeric(), nullable=True),
        sa.Column('target_label', sa.Text(), nullable=True),
        sa.Column('unit', sa.String(length=50), nullable=True),
        sa.Column('measured_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            'user_id', 'module_id', 'indicator',
            name='uq_user_module_indicator'
        )
    )
    op.create_index(
        op.f('ix_user_kpi_measurements_module_id'),
        'user_kpi_measurements', ['module_id'], unique=False
    )
    op.create_index(
        op.f('ix_user_kpi_measurements_user_id'),
        'user_kpi_measurements', ['user_id'], unique=False
    )


def downgrade() -> None:
    op.drop_index(
        op.f('ix_user_kpi_measurements_module_id'),
        table_name='user_kpi_measurements'
    )
    op.drop_index(
        op.f('ix_user_kpi_measurements_user_id'),
        table_name='user_kpi_measurements'
    )
    op.drop_table('user_kpi_measurements')