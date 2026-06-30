"""add module_id and section_type to pain_points

Revision ID: f8a3b4ce3fa9
Revises: 012
Create Date: 2026-06-30 18:23:15.192847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8a3b4ce3fa9'
down_revision: Union[str, None] = '012'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('pain_points', sa.Column('module_id', sa.Integer(), nullable=True))
    op.add_column('pain_points', sa.Column('section_type', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('pain_points', 'section_type')
    op.drop_column('pain_points', 'module_id')