"""change picture column to text

Revision ID: 0006_change_picture_type
Revises: 0005_add_profile_fields
Create Date: 2026-05-29 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = "0006_change_picture_type"
down_revision = "0005_add_profile_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "picture",
        existing_type=sa.String(length=1024),
        type_=sa.Text(),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "picture",
        existing_type=sa.Text(),
        type_=sa.String(length=1024),
        existing_nullable=True,
    )
