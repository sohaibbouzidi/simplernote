from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AiContextCreateSchema(BaseModel):
    project_id: str
    content: str = ""


class AiContextUpdateSchema(BaseModel):
    content: Optional[str] = None


class AiContextSchema(BaseModel):
    id: str
    project_id: str
    content: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
