"""add role to users

Revision ID: 0002_add_role_to_users
Revises: 0001_initial
Create Date: 2026-05-29 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = "0002_add_role_to_users"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("role", sa.String(length=20), nullable=False, server_default="user"))


def downgrade() -> None:
    op.drop_column("users", "role")
