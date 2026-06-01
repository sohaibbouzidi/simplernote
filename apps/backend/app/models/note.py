import uuid
from datetime import datetime
from app.utils.timezone import now
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    title = Column(String(256), nullable=False)
    content = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    note_type = Column(String(50), nullable=False, default="documentation")
    tags = Column(JSONB, nullable=False, default=list)
    meta = Column('meta', JSONB, nullable=False, default=dict)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: now(), onupdate=lambda: now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    project = relationship("Project", back_populates="notes")
