"""add ai_contexts table

Revision ID: 07472dba0963
Revises: 0006_change_picture_type
Create Date: 2026-05-30 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "07472dba0963"
down_revision = "0006_change_picture_type"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "ai_contexts",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("project_id", UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_by", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("project_id", name="uq_ai_context_project"),
    )


def downgrade():
    op.drop_table("ai_contexts")
