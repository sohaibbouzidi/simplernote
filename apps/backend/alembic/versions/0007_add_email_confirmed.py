"""add email_confirmed column to users

Revision ID: 0007_add_email_confirmed
Revises: 07472dba0963
Create Date: 2026-05-30 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = "0007_add_email_confirmed"
down_revision = "07472dba0963"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("email_confirmed", sa.Boolean(), server_default=sa.text("false"), nullable=False))


def downgrade() -> None:
    op.drop_column("users", "email_confirmed")
