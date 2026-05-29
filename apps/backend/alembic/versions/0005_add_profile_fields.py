"""add profile fields to users

Revision ID: 0005_add_profile_fields
Revises: 0004
Create Date: 2026-05-29 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = "0005_add_profile_fields"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("first_name", sa.String(length=128), nullable=True))
    op.add_column("users", sa.Column("last_name", sa.String(length=128), nullable=True))
    op.add_column("users", sa.Column("country", sa.String(length=100), nullable=True))
    op.add_column("users", sa.Column("city", sa.String(length=100), nullable=True))
    op.add_column("users", sa.Column("picture", sa.String(length=1024), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "picture")
    op.drop_column("users", "city")
    op.drop_column("users", "country")
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
