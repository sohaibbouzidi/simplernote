from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProjectBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreateSchema(ProjectBaseSchema):
    pass


class ProjectUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectSchema(ProjectBaseSchema):
    id: UUID
    created_by: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
