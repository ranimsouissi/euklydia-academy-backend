# alembic/versions/012_add_section_opened_at.py
"""add section_opened_at to user_module_progress

Revision ID: 012
Revises: 011
Create Date: 2026-06-29

NOTE: JSON stockant le timestamp d'ouverture de chaque section
{
  "use_case":          "2026-06-29T10:00:00",
  "kpi":               "2026-06-29T10:05:00",
  "execution_content": "2026-06-29T10:12:00",
  "execution_task":    "2026-06-29T10:20:00",
  "kpi_measurement":   "2026-06-29T10:25:00",
  "progress_update":   "2026-06-29T10:30:00"
}
Utilisé pour calculer le time-to-mastery par skill :
section_opened_at["use_case"] → execution_task_submitted_at
"""
from alembic import op
import sqlalchemy as sa

revision = "012"
down_revision = "011"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "user_module_progress",
        sa.Column("section_opened_at", sa.JSON(), nullable=True)
    )


def downgrade():
    op.drop_column("user_module_progress", "section_opened_at")