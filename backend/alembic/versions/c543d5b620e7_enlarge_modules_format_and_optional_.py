"""enlarge modules format and optional fields

Revision ID: c543d5b620e7
Revises: fa9c0c1a2d20
Create Date: 2026-04-20 19:08:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c543d5b620e7'
down_revision: Union[str, Sequence[str], None] = 'fa9c0c1a2d20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Enlarge format column and other optional string fields."""
    # format : 50 → 255 (les descriptions de format peuvent être longues)
    op.alter_column('modules', 'format',
                    existing_type=sa.VARCHAR(length=50),
                    type_=sa.String(length=255),
                    existing_nullable=True)

    # journey_stage : 50 → 100 (marge de sécurité)
    op.alter_column('modules', 'journey_stage',
                    existing_type=sa.VARCHAR(length=50),
                    type_=sa.String(length=100),
                    existing_nullable=True)

    # level : 50 → 100 (marge de sécurité)
    op.alter_column('modules', 'level',
                    existing_type=sa.VARCHAR(length=50),
                    type_=sa.String(length=100),
                    existing_nullable=False)


def downgrade() -> None:
    """Revert to original sizes."""
    op.alter_column('modules', 'level',
                    existing_type=sa.String(length=100),
                    type_=sa.VARCHAR(length=50),
                    existing_nullable=False)

    op.alter_column('modules', 'journey_stage',
                    existing_type=sa.String(length=100),
                    type_=sa.VARCHAR(length=50),
                    existing_nullable=True)

    op.alter_column('modules', 'format',
                    existing_type=sa.String(length=255),
                    type_=sa.VARCHAR(length=50),
                    existing_nullable=True)