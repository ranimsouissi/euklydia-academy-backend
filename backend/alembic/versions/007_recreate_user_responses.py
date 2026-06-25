# alembic/versions/007_recreate_user_responses.py
"""recreate user_responses table for diagnostic
Revision ID: 007
Revises: 006
Create Date: 2026-05-28
"""
from alembic import op
import sqlalchemy as sa

revision = "007"
down_revision = "006"
branch_labels = None
depends_on = None


def upgrade():
    # Supprimer l'ancienne table (creee par init) avant de la recreer
    op.execute("DROP TABLE IF EXISTS user_responses CASCADE")

    op.create_table(
        "user_responses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(),
                  sa.ForeignKey("users.id", ondelete="CASCADE"),
                  nullable=False, index=True),
        sa.Column("diagnostic_session_id", sa.Integer(),
                  sa.ForeignKey("diagnostic_sessions.id", ondelete="CASCADE"),
                  nullable=True, index=True),
        sa.Column("question_id", sa.Integer(),
                  sa.ForeignKey("questions.id", ondelete="CASCADE"),
                  nullable=False),
        sa.Column("selected_option", sa.String(1), nullable=True),
        sa.Column("is_correct", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table("user_responses")
