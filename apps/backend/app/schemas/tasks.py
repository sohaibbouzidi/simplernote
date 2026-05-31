from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict


class TaskCreateSchema(BaseModel):
    parent_task_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    status: str = Field(default="todo", pattern="^(backlog|todo|in-progress|review|blocked|done|cancelled|deferred)$")
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    assigned_agent: Optional[str] = None
    meta: Dict[str, object] = Field(default_factory=dict)


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_agent: Optional[str] = None
    meta: Optional[Dict[str, object]] = None


class TaskSchema(BaseModel):
    id: UUID
    project_id: UUID
    parent_task_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    assigned_agent: Optional[str] = None
    meta: Dict[str, object]
    created_by: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
