"""make modules bilingual

Revision ID: 204949c97c44
Revises: fa9c0c1a2d20
Create Date: 2026-03-21 17:53:55.352568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '204949c97c44'
down_revision: Union[str, Sequence[str], None] = 'fa9c0c1a2d20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add columns (ALL nullable first)
    op.add_column('modules', sa.Column('title_en', sa.String(length=255), nullable=True))
    op.add_column('modules', sa.Column('title_fr', sa.String(length=255), nullable=True))

    op.add_column('modules', sa.Column('description_en', sa.Text(), nullable=True))
    op.add_column('modules', sa.Column('description_fr', sa.Text(), nullable=True))

    op.add_column('modules', sa.Column('learning_objective_en', sa.Text(), nullable=True))
    op.add_column('modules', sa.Column('learning_objective_fr', sa.Text(), nullable=True))

    op.add_column('modules', sa.Column('expected_outcome_en', sa.Text(), nullable=True))
    op.add_column('modules', sa.Column('expected_outcome_fr', sa.Text(), nullable=True))

    op.add_column('modules', sa.Column('key_concepts_en', sa.JSON(), nullable=True))
    op.add_column('modules', sa.Column('key_concepts_fr', sa.JSON(), nullable=True))

    op.add_column('modules', sa.Column('role_based_example_en', sa.Text(), nullable=True))
    op.add_column('modules', sa.Column('role_based_example_fr', sa.Text(), nullable=True))

    op.add_column('modules', sa.Column('takeaway_en', sa.Text(), nullable=True))
    op.add_column('modules', sa.Column('takeaway_fr', sa.Text(), nullable=True))

    op.add_column('modules', sa.Column('action_point_en', sa.Text(), nullable=True))
    op.add_column('modules', sa.Column('action_point_fr', sa.Text(), nullable=True))

    op.add_column('modules', sa.Column('practical_application_en', sa.Text(), nullable=True))
    op.add_column('modules', sa.Column('practical_application_fr', sa.Text(), nullable=True))

    op.add_column('modules', sa.Column('recommended_when_en', sa.Text(), nullable=True))
    op.add_column('modules', sa.Column('recommended_when_fr', sa.Text(), nullable=True))

    op.add_column('modules', sa.Column('why_this_module_en', sa.Text(), nullable=True))
    op.add_column('modules', sa.Column('why_this_module_fr', sa.Text(), nullable=True))

    op.add_column('modules', sa.Column('next_recommended_module_en', sa.String(length=255), nullable=True))
    op.add_column('modules', sa.Column('next_recommended_module_fr', sa.String(length=255), nullable=True))

    # 2. COPY DATA (VERY IMPORTANT)
    op.execute("""
        UPDATE modules SET
            title_en = title,
            description_en = description,
            learning_objective_en = learning_objective,
            expected_outcome_en = expected_outcome,
            key_concepts_en = key_concepts,
            role_based_example_en = role_based_example,
            takeaway_en = takeaway,
            action_point_en = action_point,
            practical_application_en = practical_application,
            recommended_when_en = recommended_when,
            why_this_module_en = why_this_module,
            next_recommended_module_en = next_recommended_module
    """)

    # 3. Make title_en NOT NULL (only required field)
    op.alter_column('modules', 'title_en', nullable=False)

    # 4. DROP OLD COLUMNS
    op.drop_column('modules', 'expected_outcome')
    op.drop_column('modules', 'description')
    op.drop_column('modules', 'key_concepts')
    op.drop_column('modules', 'action_point')
    op.drop_column('modules', 'learning_objective')
    op.drop_column('modules', 'practical_application')
    op.drop_column('modules', 'title')
    op.drop_column('modules', 'role_based_example')
    op.drop_column('modules', 'takeaway')
    op.drop_column('modules', 'why_this_module')
    op.drop_column('modules', 'recommended_when')
    op.drop_column('modules', 'next_recommended_module')