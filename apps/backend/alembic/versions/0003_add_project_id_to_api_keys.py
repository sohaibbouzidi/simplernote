"""add project_id to api_keys

Revision ID: 0003_add_project_id_to_api_keys
Revises: 0002_add_role_to_users
Create Date: 2026-05-29 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0003_add_project_id_to_api_keys"
down_revision = "0002_add_role_to_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("api_keys", sa.Column("project_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("projects.id"), nullable=True))


def downgrade() -> None:
    op.drop_column("api_keys", "project_id")
