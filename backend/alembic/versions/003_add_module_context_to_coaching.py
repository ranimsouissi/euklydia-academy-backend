from alembic import op
import sqlalchemy as sa

revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

def upgrade():
    # ── coaching_sessions ──────────────────────────────
    op.add_column('coaching_sessions', sa.Column(
        'section_type', sa.String(50), nullable=True
    ))
    op.add_column('coaching_sessions', sa.Column(
        'kpi_baseline', sa.String(500), nullable=True
    ))
    op.add_column('coaching_sessions', sa.Column(
        'diagnostic_score', sa.Integer(), nullable=True
    ))
    op.alter_column('coaching_sessions', 'lesson_id', nullable=True)
    # ── bloc 'events' supprimé : table inexistante (reliquat) ──

def downgrade():
    op.drop_column('coaching_sessions', 'section_type')
    op.drop_column('coaching_sessions', 'kpi_baseline')
    op.drop_column('coaching_sessions', 'diagnostic_score')
    op.alter_column('coaching_sessions', 'lesson_id', nullable=False)