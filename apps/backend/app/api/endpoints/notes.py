from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.notes import NoteCreateSchema, NoteSchema, NoteUpdateSchema
from app.services.notes import NoteService
from app.api.deps import PermissionChecker
from app.services.auth import AuthService

router = APIRouter()


@router.get("/", response_model=List[NoteSchema], dependencies=[Depends(PermissionChecker(["read_notes"]))])
def list_notes(project_id: Optional[str] = None, note_type: Optional[str] = None, search: Optional[str] = None, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    # Note: If API key is used, current_user is still fetched by AuthService.get_current_user
    # The permissions are checked by PermissionChecker dependency above.
    user_id = current_user.id
    return NoteService.list_notes(db, user_id, project_id=project_id, note_type=note_type, search=search)


@router.post("/", response_model=NoteSchema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionChecker(["write_notes"]))])
def create_note(note_in: NoteCreateSchema, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    user_id = current_user.id
    return NoteService.create_note(db, user_id, note_in)


@router.get("/{note_id}", response_model=NoteSchema, dependencies=[Depends(PermissionChecker(["read_notes"]))])
def get_note(note_id: str, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    user_id = current_user.id
    note = NoteService.get_note(db, note_id, user_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.patch("/{note_id}", response_model=NoteSchema, dependencies=[Depends(PermissionChecker(["write_notes"]))])
def update_note(note_id: str, note_in: NoteUpdateSchema, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    user_id = current_user.id
    note = NoteService.update_note(db, note_id, user_id, note_in)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionChecker(["write_notes"]))])
def delete_note(note_id: str, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    user_id = current_user.id
    success = NoteService.delete_note(db, note_id, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return None
