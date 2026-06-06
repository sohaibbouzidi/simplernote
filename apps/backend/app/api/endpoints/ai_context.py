from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.auth import AuthService
from app.services.ai_contexts import AiContextService
from app.api.deps import PermissionChecker
from app.schemas.ai_context import AiContextCreateSchema, AiContextUpdateSchema, AiContextSchema
from app.models.user import User
from app.models.project import Project
from app.models.note import Note
from app.models.task import Task
from app.models.ai_context import AiContext

from app.core.rate_limit import rate_limit

router = APIRouter(dependencies=[Depends(rate_limit(30, 60))])
contexts_router = APIRouter(dependencies=[Depends(rate_limit(30, 60))])
search_router = APIRouter(dependencies=[Depends(rate_limit(30, 60))])


class SearchResultItem(BaseModel):
    id: str
    type: str = "note"
    project_id: str
    title: str
    content: Optional[str] = None
    note_type: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


# ===== NEW ENDPOINTS: Multiple contexts per project =====

@contexts_router.get("", response_model=List[AiContextSchema], dependencies=[Depends(PermissionChecker(["read_ai_context"]))])
def list_contexts(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    """List all contexts for a project."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.created_by == current_user.id,
        Project.deleted_at.is_(None)
    ).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    contexts = AiContextService.list_by_project(db, project_id, user_id=str(current_user.id))
    return contexts


@contexts_router.post("", response_model=AiContextSchema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionChecker(["write_ai_context"]))])
def create_context(
    project_id: str,
    data: AiContextCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    """Create a new context for a project."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.created_by == current_user.id,
        Project.deleted_at.is_(None)
    ).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    existing = AiContextService.get_by_project_and_name(db, project_id, data.name, user_id=str(current_user.id))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"A context named '{data.name}' already exists for this project")
    
    return AiContextService.create(db, str(current_user.id), project_id, data)


@contexts_router.get("/{context_id}", response_model=AiContextSchema, dependencies=[Depends(PermissionChecker(["read_ai_context"]))])
def get_context(
    project_id: str,
    context_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    """Get a specific context by ID."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.created_by == current_user.id,
        Project.deleted_at.is_(None)
    ).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    ctx = AiContextService.get_by_id(db, context_id, user_id=str(current_user.id))
    if not ctx or str(ctx.project_id) != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Context not found")
    return ctx


@contexts_router.patch("/{context_id}", response_model=AiContextSchema, dependencies=[Depends(PermissionChecker(["write_ai_context"]))])
def update_context(
    project_id: str,
    context_id: str,
    data: AiContextUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    """Update a specific context."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.created_by == current_user.id,
        Project.deleted_at.is_(None)
    ).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    ctx = AiContextService.get_by_id(db, context_id, user_id=str(current_user.id))
    if not ctx or str(ctx.project_id) != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Context not found")
    
    # Check if renaming to an existing context name
    if data.name and data.name != ctx.name:
        existing = AiContextService.get_by_project_and_name(db, project_id, data.name, user_id=str(current_user.id))
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"A context named '{data.name}' already exists for this project")
    
    return AiContextService.update(db, ctx, data)


@contexts_router.delete("/{context_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionChecker(["write_ai_context"]))])
def delete_context(
    project_id: str,
    context_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    """Delete (soft-delete) a specific context."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.created_by == current_user.id,
        Project.deleted_at.is_(None)
    ).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    ctx = AiContextService.get_by_id(db, context_id, user_id=str(current_user.id))
    if not ctx or str(ctx.project_id) != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Context not found")
    
    AiContextService.delete(db, ctx)


@contexts_router.post("/{context_id}/restore", response_model=AiContextSchema, dependencies=[Depends(PermissionChecker(["write_ai_context"]))])
def restore_context(
    project_id: str,
    context_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    """Restore a soft-deleted context."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.created_by == current_user.id,
        Project.deleted_at.is_(None)
    ).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    ctx = db.query(AiContext).filter(
        AiContext.id == context_id,
        AiContext.project_id == project_id,
        AiContext.created_by == current_user.id,
        AiContext.deleted_at.isnot(None)
    ).first()
    if not ctx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Context not found or not deleted")
    
    return AiContextService.restore(db, ctx)



# ===== DEPRECATED ENDPOINTS: For backwards compatibility (single context per project) =====

@router.get("", response_model=AiContextSchema, dependencies=[Depends(PermissionChecker(["read_ai_context"]))])
def get_ai_context(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    """DEPRECATED: Get the default context for a project. Use /contexts instead."""
    ctx = AiContextService.get_by_project(db, project_id, user_id=str(current_user.id))
    if not ctx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No AI context for this project")
    return ctx


@router.post("", response_model=AiContextSchema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionChecker(["write_ai_context"]))])
def create_ai_context(
    project_id: str,
    data: AiContextCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    """DEPRECATED: Create the default context for a project. Use /contexts instead."""
    existing = AiContextService.get_by_project(db, project_id, user_id=str(current_user.id))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="AI context already exists for this project")
    project = db.query(Project).filter(Project.id == project_id, Project.created_by == current_user.id, Project.deleted_at.is_(None)).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    # Create with "default" name for backwards compatibility
    create_data = AiContextCreateSchema(name="default", content=data.content)
    return AiContextService.create(db, str(current_user.id), project_id, create_data)


@router.patch("", response_model=AiContextSchema, dependencies=[Depends(PermissionChecker(["write_ai_context"]))])
def update_ai_context(
    project_id: str,
    data: AiContextUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    """DEPRECATED: Update the default context for a project. Use /contexts instead."""
    ctx = AiContextService.get_by_project(db, project_id, user_id=str(current_user.id))
    if not ctx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No AI context for this project")
    return AiContextService.update(db, ctx, data)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionChecker(["write_ai_context"]))])
def delete_ai_context(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    """DEPRECATED: Delete the default context for a project. Use /contexts instead."""
    ctx = AiContextService.get_by_project(db, project_id, user_id=str(current_user.id))
    if not ctx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No AI context for this project")
    AiContextService.delete(db, ctx)


@router.post("/import", response_model=AiContextSchema, dependencies=[Depends(PermissionChecker(["write_ai_context"]))])
def import_context(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    """Import notes and tasks into the default context."""
    project = db.query(Project).filter(Project.id == project_id, Project.created_by == current_user.id, Project.deleted_at.is_(None)).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    user_id = current_user.id
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

    existing = AiContextService.get_by_project(db, project_id, user_id=str(user_id))
    if existing:
        existing.content = content
        db.commit()
        db.refresh(existing)
        return existing
    
    create_data = AiContextCreateSchema(name="default", content=content)
    return AiContextService.create(db, str(user_id), project_id, create_data)


@search_router.get("/search", response_model=List[SearchResultItem])
def search_context(
    query: str = Query(..., min_length=1),
    project_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    user_id = current_user.id
    results = []

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

    return results
