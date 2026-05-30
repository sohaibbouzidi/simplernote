"""add totp_secret and totp_enabled to users

Revision ID: 0009_add_totp_fields
Revises: 0008_add_last_login_etc
Create Date: 2026-05-30 16:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = "0009_add_totp_fields"
down_revision = "0008_add_last_login_etc"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("totp_secret", sa.String(32), nullable=True))
    op.add_column("users", sa.Column("totp_enabled", sa.Boolean(), server_default=sa.text("false"), nullable=False))


def downgrade() -> None:
    op.drop_column("users", "totp_enabled")
    op.drop_column("users", "totp_secret")
