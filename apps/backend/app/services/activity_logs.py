from sqlalchemy.orm import Session

from app.repositories.activity_logs import ActivityLogRepository


class ActivityLogService:
    @staticmethod
    def list_activity_logs(db: Session, user_id: str, project_id=None):
        return ActivityLogRepository.list(db, user_id=user_id, project_id=project_id)

    @staticmethod
    def record(db: Session, user_id: str | None, action: str, entity_type: str, entity_id: str | None = None, project_id: str | None = None, payload: dict | None = None, auth_method: str = "user"):
        return ActivityLogRepository.create(db, user_id, action, entity_type, entity_id, project_id, payload, auth_method)
