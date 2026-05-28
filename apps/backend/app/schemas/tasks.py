from pydantic import BaseModel, Field
from typing import Optional, Dict


class TaskBaseSchema(BaseModel):
    project_id: str
    parent_task_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    status: str = Field(default="todo", pattern="^(todo|planning|research|coding|review|testing|done|blocked)$")
    priority: str = Field(default="medium", pattern="^(low|medium|high|critical)$")
    assigned_agent: Optional[str] = None
    metadata_: Dict[str, object] = Field(default_factory=dict, alias="metadata")


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    priority: Optional[str]
    assigned_agent: Optional[str]
    metadata_: Optional[Dict[str, object]]


class TaskSchema(TaskBaseSchema):
    id: str
    created_by: str
    created_at: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
