from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class AiContextCreateSchema(BaseModel):
    content: str = ""


class AiContextUpdateSchema(BaseModel):
    content: Optional[str] = None


class AiContextSchema(BaseModel):
    id: UUID
    project_id: UUID
    content: str
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
