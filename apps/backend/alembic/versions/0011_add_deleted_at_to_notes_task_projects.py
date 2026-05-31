"""add soft delete columns to notes, tasks, and projects

Revision ID: 0011_add_deleted
Revises: 0010_add_auth_method
Create Date: 2026-05-30 12:10:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "0011_add_deleted"
down_revision = "0010_add_auth_method"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("notes", sa.Column("deleted_at", sa.DateTime(), nullable=True))
    op.add_column("tasks", sa.Column("deleted_at", sa.DateTime(), nullable=True))
    op.add_column("projects", sa.Column("deleted_at", sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column("notes", "deleted_at")
    op.drop_column("tasks", "deleted_at")
    op.drop_column("projects", "deleted_at")
