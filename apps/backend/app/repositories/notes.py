from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.note import Note
from app.schemas.notes import NoteCreateSchema, NoteUpdateSchema


class NoteRepository:
    @staticmethod
    def list(db: Session, user_id: str, project_id=None, note_type=None, search=None):
        query = db.query(Note).filter(Note.created_by == user_id)
        if project_id:
            query = query.filter(Note.project_id == project_id)
        if note_type:
            query = query.filter(Note.note_type == note_type)
        if search:
            search_term = f"%{search}%"
            query = query.filter(or_(Note.title.ilike(search_term), Note.content.ilike(search_term), Note.summary.ilike(search_term)))
        return query.order_by(Note.updated_at.desc()).all()

    @staticmethod
    def get(db: Session, note_id: str, user_id: str):
        return db.query(Note).filter(Note.id == note_id, Note.created_by == user_id).first()

    @staticmethod
    def create(db: Session, user_id: str, note_in: NoteCreateSchema):
        note = Note(created_by=user_id, **note_in.model_dump())
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

    @staticmethod
    def update(db: Session, note: Note, note_in: NoteUpdateSchema):
        for field, value in note_in.model_dump(exclude_unset=True).items():
            setattr(note, field, value)
        db.commit()
        db.refresh(note)
        return note

    @staticmethod
    def delete(db: Session, note: Note):
        db.delete(note)
        db.commit()
