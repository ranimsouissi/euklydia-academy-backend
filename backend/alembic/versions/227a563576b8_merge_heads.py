"""merge heads

Revision ID: 227a563576b8
Revises: a9fee27d1f77, c543d5b620e7
Create Date: 2026-04-20 18:11:13.165296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '227a563576b8'
down_revision: Union[str, Sequence[str], None] = ('a9fee27d1f77', 'c543d5b620e7')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
