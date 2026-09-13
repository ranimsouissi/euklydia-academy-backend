"""add_user_recommendations

Revision ID: c7d15f659093
Revises: 2a0559a59fd7
Create Date: 2026-06-30 23:32:43.110146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c7d15f659093'
down_revision: Union[str, None] = '2a0559a59fd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'user_recommendations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('module_id', sa.Integer(), nullable=False),
        sa.Column('section_review', sa.String(), nullable=True),
        sa.Column('stagnation_alert', sa.Boolean(), default=False),
        sa.Column('recommendation_summary', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'ix_user_recommendations_user_module',
        'user_recommendations',
        ['user_id', 'module_id']
    )

def downgrade():
    op.drop_index('ix_user_recommendations_user_module')
    op.drop_table('user_recommendations')