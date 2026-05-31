from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.notes import NoteCreateSchema, NoteSchema, NoteUpdateSchema
from app.services.notes import NoteService
from app.api.deps import PermissionChecker
from app.services.auth import AuthService
from app.services.activity_logs import ActivityLogService

router = APIRouter()


@router.get("/", response_model=List[NoteSchema], dependencies=[Depends(PermissionChecker(["read_notes"]))])
def list_notes(project_id: str, note_type: Optional[str] = None, search: Optional[str] = None, with_deleted: bool = Query(False), db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    user_id = current_user.id
    return NoteService.list_notes(db, user_id, project_id, note_type=note_type, search=search, with_deleted=with_deleted)


@router.post("/", response_model=NoteSchema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionChecker(["write_notes"]))])
def create_note(project_id: str, note_in: NoteCreateSchema, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    user_id = current_user.id
    note = NoteService.create_note(db, user_id, project_id, note_in)
    ActivityLogService.record(db, user_id=str(user_id), action="create", entity_type="note", entity_id=str(note.id), project_id=project_id, payload={"title": note.title}, auth_method=getattr(current_user, '_auth_method', 'user'))
    return note


@router.get("/{note_id}", response_model=NoteSchema, dependencies=[Depends(PermissionChecker(["read_notes"]))])
def get_note(project_id: str, note_id: str, with_deleted: bool = Query(False), db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    user_id = current_user.id
    note = NoteService.get_note(db, note_id, user_id, project_id=project_id, with_deleted=with_deleted)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.patch("/{note_id}", response_model=NoteSchema, dependencies=[Depends(PermissionChecker(["write_notes"]))])
def update_note(project_id: str, note_id: str, note_in: NoteUpdateSchema, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    user_id = current_user.id
    note = NoteService.get_note(db, note_id, user_id, project_id=project_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    note = NoteService.update_note(db, note_id, user_id, note_in)
    ActivityLogService.record(db, user_id=str(user_id), action="update", entity_type="note", entity_id=note_id, project_id=project_id, payload={"title": note.title}, auth_method=getattr(current_user, '_auth_method', 'user'))
    return note


@router.patch("/{note_id}/restore", response_model=NoteSchema, dependencies=[Depends(PermissionChecker(["write_notes"]))])
def restore_note(project_id: str, note_id: str, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    user_id = current_user.id
    note = NoteService.restore_note(db, note_id, user_id, project_id=project_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found or not deleted")
    ActivityLogService.record(db, user_id=str(user_id), action="restore", entity_type="note", entity_id=note_id, project_id=project_id, payload={"title": note.title}, auth_method=getattr(current_user, '_auth_method', 'user'))
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionChecker(["write_notes"]))])
def delete_note(project_id: str, note_id: str, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    user_id = current_user.id
    note = NoteService.get_note(db, note_id, user_id, project_id=project_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    ActivityLogService.record(db, user_id=str(user_id), action="delete", entity_type="note", entity_id=note_id, project_id=project_id, payload={"title": note.title}, auth_method=getattr(current_user, '_auth_method', 'user'))
    NoteService.delete_note(db, note_id, user_id, project_id=project_id)
    return None