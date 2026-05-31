from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict


class NoteCreateSchema(BaseModel):
    title: str
    content: Optional[str] = None
    summary: Optional[str] = None
    note_type: str = Field(default="documentation", pattern="^(memory|decision|research|issue|workflow|architecture|documentation)$")
    tags: List[str] = Field(default_factory=list)
    meta: Dict[str, object] = Field(default_factory=dict)


class NoteUpdateSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    note_type: Optional[str] = None
    tags: Optional[List[str]] = None
    meta: Optional[Dict[str, object]] = None


class NoteSchema(BaseModel):
    id: UUID
    project_id: UUID
    title: str
    content: Optional[str] = None
    summary: Optional[str] = None
    note_type: str
    tags: List[str]
    meta: Dict[str, object]
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
