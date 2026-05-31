"""add soft delete column to ai_contexts

Revision ID: 0012_add_deleted_ai
Revises: 0011_add_deleted
Create Date: 2026-05-31 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "0012_add_deleted_ai"
down_revision = "0011_add_deleted"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("ai_contexts", sa.Column("deleted_at", sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column("ai_contexts", "deleted_at")
