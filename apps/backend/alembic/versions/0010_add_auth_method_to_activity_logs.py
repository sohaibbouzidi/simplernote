"""add auth_method column to activity_logs

Revision ID: 0010_add_auth_method
Revises: 0009_add_totp_fields
Create Date: 2026-05-30 16:30:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = "0010_add_auth_method"
down_revision = "0009_add_totp_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("activity_logs", sa.Column("auth_method", sa.String(16), server_default=sa.text("'user'"), nullable=False))


def downgrade() -> None:
    op.drop_column("activity_logs", "auth_method")
