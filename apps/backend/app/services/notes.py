from sqlalchemy.orm import Session

from app.repositories.notes import NoteRepository
from app.schemas.notes import NoteCreateSchema, NoteUpdateSchema


class NoteService:
    @staticmethod
    def list_notes(db: Session, user_id: str, project_id=None, note_type=None, search=None):
        return NoteRepository.list(db, user_id, project_id=project_id, note_type=note_type, search=search)

    @staticmethod
    def create_note(db: Session, user_id: str, note_in: NoteCreateSchema):
        return NoteRepository.create(db, user_id, note_in)

    @staticmethod
    def get_note(db: Session, note_id: str, user_id: str):
        return NoteRepository.get(db, note_id, user_id)

    @staticmethod
    def update_note(db: Session, note_id: str, user_id: str, note_in: NoteUpdateSchema):
        note = NoteRepository.get(db, note_id, user_id)
        if not note:
            return None
        return NoteRepository.update(db, note, note_in)

    @staticmethod
    def delete_note(db: Session, note_id: str, user_id: str):
        note = NoteRepository.get(db, note_id, user_id)
        if not note:
            return False
        NoteRepository.delete(db, note)
        return True
