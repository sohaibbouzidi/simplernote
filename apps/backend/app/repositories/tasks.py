from datetime import datetime
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.tasks import TaskCreateSchema, TaskUpdateSchema


class TaskRepository:
    @staticmethod
    def list(db: Session, user_id: str, project_id: str, status=None, with_deleted=False):
        query = db.query(Task).filter(Task.created_by == user_id, Task.project_id == project_id)
        if not with_deleted:
            query = query.filter(Task.deleted_at.is_(None))
        if status:
            query = query.filter(Task.status == status)
        return query.order_by(Task.created_at.desc()).all()

    @staticmethod
    def get(db: Session, task_id: str, user_id: str, project_id: str = None, with_deleted=False):
        query = db.query(Task).filter(Task.id == task_id, Task.created_by == user_id)
        if project_id:
            query = query.filter(Task.project_id == project_id)
        if not with_deleted:
            query = query.filter(Task.deleted_at.is_(None))
        return query.first()

    @staticmethod
    def create(db: Session, user_id: str, project_id: str, task_in: TaskCreateSchema):
        task = Task(created_by=user_id, project_id=project_id, **task_in.model_dump())
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def update(db: Session, task: Task, task_in: TaskUpdateSchema):
        for field, value in task_in.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete(db: Session, task: Task):
        task.deleted_at = datetime.utcnow()
        db.commit()

    @staticmethod
    def restore(db: Session, task: Task):
        task.deleted_at = None
        db.commit()
        db.refresh(task)
        return task
