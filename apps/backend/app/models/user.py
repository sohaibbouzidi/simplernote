import uuid
from datetime import datetime
from app.utils.timezone import now
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(256), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    email_confirmed = Column(Boolean, default=False, nullable=False)
    totp_secret = Column(String(32), nullable=True)
    totp_enabled = Column(Boolean, default=False, nullable=False)
    role = Column(String(20), default="user", nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: now(), nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    profile_updated_at = Column(DateTime(timezone=True), nullable=True)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    picture = Column(Text, nullable=True)
