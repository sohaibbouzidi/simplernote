from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_ai_agent_key
from app.services.projects import ProjectService
from app.services.notes import NoteService
from app.services.tasks import TaskService
from app.services.ai_contexts import AiContextService
from app.schemas.notes import NoteCreateSchema, NoteUpdateSchema, NoteSchema
from app.schemas.tasks import TaskCreateSchema, TaskUpdateSchema, TaskSchema
from app.schemas.ai_context import AiContextSchema
from app.models.project import Project
from app.models.note import Note
from app.models.task import Task
from app.models.ai_context import AiContext

router = APIRouter()


class SearchResultItem(BaseModel):
    id: str
    type: str
    project_id: str
    title: str
    content: Optional[str] = None
    note_type: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class AgentAiContextCreateSchema(BaseModel):
    name: str = "default"
    content: str = ""


class AgentAiContextUpdateSchema(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None


class ImportSchema(BaseModel):
    pass


def _check_project_access(key_data: dict, project_id: str):
    key_project_id = key_data.get("project_id")
    if key_project_id and key_project_id != "None" and key_project_id != project_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="API key not authorized for this project")


def _require_permission(permissions: dict, perm: str):
    if not permissions.get(perm, False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Missing required permission: {perm}")


# ── Projects ──

@router.get("/projects")
def list_projects(
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    user_id = key_data["user_id"]
    key_project_id = key_data.get("project_id")
    if key_project_id and key_project_id != "None":
        project = ProjectService.get_project(db, key_project_id, user_id)
        return [project] if project else []
    return ProjectService.list_projects(db, user_id)


# ── Notes ──

@router.get("/projects/{project_id}/notes")
def list_notes(
    project_id: str,
    note_type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "read_notes")
    return NoteService.list_notes(db, key_data["user_id"], project_id, note_type=note_type, search=search)


@router.post("/projects/{project_id}/notes", response_model=NoteSchema, status_code=status.HTTP_201_CREATED)
def create_note(
    project_id: str,
    data: NoteCreateSchema,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "write_notes")
    return NoteService.create_note(db, key_data["user_id"], project_id, data)


@router.patch("/projects/{project_id}/notes/{note_id}", response_model=NoteSchema)
def update_note(
    project_id: str,
    note_id: str,
    data: NoteUpdateSchema,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "write_notes")
    note = NoteService.update_note(db, note_id, key_data["user_id"], data)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.delete("/projects/{project_id}/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    project_id: str,
    note_id: str,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "write_notes")
    deleted = NoteService.delete_note(db, note_id, key_data["user_id"], project_id=project_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")


@router.patch("/projects/{project_id}/notes/{note_id}/restore", response_model=NoteSchema)
def restore_note(
    project_id: str,
    note_id: str,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "write_notes")
    note = NoteService.restore_note(db, note_id, key_data["user_id"], project_id=project_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found or not deleted")
    return note


# ── Tasks ──

@router.get("/projects/{project_id}/tasks")
def list_tasks(
    project_id: str,
    status_param: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "read_tasks")
    return TaskService.list_tasks(db, key_data["user_id"], project_id, status=status_param)


@router.post("/projects/{project_id}/tasks", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
def create_task(
    project_id: str,
    data: TaskCreateSchema,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "write_tasks")
    return TaskService.create_task(db, key_data["user_id"], project_id, data)


@router.patch("/projects/{project_id}/tasks/{task_id}", response_model=TaskSchema)
def update_task(
    project_id: str,
    task_id: str,
    data: TaskUpdateSchema,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "write_tasks")
    task = TaskService.update_task(db, task_id, key_data["user_id"], data)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.delete("/projects/{project_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    project_id: str,
    task_id: str,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "write_tasks")
    deleted = TaskService.delete_task(db, task_id, key_data["user_id"], project_id=project_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.patch("/projects/{project_id}/tasks/{task_id}/restore", response_model=TaskSchema)
def restore_task(
    project_id: str,
    task_id: str,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "write_tasks")
    task = TaskService.restore_task(db, task_id, key_data["user_id"], project_id=project_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or not deleted")
    return task


# ── AI Context ──

# New endpoints: Multiple contexts per project

@router.get("/projects/{project_id}/contexts", response_model=List[AiContextSchema])
def list_project_contexts(
    project_id: str,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    """List all contexts for a project."""
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "read_ai_context")
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.created_by == key_data["user_id"],
        Project.deleted_at.is_(None)
    ).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return AiContextService.list_by_project(db, project_id, user_id=key_data["user_id"])


@router.post("/projects/{project_id}/contexts", response_model=AiContextSchema, status_code=status.HTTP_201_CREATED)
def create_project_context_new(
    project_id: str,
    data: AgentAiContextCreateSchema,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    """Create a new context for a project."""
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "write_ai_context")
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.created_by == key_data["user_id"],
        Project.deleted_at.is_(None)
    ).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    existing = AiContextService.get_by_project_and_name(db, project_id, data.name, user_id=key_data["user_id"])
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"A context named '{data.name}' already exists")
    
    from app.schemas.ai_context import AiContextCreateSchema
    return AiContextService.create(db, key_data["user_id"], project_id, AiContextCreateSchema(name=data.name, content=data.content))


@router.get("/projects/{project_id}/contexts/{context_id}", response_model=AiContextSchema)
def get_project_context_by_id(
    project_id: str,
    context_id: str,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    """Get a specific context by ID."""
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "read_ai_context")
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.created_by == key_data["user_id"],
        Project.deleted_at.is_(None)
    ).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    ctx = AiContextService.get_by_id(db, context_id, user_id=key_data["user_id"])
    if not ctx or str(ctx.project_id) != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Context not found")
    return ctx


@router.patch("/projects/{project_id}/contexts/{context_id}", response_model=AiContextSchema)
def update_project_context_by_id(
    project_id: str,
    context_id: str,
    data: AgentAiContextUpdateSchema,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    """Update a specific context."""
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "write_ai_context")
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.created_by == key_data["user_id"],
        Project.deleted_at.is_(None)
    ).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    ctx = AiContextService.get_by_id(db, context_id, user_id=key_data["user_id"])
    if not ctx or str(ctx.project_id) != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Context not found")
    
    if data.name and data.name != ctx.name:
        existing = AiContextService.get_by_project_and_name(db, project_id, data.name, user_id=key_data["user_id"])
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"A context named '{data.name}' already exists")
    
    from app.schemas.ai_context import AiContextUpdateSchema
    return AiContextService.update(db, ctx, AiContextUpdateSchema(name=data.name, content=data.content))


@router.delete("/projects/{project_id}/contexts/{context_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_context_by_id(
    project_id: str,
    context_id: str,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    """Delete a specific context."""
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "write_ai_context")
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.created_by == key_data["user_id"],
        Project.deleted_at.is_(None)
    ).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    ctx = AiContextService.get_by_id(db, context_id, user_id=key_data["user_id"])
    if not ctx or str(ctx.project_id) != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Context not found")
    
    AiContextService.delete(db, ctx)


# Deprecated endpoints: For backwards compatibility (single context)

@router.get("/projects/{project_id}/context", response_model=AiContextSchema)
def get_project_context(
    project_id: str,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    """DEPRECATED: Get the default context. Use /contexts instead."""
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "read_ai_context")
    ctx = AiContextService.get_by_project(db, project_id, user_id=key_data["user_id"])
    if not ctx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No AI context for this project")
    return ctx


@router.post("/projects/{project_id}/context", response_model=AiContextSchema, status_code=status.HTTP_201_CREATED)
def create_project_context(
    project_id: str,
    data: AgentAiContextCreateSchema,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    """DEPRECATED: Create the default context. Use /contexts instead."""
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "write_ai_context")
    existing = AiContextService.get_by_project(db, project_id, user_id=key_data["user_id"])
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="AI context already exists for this project")
    project = db.query(Project).filter(Project.id == project_id, Project.created_by == key_data["user_id"], Project.deleted_at.is_(None)).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    from app.schemas.ai_context import AiContextCreateSchema
    return AiContextService.create(db, key_data["user_id"], project_id, AiContextCreateSchema(name="default", content=data.content))


@router.put("/projects/{project_id}/context", response_model=AiContextSchema)
def set_project_context(
    project_id: str,
    data: AgentAiContextCreateSchema,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    """DEPRECATED: Update the default context. Use /contexts instead."""
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "write_ai_context")
    ctx = AiContextService.get_by_project(db, project_id, user_id=key_data["user_id"])
    if not ctx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No AI context for this project")
    from app.schemas.ai_context import AiContextUpdateSchema
    return AiContextService.update(db, ctx, AiContextUpdateSchema(content=data.content))


@router.post("/projects/{project_id}/context/import", response_model=AiContextSchema)
def import_project_context(
    project_id: str,
    data: ImportSchema,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    """DEPRECATED: Import notes/tasks to default context. Use /contexts instead."""
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "write_ai_context")
    project = db.query(Project).filter(Project.id == project_id, Project.created_by == key_data["user_id"], Project.deleted_at.is_(None)).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    user_id = key_data["user_id"]
    notes = db.query(Note).filter(Note.project_id == project_id, Note.created_by == user_id, Note.deleted_at.is_(None)).all()
    tasks = db.query(Task).filter(Task.project_id == project_id, Task.created_by == user_id, Task.deleted_at.is_(None)).all()
    lines = [f"# AI Context for Project: {project.name}"]
    if notes:
        lines.append(f"## Notes ({len(notes)})")
        for n in notes:
            lines.append(f"- [{n.note_type}] {n.title}")
            if n.summary:
                lines.append(f"  Summary: {n.summary}")
            if n.content:
                lines.append(f"  Content: {n.content[:500]}")
        lines.append("")
    if tasks:
        lines.append(f"## Tasks ({len(tasks)})")
        for t in tasks:
            lines.append(f"- [{t.status}/{t.priority}] {t.title}")
            if t.description:
                lines.append(f"  Description: {t.description}")
        lines.append("")
    content = "\n".join(lines)
    existing = AiContextService.get_by_project(db, project_id, user_id=key_data["user_id"])
    if existing:
        from app.schemas.ai_context import AiContextUpdateSchema
        return AiContextService.update(db, existing, AiContextUpdateSchema(content=content))
    from app.schemas.ai_context import AiContextCreateSchema
    return AiContextService.create(db, key_data["user_id"], project_id, AiContextCreateSchema(name="default", content=content))


@router.delete("/projects/{project_id}/context", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_context(
    project_id: str,
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    """DEPRECATED: Delete the default context. Use /contexts instead."""
    _check_project_access(key_data, project_id)
    _require_permission(key_data.get("permissions", {}), "write_ai_context")
    ctx = AiContextService.get_by_project(db, project_id, user_id=key_data["user_id"])
    if not ctx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No AI context for this project")
    AiContextService.delete(db, ctx)


# ── Search ──

@router.get("/search", response_model=List[SearchResultItem])
def search(
    query: str = Query(..., min_length=1),
    project_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    key_data: dict = Depends(get_ai_agent_key),
):
    _check_project_access(key_data, project_id) if project_id else None
    user_id = key_data["user_id"]
    permissions = key_data.get("permissions", {})
    results = []

    if permissions.get("read_notes", False):
        note_q = db.query(Note).filter(
            Note.created_by == user_id,
            Note.deleted_at.is_(None),
            Note.title.ilike(f"%{query}%") | Note.content.ilike(f"%{query}%") | Note.summary.ilike(f"%{query}%"),
        )
        if project_id:
            note_q = note_q.filter(Note.project_id == project_id)
        for n in note_q.all():
            results.append(SearchResultItem(
                id=str(n.id), type="note", project_id=str(n.project_id),
                title=n.title, content=n.content, note_type=n.note_type,
                created_at=n.created_at, updated_at=n.updated_at,
            ))

    if permissions.get("read_tasks", False):
        task_q = db.query(Task).filter(
            Task.created_by == user_id,
            Task.deleted_at.is_(None),
            Task.title.ilike(f"%{query}%") | Task.description.ilike(f"%{query}%"),
        )
        if project_id:
            task_q = task_q.filter(Task.project_id == project_id)
        for t in task_q.all():
            results.append(SearchResultItem(
                id=str(t.id), type="task", project_id=str(t.project_id),
                title=t.title, content=t.description, status=t.status, priority=t.priority,
                created_at=t.created_at,
            ))

    if permissions.get("read_ai_context", False):
        context_q = db.query(AiContext).filter(
            AiContext.created_by == user_id,
            AiContext.deleted_at.is_(None),
            AiContext.name.ilike(f"%{query}%") | AiContext.content.ilike(f"%{query}%"),
        )
        if project_id:
            context_q = context_q.filter(AiContext.project_id == project_id)
        for ctx in context_q.all():
            results.append(SearchResultItem(
                id=str(ctx.id), type="context", project_id=str(ctx.project_id),
                title=ctx.name, content=ctx.content,
                created_at=ctx.created_at, updated_at=ctx.updated_at,
            ))

    return results
