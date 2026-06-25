"""drop_reports_table_and_remove_brochure_feature

Revision ID: b93a52046503
Revises: a1b2c3d4e5f6
Create Date: 2026-05-12 13:04:15.696663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b93a52046503"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Drop the reports table — brochure/executive_report feature removed."""
    op.drop_table("reports")


def downgrade() -> None:
    """Recreate the reports table (rollback to original schema)."""
    op.create_table(
        "reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("report_type", sa.String(length=50), nullable=False),
        sa.Column("version", sa.String(length=50), nullable=False),
        sa.Column("global_score_percent", sa.Float(), nullable=False),
        sa.Column("maturity_level", sa.String(length=30), nullable=False),
        sa.Column("file_path", sa.String(length=500), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
