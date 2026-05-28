from pydantic import BaseModel
from typing import Optional


class ProjectBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreateSchema(ProjectBaseSchema):
    pass


class ProjectUpdateSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]


class ProjectSchema(ProjectBaseSchema):
    id: str
    created_by: str
    created_at: str

    class Config:
        orm_mode = True
