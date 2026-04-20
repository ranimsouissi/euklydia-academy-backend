"""rename skills.role_id to career_path_id

Revision ID: a9fee27d1f77
Revises: 9ea5afece69c
Create Date: 2026-04-17 10:56:24.020656

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9fee27d1f77'
down_revision: Union[str, Sequence[str], None] = '9ea5afece69c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Supprimer l'ancienne FK nommée 'skills_role_id_fkey'
    op.drop_constraint('skills_role_id_fkey', 'skills', type_='foreignkey')

    # 2. Renommer la colonne role_id → career_path_id
    op.alter_column('skills', 'role_id', new_column_name='career_path_id')

    # 3. Recréer la FK avec un nom propre
    op.create_foreign_key(
        'skills_career_path_id_fkey',
        'skills',
        'career_paths',
        ['career_path_id'],
        ['id']
    )


def downgrade():
    # Rollback : on refait l'inverse
    op.drop_constraint('skills_career_path_id_fkey', 'skills', type_='foreignkey')
    op.alter_column('skills', 'career_path_id', new_column_name='role_id')
    op.create_foreign_key(
        'skills_role_id_fkey',
        'skills',
        'career_paths',
        ['role_id'],
        ['id']
    )