"""widen citation_ref column on content_chunks

Revision ID: 2a0559a59fd7
Revises: f8a3b4ce3fa9
Create Date: 2026-06-30 19:03:11.248579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a0559a59fd7'
down_revision: Union[str, None] = 'f8a3b4ce3fa9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'content_chunks',
        'citation_ref',
        type_=sa.String(length=100),
        existing_type=sa.String(length=20),
    )


def downgrade() -> None:
    op.alter_column(
        'content_chunks',
        'citation_ref',
        type_=sa.String(length=20),
        existing_type=sa.String(length=100),
    )