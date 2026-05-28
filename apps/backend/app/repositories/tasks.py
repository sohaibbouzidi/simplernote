from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.tasks import TaskCreateSchema, TaskUpdateSchema


class TaskRepository:
    @staticmethod
    def list(db: Session, user_id: str, project_id=None, status=None):
        query = db.query(Task).filter(Task.created_by == user_id)
        if project_id:
            query = query.filter(Task.project_id == project_id)
        if status:
            query = query.filter(Task.status == status)
        return query.order_by(Task.created_at.desc()).all()

    @staticmethod
    def get(db: Session, task_id: str, user_id: str):
        return db.query(Task).filter(Task.id == task_id, Task.created_by == user_id).first()

    @staticmethod
    def create(db: Session, user_id: str, task_in: TaskCreateSchema):
        task = Task(created_by=user_id, **task_in.model_dump())
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
        db.delete(task)
        db.commit()
