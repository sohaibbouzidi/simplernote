from datetime import timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import TokenPayload
from app.services.users import UserService
from app.services.api_keys import APIKeyService
from app.utils.security import create_token, decode_token, verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


class AuthService:
    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> Optional[User]:
        user = UserService.get_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta) -> str:
        return create_token(data, settings.JWT_SECRET, settings.JWT_ALGORITHM, expires_delta)

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: timedelta) -> str:
        return create_token(data, settings.JWT_SECRET, settings.JWT_ALGORITHM, expires_delta)

    @staticmethod
    def verify_refresh_token(token: str) -> Optional[TokenPayload]:
        payload = decode_token(token, settings.JWT_SECRET, [settings.JWT_ALGORITHM])
        if not payload or "sub" not in payload:
            return None
        return TokenPayload(sub=payload["sub"])

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
        if token.startswith("sk_"):
            key_data = APIKeyService.authenticate_api_token(db, token)
            if not key_data:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
            user = UserService.get_by_id(db, key_data["user_id"])
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
            return user

        payload = decode_token(token, settings.JWT_SECRET, [settings.JWT_ALGORITHM])
        if not payload or "sub" not in payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        user = UserService.get_by_id(db, payload["sub"])
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
