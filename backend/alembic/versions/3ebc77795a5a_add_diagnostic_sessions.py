from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3ebc77795a5a"
down_revision: Union[str, Sequence[str], None] = "360d2bf8711a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "diagnostic_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("career_path_id", sa.Integer(), sa.ForeignKey("career_paths.id"), nullable=False),
        sa.Column("global_score_percent", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )

    op.add_column(
        "user_skill_scores",
        sa.Column("diagnostic_session_id", sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        "fk_user_skill_scores_diagnostic_session",
        "user_skill_scores",
        "diagnostic_sessions",
        ["diagnostic_session_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.create_index(
        "ix_diag_sessions_user_cp_created",
        "diagnostic_sessions",
        ["user_id", "career_path_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_diag_sessions_user_cp_created", table_name="diagnostic_sessions")

    op.drop_constraint(
        "fk_user_skill_scores_diagnostic_session",
        "user_skill_scores",
        type_="foreignkey",
    )

    op.drop_column("user_skill_scores", "diagnostic_session_id")

    op.drop_table("diagnostic_sessions")