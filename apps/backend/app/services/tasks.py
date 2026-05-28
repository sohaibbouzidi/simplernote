from sqlalchemy.orm import Session

from app.repositories.tasks import TaskRepository
from app.schemas.tasks import TaskCreateSchema, TaskUpdateSchema


class TaskService:
    @staticmethod
    def list_tasks(db: Session, user_id: str, project_id=None, status=None):
        return TaskRepository.list(db, user_id, project_id=project_id, status=status)

    @staticmethod
    def create_task(db: Session, user_id: str, task_in: TaskCreateSchema):
        return TaskRepository.create(db, user_id, task_in)

    @staticmethod
    def get_task(db: Session, task_id: str, user_id: str):
        return TaskRepository.get(db, task_id, user_id)

    @staticmethod
    def update_task(db: Session, task_id: str, user_id: str, task_in: TaskUpdateSchema):
        task = TaskRepository.get(db, task_id, user_id)
        if not task:
            return None
        return TaskRepository.update(db, task, task_in)

    @staticmethod
    def delete_task(db: Session, task_id: str, user_id: str):
        task = TaskRepository.get(db, task_id, user_id)
        if not task:
            return False
        TaskRepository.delete(db, task)
        return True
