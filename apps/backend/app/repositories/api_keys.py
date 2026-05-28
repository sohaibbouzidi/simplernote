from datetime import datetime
from sqlalchemy.orm import Session

from app.models.api_key import APIKey


class APIKeyRepository:
    @staticmethod
    def list_by_user(db: Session, user_id: str):
        return db.query(APIKey).filter(APIKey.user_id == user_id).all()

    @staticmethod
    def get(db: Session, key_id: str, user_id: str):
        return db.query(APIKey).filter(APIKey.id == key_id, APIKey.user_id == user_id).first()

    @staticmethod
    def get_by_id(db: Session, key_id: str):
        return db.query(APIKey).filter(APIKey.id == key_id).first()

    @staticmethod
    def create(db: Session, user_id: str, name: str, key_hash: str, permissions: dict, expires_at=None):
        api_key = APIKey(user_id=user_id, name=name, key_hash=key_hash, permissions=permissions, expires_at=expires_at)
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
        api_key.last_used_at = datetime.utcnow()
        db.commit()
        db.refresh(api_key)
        return api_key
