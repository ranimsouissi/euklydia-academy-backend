"""add google_id to users

Revision ID: 9ea5afece69c
Revises: dfec483c07e6
Create Date: 2026-04-17 08:46:10.641708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ea5afece69c'
down_revision: Union[str, Sequence[str], None] = 'dfec483c07e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("google_id", sa.String(length=255), nullable=True)
    )
    op.create_index("ix_users_google_id", "users", ["google_id"], unique=True)
    # Rendre password_hash nullable pour les comptes purement Google
    op.alter_column("users", "password_hash", nullable=True)


def downgrade():
    op.alter_column("users", "password_hash", nullable=False)
    op.drop_index("ix_users_google_id", table_name="users")
    op.drop_column("users", "google_id")