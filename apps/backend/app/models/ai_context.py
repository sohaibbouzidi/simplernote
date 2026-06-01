import uuid
from datetime import datetime
from app.utils.timezone import now
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class AiContext(Base):
    __tablename__ = "ai_contexts"
    __table_args__ = (UniqueConstraint("project_id", name="uq_ai_context_project"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False, default="")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: now(), onupdate=lambda: now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)
