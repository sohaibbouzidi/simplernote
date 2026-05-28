from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class NoteBaseSchema(BaseModel):
    project_id: str
    title: str
    content: Optional[str] = None
    summary: Optional[str] = None
    note_type: str = Field(default="documentation", pattern="^(memory|decision|research|issue|workflow|architecture|documentation)$")
    tags: List[str] = Field(default_factory=list)
    metadata_: Dict[str, object] = Field(default_factory=dict, alias="metadata")


class NoteCreateSchema(NoteBaseSchema):
    pass


class NoteUpdateSchema(BaseModel):
    title: Optional[str]
    content: Optional[str]
    summary: Optional[str]
    note_type: Optional[str]
    tags: Optional[List[str]]
    metadata_: Optional[Dict[str, object]]


class NoteSchema(NoteBaseSchema):
    id: str
    created_by: str
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
