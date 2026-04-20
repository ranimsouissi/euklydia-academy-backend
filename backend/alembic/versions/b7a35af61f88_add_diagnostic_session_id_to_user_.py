"""add diagnostic_session_id to user_responses

Revision ID: b7a35af61f88
Revises: f4cb4bf5214e
Create Date: 2026-03-02 15:17:50.453591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7a35af61f88'
down_revision: Union[str, Sequence[str], None] = 'f4cb4bf5214e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
