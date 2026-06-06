from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class AiContextCreateSchema(BaseModel):
    name: str
    content: str = ""


class AiContextUpdateSchema(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None


class AiContextSchema(BaseModel):
    id: UUID
    project_id: UUID
    name: str
    content: str
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
