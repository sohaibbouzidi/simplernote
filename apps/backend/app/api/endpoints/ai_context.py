from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.session import get_db
from app.api.deps import PermissionChecker
from app.services.auth import AuthService
from app.schemas.notes import NoteSchema
from app.schemas.tasks import TaskSchema
from app.models.note import Note
from app.models.task import Task

from app.core.rate_limit import rate_limit

router = APIRouter(dependencies=[Depends(rate_limit(30, 60))])


def _serialize_notes(notes: List[Note]) -> List[dict]:
    return [
        {
            "id": str(n.id),
            "project_id": str(n.project_id),
            "title": n.title,
            "content": n.content,
            "summary": n.summary,
            "note_type": n.note_type,
            "tags": n.tags or [],
            "meta": n.meta or {},
            "created_by": str(n.created_by),
            "created_at": n.created_at.isoformat() if n.created_at else None,
            "updated_at": n.updated_at.isoformat() if n.updated_at else None,
        }
        for n in notes
    ]


def _serialize_tasks(tasks: List[Task]) -> List[dict]:
    return [
        {
            "id": str(t.id),
            "project_id": str(t.project_id),
            "parent_task_id": str(t.parent_task_id) if t.parent_task_id else None,
            "title": t.title,
            "description": t.description,
            "status": t.status,
            "priority": t.priority,
            "assigned_agent": t.assigned_agent,
            "meta": t.meta or {},
            "created_by": str(t.created_by),
            "created_at": t.created_at.isoformat() if t.created_at else None,
        }
        for t in tasks
    ]


@router.get("/search", dependencies=[Depends(PermissionChecker(["read_notes"]))])
def search_knowledge_base(
    query: str, 
    db: Session = Depends(get_db), 
    current_user=Depends(AuthService.get_current_user)
):
    """
    Search endpoint optimized for AI Agents to retrieve relevant context.
    Searches both notes and tasks for the given query.
    """
    user_id = current_user.id
    
    # Simple keyword search - can be upgraded to vector search later
    notes = db.query(Note).filter(
        Note.created_by == user_id,
        or_(
            Note.title.ilike(f"%{query}%"),
            Note.content.ilike(f"%{query}%")
        )
    ).limit(10).all()

    tasks = db.query(Task).filter(
        Task.created_by == user_id,
        or_(
            Task.title.ilike(f"%{query}%"),
            Task.description.ilike(f"%{query}%")
        )
    ).limit(10).all()

    return {"notes": _serialize_notes(notes), "tasks": _serialize_tasks(tasks)}

@router.post("/import", status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionChecker(["write_notes"]))])
def import_knowledge(
    data: dict, # Expecting {"notes": [...], "tasks": [...]}
    db: Session = Depends(get_db),
    current_user=Depends(AuthService.get_current_user)
):
    """
    Import batch notes and tasks into the knowledge base.
    """
    user_id = current_user.id
    count = {"notes": 0, "tasks": 0}
    
    from app.services.notes import NoteService
    from app.services.tasks import TaskService
    from app.schemas.notes import NoteCreateSchema
    from app.schemas.tasks import TaskCreateSchema
    
    for note_data in data.get("notes", []):
        note_in = NoteCreateSchema(**note_data)
        NoteService.create_note(db, user_id, note_in)
        count["notes"] += 1
        
    for task_data in data.get("tasks", []):
        task_in = TaskCreateSchema(**task_data)
        TaskService.create_task(db, user_id, task_in)
        count["tasks"] += 1
        
    return {"message": "Import successful", "imported": count}
