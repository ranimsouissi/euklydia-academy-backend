"""add full_name to users"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '749c0953f98a'
down_revision: Union[str, Sequence[str], None] = 'cf8cc516c71e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('full_name', sa.String(length=120), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'full_name')