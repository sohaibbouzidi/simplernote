from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict
from datetime import datetime


class ActivityLogSchema(BaseModel):
    id: UUID
    project_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    action: str
    entity_type: str
    entity_id: Optional[UUID] = None
    payload: Optional[Dict[str, object]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
