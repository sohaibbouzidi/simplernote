from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.activity_logs import ActivityLogSchema
from app.services.activity_logs import ActivityLogService
from app.services.auth import AuthService

router = APIRouter()


@router.get("/", response_model=List[ActivityLogSchema])
def list_activity_logs(project_id: Optional[str] = None, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    return ActivityLogService.list_activity_logs(db, current_user.id, project_id=project_id)
