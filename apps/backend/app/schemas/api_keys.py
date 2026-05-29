from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Optional
from datetime import datetime


class APIKeyCreateSchema(BaseModel):
    name: str
    permissions: Dict[str, bool] = Field(default_factory=dict)
    expires_at: Optional[datetime] = None
    project_id: Optional[UUID] = None


class APIKeySchema(BaseModel):
    id: UUID
    name: str
    permissions: Dict[str, bool]
    project_id: Optional[UUID] = None
    project_name: Optional[str] = None
    last_used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    created_at: datetime
    plain_text_key: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
