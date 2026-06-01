from datetime import datetime
from app.utils.timezone import now
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.models.api_key import APIKey
from app.models.project import Project


class APIKeyRepository:
    @staticmethod
    def list_by_user(db: Session, user_id: str, project_id: str | None = None):
        q = db.query(APIKey).options(joinedload(APIKey.project)).filter(APIKey.user_id == user_id)
        if project_id:
            q = q.filter(APIKey.project_id == project_id)
        return q.all()

    @staticmethod
    def get(db: Session, key_id: str, user_id: str):
        return (
            db.query(APIKey)
            .options(joinedload(APIKey.project))
            .filter(APIKey.id == key_id, APIKey.user_id == user_id)
            .first()
        )

    @staticmethod
    def get_by_id(db: Session, key_id: str):
        return (
            db.query(APIKey)
            .options(joinedload(APIKey.project))
            .filter(APIKey.id == key_id)
            .first()
        )

    @staticmethod
    def create(db: Session, user_id: str, name: str, key_hash: str, permissions: dict, expires_at=None, project_id: UUID = None):
        api_key = APIKey(
            user_id=user_id,
            name=name,
            key_hash=key_hash,
            permissions=permissions,
            expires_at=expires_at,
            project_id=project_id,
        )
        db.add(api_key)
        db.commit()
        db.refresh(api_key)
        return api_key

    @staticmethod
    def delete(db: Session, api_key: APIKey):
        db.delete(api_key)
        db.commit()

    @staticmethod
    def update_last_used(db: Session, api_key: APIKey):
        api_key.last_used_at = now()
        db.commit()
        db.refresh(api_key)
        return api_key
