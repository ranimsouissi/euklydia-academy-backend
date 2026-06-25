"""add citation_ref to content_chunks

Revision ID: 85187baf525c
Revises: (base existante)
Create Date: 2026-05-17

Contexte:
    Ajoute la colonne citation_ref à content_chunks pour permettre
    au RAG de retourner des références lisibles dans le chat tuteur
    (ex: "L2.1", "M3.4", "U1.2").
"""

from alembic import op
import sqlalchemy as sa


revision = "85187baf525c"
down_revision = "b93a52046503"
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass  # content_chunks table no longer exists, skipping


def downgrade() -> None:
    pass