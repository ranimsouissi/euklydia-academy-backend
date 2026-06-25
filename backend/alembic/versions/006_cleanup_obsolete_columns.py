# alembic/versions/006_cleanup_obsolete_columns.py
"""cleanup obsolete columns and tables

Revision ID: 006
Revises: 005
Create Date: 2026-05-28
"""
from alembic import op
import sqlalchemy as sa

revision = "006"
down_revision = "005"
branch_labels = None
depends_on = None


def upgrade():
    # modules - supprimer quiz
    op.drop_column("modules", "quiz_questions_en")
    op.drop_column("modules", "quiz_questions_fr")

    # activities - supprimer evaluation notee
    op.drop_column("activities", "passing_score")
    op.drop_column("activities", "is_assessed")
    op.drop_column("activities", "rubric_en")
    op.drop_column("activities", "rubric_fr")
    op.drop_column("activities", "hints_en")
    op.drop_column("activities", "hints_fr")

    # coaching_sessions - supprimer lesson_id
    op.drop_column("coaching_sessions", "lesson_id")

    # bloc events supprime : table inexistante (reliquat)


def downgrade():
    op.create_table(
        "user_responses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("question_id", sa.Integer(), nullable=True),
        sa.Column("answer", sa.Text(), nullable=True),
        sa.Column("is_correct", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )

    op.add_column("coaching_sessions",
        sa.Column("lesson_id", sa.Integer(), nullable=True))

    op.add_column("activities",
        sa.Column("passing_score", sa.Integer(), nullable=True))
    op.add_column("activities",
        sa.Column("is_assessed", sa.Boolean(), nullable=True))
    op.add_column("activities",
        sa.Column("rubric_en", sa.JSON(), nullable=True))
    op.add_column("activities",
        sa.Column("rubric_fr", sa.JSON(), nullable=True))
    op.add_column("activities",
        sa.Column("hints_en", sa.JSON(), nullable=True))
    op.add_column("activities",
        sa.Column("hints_fr", sa.JSON(), nullable=True))

    op.add_column("modules",
        sa.Column("quiz_questions_en", sa.JSON(), nullable=True))
    op.add_column("modules",
        sa.Column("quiz_questions_fr", sa.JSON(), nullable=True))
