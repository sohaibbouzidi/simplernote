"""add name column to ai_contexts for multiple contexts per project

Revision ID: 0013_add_name_ai
Revises: 0012_add_deleted_ai
Create Date: 2026-06-06 15:58:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = "0013_add_name_ai"
down_revision = "0012_add_deleted_ai"
branch_labels = None
depends_on = None


def upgrade():
    # Add name column as nullable first
    op.add_column("ai_contexts", sa.Column("name", sa.String(255), nullable=True))
    
    # Backfill existing contexts with "default" name
    connection = op.get_bind()
    connection.execute(sa.text("UPDATE ai_contexts SET name = 'default' WHERE name IS NULL"))
    
    # Make it NOT NULL
    op.alter_column("ai_contexts", "name", nullable=False)
    
    # Drop old unique constraint on project_id only
    op.drop_constraint("uq_ai_context_project", "ai_contexts", type_="unique")
    
    # Create new unique constraint on (project_id, name)
    op.create_unique_constraint(
        "uq_ai_context_project_name",
        "ai_contexts",
        ["project_id", "name"]
    )


def downgrade():
    # Drop new unique constraint
    op.drop_constraint("uq_ai_context_project_name", "ai_contexts", type_="unique")
    
    # Recreate old unique constraint
    op.create_unique_constraint(
        "uq_ai_context_project",
        "ai_contexts",
        ["project_id"]
    )
    
    # Drop name column
    op.drop_column("ai_contexts", "name")
