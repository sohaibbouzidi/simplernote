"""add last_login_at and profile_updated_at to users

Revision ID: 0008_add_last_login_etc
Revises: 0007_add_email_confirmed
Create Date: 2026-05-30 14:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = "0008_add_last_login_etc"
down_revision = "0007_add_email_confirmed"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("users", sa.Column("profile_updated_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "profile_updated_at")
    op.drop_column("users", "last_login_at")
