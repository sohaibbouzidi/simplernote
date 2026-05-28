from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.api_keys import APIKeyService
from app.services.users import UserService

security = HTTPBearer(auto_error=False)


def get_api_key_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization header")
    token = credentials.credentials
    key_data = APIKeyService.authenticate_api_token(db, token)
    if not key_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    user = UserService.get_by_id(db, key_data["user_id"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key user")
    return {"user": user, "permissions": key_data["permissions"]}


def require_permission(permission: str):
    def dependency(api_key_data = Depends(get_api_key_user)):
        if not api_key_data["permissions"].get(permission, False):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return api_key_data
    return dependency
