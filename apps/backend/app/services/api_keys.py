import secrets
from datetime import datetime
from typing import Tuple, Optional

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.repositories.api_keys import APIKeyRepository
from app.schemas.api_keys import APIKeyCreateSchema
from app.utils.security import get_password_hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class APIKeyService:
    @staticmethod
    def list_api_keys(db: Session, user_id: str):
        return APIKeyRepository.list_by_user(db, user_id)

    @staticmethod
    def create_api_key(db: Session, user_id: str, key_in: APIKeyCreateSchema) -> Tuple[dict, str]:
        secret = secrets.token_urlsafe(32)
        hashed = get_password_hash(secret)
        expires_at = key_in.expires_at
        api_key = APIKeyRepository.create(db, user_id, key_in.name, hashed, key_in.permissions, expires_at)
        token = f"sk_{api_key.id}.{secret}"
        serialized = {
            "id": api_key.id,
            "name": api_key.name,
            "permissions": api_key.permissions,
            "last_used_at": api_key.last_used_at,
            "expires_at": api_key.expires_at,
            "created_at": api_key.created_at,
        }
        return serialized, token

    @staticmethod
    def revoke_api_key(db: Session, user_id: str, key_id: str):
        api_key = APIKeyRepository.get(db, key_id, user_id)
        if not api_key:
            return False
        APIKeyRepository.delete(db, api_key)
        return True

    @staticmethod
    def authenticate_api_token(db: Session, token: str) -> Optional[dict]:
        if not token.startswith("sk_") or "." not in token:
            return None
        _, rest = token.split("sk_", 1)
        try:
            token_id, secret = rest.split(".", 1)
        except ValueError:
            return None
        api_key = APIKeyRepository.get_by_id(db, token_id)
        if not api_key:
            return None
        if api_key.expires_at and api_key.expires_at < datetime.utcnow():
            return None
        if not pwd_context.verify(secret, api_key.key_hash):
            return None
        APIKeyRepository.update_last_used(db, api_key)
        return {"user_id": str(api_key.user_id), "permissions": api_key.permissions, "api_key_id": str(api_key.id)}
