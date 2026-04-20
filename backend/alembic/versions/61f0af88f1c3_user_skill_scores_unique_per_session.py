"""user_skill_scores unique per session

Revision ID: 61f0af88f1c3
Revises: 8c8efb6fd9a4
Create Date: 2026-03-02 15:47:48.360105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61f0af88f1c3'
down_revision: Union[str, Sequence[str], None] = '8c8efb6fd9a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop old unique constraint (user_id, skill_id)
    op.drop_constraint("uq_user_skill", "user_skill_scores", type_="unique")

    # New unique constraint: one score per skill per diagnostic session
    op.create_unique_constraint(
        "uq_session_skill",
        "user_skill_scores",
        ["diagnostic_session_id", "skill_id"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_session_skill", "user_skill_scores", type_="unique")

    op.create_unique_constraint(
        "uq_user_skill",
        "user_skill_scores",
        ["user_id", "skill_id"],
    )