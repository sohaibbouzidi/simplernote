from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Optional
from datetime import datetime


class APIKeyCreateSchema(BaseModel):
    name: str
    permissions: Dict[str, bool] = Field(default_factory=dict)
    expires_at: Optional[datetime] = None


class APIKeySchema(BaseModel):
    id: UUID
    name: str
    permissions: Dict[str, bool]
    last_used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    created_at: datetime
    plain_text_key: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
