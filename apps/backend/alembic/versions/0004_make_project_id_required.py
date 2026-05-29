"""make api_key project_id required

Revision ID: 0004
Revises: 0003
Create Date: 2026-05-29 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0004"
down_revision = "0003_add_project_id_to_api_keys"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("DELETE FROM api_keys WHERE project_id IS NULL")
    op.alter_column("api_keys", "project_id", nullable=False)


def downgrade() -> None:
    op.alter_column("api_keys", "project_id", nullable=True)
