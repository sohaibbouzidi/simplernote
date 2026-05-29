from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict


class NoteBaseSchema(BaseModel):
    project_id: UUID
    title: str
    content: Optional[str] = None
    summary: Optional[str] = None
    note_type: str = Field(default="documentation", pattern="^(memory|decision|research|issue|workflow|architecture|documentation)$")
    tags: List[str] = Field(default_factory=list)
    meta: Dict[str, object] = Field(default_factory=dict)


class NoteCreateSchema(NoteBaseSchema):
    pass


class NoteUpdateSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    note_type: Optional[str] = None
    tags: Optional[List[str]] = None
    meta: Optional[Dict[str, object]] = None


class NoteSchema(NoteBaseSchema):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
