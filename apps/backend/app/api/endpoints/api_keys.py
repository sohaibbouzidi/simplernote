from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.api_keys import APIKeyCreateSchema, APIKeySchema
from app.services.api_keys import APIKeyService
from app.services.auth import AuthService
from app.services.activity_logs import ActivityLogService
import uuid

router = APIRouter()


@router.get("/", response_model=List[APIKeySchema])
def list_api_keys(db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    return APIKeyService.list_api_keys(db, current_user.id)


@router.get("/project/{project_id}", response_model=List[APIKeySchema])
def list_project_api_keys(project_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    return APIKeyService.list_api_keys(db, current_user.id, project_id=str(project_id))


@router.post("/", response_model=APIKeySchema, status_code=status.HTTP_201_CREATED)
def create_api_key(key_in: APIKeyCreateSchema, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    api_key, token = APIKeyService.create_api_key(db, current_user.id, key_in)
    ActivityLogService.record(db, user_id=str(current_user.id), action="create", entity_type="api_key", entity_id=str(api_key["id"]), project_id=str(api_key["project_id"]), payload={"name": api_key["name"]})
    return {**api_key, "plain_text_key": token}


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_api_key(key_id: str, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    from app.repositories.api_keys import APIKeyRepository
    api_key = APIKeyRepository.get(db, key_id, current_user.id)
    if not api_key:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found")
    ActivityLogService.record(db, user_id=str(current_user.id), action="delete", entity_type="api_key", entity_id=key_id, project_id=str(api_key.project_id), payload={"name": api_key.name})
    APIKeyService.revoke_api_key(db, current_user.id, key_id)
    return None
