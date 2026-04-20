"""make password_hash nullable

Revision ID: f4cb4bf5214e
Revises: 3ebc77795a5a
Create Date: 2026-03-02 11:18:38.645507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4cb4bf5214e'
down_revision: Union[str, Sequence[str], None] = '3ebc77795a5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("users", "password_hash", existing_type=sa.String(length=255), nullable=True)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
