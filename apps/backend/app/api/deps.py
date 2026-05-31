from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.services.auth import AuthService, oauth2_scheme
from app.services.api_keys import APIKeyService
from typing import List
from app.services.users import UserService

class PermissionChecker:
    def __init__(self, required_permissions: List[str]):
        self.required_permissions = required_permissions

    def __call__(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        if token.startswith("sk_"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Use X-API-KEY header for API key auth")
        user = AuthService.get_current_user(token=token, db=db)
        return {"user_id": user.id}


def require_role(role: str):
    def role_checker(current_user: User = Depends(AuthService.get_current_user)):
        if current_user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. {role} role required.",
            )
        return current_user
    return role_checker


def require_profile_complete(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if token.startswith("sk_"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Use X-API-KEY header for API key auth")
    user = AuthService.get_current_user(token=token, db=db)
    # picture is optional; require only name and location fields
    required = [user.first_name, user.last_name, user.country, user.city]
    if not all(required):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Profile incomplete. Please complete your profile.")
    return user


async def get_ai_agent_key(request: Request, db: Session = Depends(get_db)):
    api_key = request.headers.get("X-API-KEY")
    if not api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="X-API-KEY header required")
    key_data = APIKeyService.authenticate_api_token(db, api_key)
    if not key_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return key_data
