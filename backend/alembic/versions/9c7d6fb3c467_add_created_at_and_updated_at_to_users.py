"""add created_at and updated_at to users

Revision ID: 9c7d6fb3c467
Revises: 749c0953f98a
Create Date: 2026-03-09 20:20:09.101205
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9c7d6fb3c467"
down_revision: Union[str, Sequence[str], None] = "749c0953f98a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )
    op.add_column(
        "users",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )

    op.alter_column("users", "created_at", server_default=None)
    op.alter_column("users", "updated_at", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "updated_at")
    op.drop_column("users", "created_at")