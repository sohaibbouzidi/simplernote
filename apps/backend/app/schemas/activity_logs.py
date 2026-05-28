from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class ActivityLogSchema(BaseModel):
    id: str
    project_id: Optional[str]
    user_id: Optional[str]
    action: str
    entity_type: str
    entity_id: Optional[str]
    payload: Optional[Dict[str, object]]
    created_at: datetime

    class Config:
        orm_mode = True
