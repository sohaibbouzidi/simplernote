import json
from sqlalchemy.orm import Session

from app.repositories.notes import NoteRepository
from app.schemas.notes import NoteCreateSchema, NoteUpdateSchema
from app.core.redis_client import get_redis, cache_invalidate_pattern


CACHE_TTL = 300


def _note_cache_key(user_id: str, note_id: str = None, project_id=None, note_type=None, search=None):
    if note_id:
        return f"notes:get:{user_id}:{note_id}"
    return f"notes:list:{user_id}:p:{project_id or ''}:t:{note_type or ''}:s:{search or ''}"


def _serialize_note(n):
    from app.models.note import Note
    return {
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


class NoteService:
    @staticmethod
    def list_notes(db: Session, user_id: str, project_id: str, note_type=None, search=None, with_deleted=False):
        cache_key = _note_cache_key(user_id, project_id=project_id, note_type=note_type, search=search)
        r = get_redis()
        if r and not with_deleted:
            cached = r.get(cache_key)
            if cached:
                return json.loads(cached)
        notes = NoteRepository.list(db, user_id, project_id, note_type=note_type, search=search, with_deleted=with_deleted)
        if r and not with_deleted:
            r.setex(cache_key, CACHE_TTL, json.dumps([_serialize_note(n) for n in notes], default=str))
        return notes

    @staticmethod
    def create_note(db: Session, user_id: str, project_id: str, note_in: NoteCreateSchema):
        note = NoteRepository.create(db, user_id, project_id, note_in)
        cache_invalidate_pattern(f"notes:list:{user_id}:*")
        return note

    @staticmethod
    def get_note(db: Session, note_id: str, user_id: str, project_id: str = None, with_deleted=False):
        cache_key = _note_cache_key(user_id, note_id=note_id)
        r = get_redis()
        if r and not with_deleted:
            cached = r.get(cache_key)
            if cached:
                return json.loads(cached)
        note = NoteRepository.get(db, note_id, user_id, project_id=project_id, with_deleted=with_deleted)
        if r and note and not with_deleted:
            r.setex(cache_key, CACHE_TTL, json.dumps(_serialize_note(note), default=str))
        return note

    @staticmethod
    def update_note(db: Session, note_id: str, user_id: str, note_in: NoteUpdateSchema):
        note = NoteRepository.get(db, note_id, user_id)
        if not note:
            return None
        note = NoteRepository.update(db, note, note_in)
        cache_invalidate_pattern(f"notes:*:{user_id}:*")
        return note

    @staticmethod
    def delete_note(db: Session, note_id: str, user_id: str, project_id: str = None):
        note = NoteRepository.get(db, note_id, user_id, project_id=project_id)
        if not note:
            return False
        NoteRepository.delete(db, note)
        cache_invalidate_pattern(f"notes:*:{user_id}:*")
        return True

    @staticmethod
    def restore_note(db: Session, note_id: str, user_id: str, project_id: str = None):
        note = NoteRepository.get(db, note_id, user_id, project_id=project_id, with_deleted=True)
        if not note or note.deleted_at is None:
            return None
        note.deleted_at = None
        db.commit()
        cache_invalidate_pattern(f"notes:*:{user_id}:*")
        return note
