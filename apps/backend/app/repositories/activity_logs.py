from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog


class ActivityLogRepository:
    @staticmethod
    def list(db: Session, user_id: str, project_id=None):
        query = db.query(ActivityLog).join(ActivityLog.project, isouter=True)
        if project_id:
            query = query.filter(ActivityLog.project_id == project_id)
        if user_id:
            query = query.filter(ActivityLog.user_id == user_id)
        return query.order_by(ActivityLog.created_at.desc()).all()

    @staticmethod
    def create(db: Session, user_id: str | None, action: str, entity_type: str, entity_id: str | None = None, project_id: str | None = None, payload: dict | None = None, auth_method: str = "user"):
        record = ActivityLog(user_id=user_id, action=action, entity_type=entity_type, entity_id=entity_id, project_id=project_id, payload=payload or {}, auth_method=auth_method)
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
