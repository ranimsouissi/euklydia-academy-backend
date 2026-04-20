"""make diagnostic_session_id not null

Revision ID: cf8cc516c71e
Revises: 61f0af88f1c3
Create Date: 2026-03-02 16:02:52.627838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf8cc516c71e'
down_revision: Union[str, Sequence[str], None] = '61f0af88f1c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "user_responses",
        "diagnostic_session_id",
        nullable=False
    )

    op.alter_column(
        "user_skill_scores",
        "diagnostic_session_id",
        nullable=False
    )


def downgrade():
    op.alter_column(
        "user_responses",
        "diagnostic_session_id",
        nullable=True
    )

    op.alter_column(
        "user_skill_scores",
        "diagnostic_session_id",
        nullable=True
    )
