from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.services.auth import AuthService, oauth2_scheme
from app.services.api_keys import APIKeyService
from typing import List

class PermissionChecker:
    def __init__(self, required_permissions: List[str]):
        self.required_permissions = required_permissions

    def __call__(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        # If it's an API key, we check permissions explicitly
        if token.startswith("sk_"):
            key_data = APIKeyService.authenticate_api_token(db, token)
            if not key_data:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
            
            # Check if all required permissions are True in the API key
            permissions = key_data.get("permissions", {})
            for perm in self.required_permissions:
                if not permissions.get(perm, False):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, 
                        detail=f"Missing required permission: {perm}"
                    )
            return key_data
        
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
