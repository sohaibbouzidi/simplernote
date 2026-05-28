from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.api_keys import APIKeyCreateSchema, APIKeySchema
from app.services.api_keys import APIKeyService
from app.services.auth import AuthService

router = APIRouter()


@router.get("/", response_model=List[APIKeySchema])
def list_api_keys(db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    return APIKeyService.list_api_keys(db, current_user.id)


@router.post("/", response_model=APIKeySchema, status_code=status.HTTP_201_CREATED)
def create_api_key(key_in: APIKeyCreateSchema, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    api_key, token = APIKeyService.create_api_key(db, current_user.id, key_in)
    return {**api_key, "plain_text_key": token}


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_api_key(key_id: str, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    success = APIKeyService.revoke_api_key(db, current_user.id, key_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found")
    return None
