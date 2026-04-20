"""add diagnostic_session_id to user_responses

Revision ID: 8c8efb6fd9a4
Revises: b7a35af61f88
Create Date: 2026-03-02 15:19:53.558705

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c8efb6fd9a4'
down_revision: Union[str, Sequence[str], None] = 'b7a35af61f88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1) Add diagnostic_session_id (nullable for now to avoid breaking existing rows)
    op.add_column(
        "user_responses",
        sa.Column("diagnostic_session_id", sa.Integer(), nullable=True),
    )

    # 2) FK to diagnostic_sessions
    op.create_foreign_key(
        "fk_user_responses_diagnostic_session",
        "user_responses",
        "diagnostic_sessions",
        ["diagnostic_session_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 3) Replace unique constraint: (user_id, question_id) -> (diagnostic_session_id, question_id)
    op.drop_constraint("uq_user_question", "user_responses", type_="unique")

    op.create_unique_constraint(
        "uq_session_question",
        "user_responses",
        ["diagnostic_session_id", "question_id"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_session_question", "user_responses", type_="unique")

    op.create_unique_constraint(
        "uq_user_question",
        "user_responses",
        ["user_id", "question_id"],
    )

    op.drop_constraint(
        "fk_user_responses_diagnostic_session",
        "user_responses",
        type_="foreignkey",
    )

    op.drop_column("user_responses", "diagnostic_session_id")