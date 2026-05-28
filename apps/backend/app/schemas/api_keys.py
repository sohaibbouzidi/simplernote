from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime


class APIKeyCreateSchema(BaseModel):
    name: str
    permissions: Dict[str, bool] = Field(default_factory=dict)
    expires_at: Optional[datetime] = None


class APIKeySchema(BaseModel):
    id: str
    name: str
    permissions: Dict[str, bool]
    last_used_at: Optional[datetime]
    expires_at: Optional[datetime]
    created_at: datetime
    plain_text_key: Optional[str] = None

    class Config:
        orm_mode = True
