"""add bilingual asset urls to modules

Revision ID: fa9c0c1a2d20
Revises: c088e3130e4f
Create Date: 2026-03-20 22:01:27.816552
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'fa9c0c1a2d20'
down_revision: Union[str, Sequence[str], None] = 'c088e3130e4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(table_name: str, column_name: str) -> bool:
    """Check if a column exists in a table."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade() -> None:
    """Upgrade schema."""
    # Ajout des colonnes bilingues (nouvelles)
    if not _column_exists('modules', 'infographic_en_url'):
        op.add_column('modules', sa.Column('infographic_en_url', sa.String(length=255), nullable=True))
    if not _column_exists('modules', 'infographic_fr_url'):
        op.add_column('modules', sa.Column('infographic_fr_url', sa.String(length=255), nullable=True))
    if not _column_exists('modules', 'video_en_url'):
        op.add_column('modules', sa.Column('video_en_url', sa.String(length=255), nullable=True))
    if not _column_exists('modules', 'video_fr_url'):
        op.add_column('modules', sa.Column('video_fr_url', sa.String(length=255), nullable=True))

    # quiz_url : créer si absent, sinon redimensionner
    if _column_exists('modules', 'quiz_url'):
        op.alter_column('modules', 'quiz_url',
                   existing_type=sa.VARCHAR(length=500),
                   type_=sa.String(length=255),
                   existing_nullable=True)
    else:
        op.add_column('modules', sa.Column('quiz_url', sa.String(length=255), nullable=True))

    # Suppression des anciennes colonnes (seulement si elles existent)
    if _column_exists('modules', 'infographic_url'):
        op.drop_column('modules', 'infographic_url')
    if _column_exists('modules', 'video_url'):
        op.drop_column('modules', 'video_url')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('modules', sa.Column('video_url', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.add_column('modules', sa.Column('infographic_url', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    if _column_exists('modules', 'quiz_url'):
        op.alter_column('modules', 'quiz_url',
                   existing_type=sa.String(length=255),
                   type_=sa.VARCHAR(length=500),
                   existing_nullable=True)
    op.drop_column('modules', 'video_fr_url')
    op.drop_column('modules', 'video_en_url')
    op.drop_column('modules', 'infographic_fr_url')
    op.drop_column('modules', 'infographic_en_url')