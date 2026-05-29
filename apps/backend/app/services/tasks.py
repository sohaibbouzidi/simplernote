import json
from sqlalchemy.orm import Session

from app.repositories.tasks import TaskRepository
from app.schemas.tasks import TaskCreateSchema, TaskUpdateSchema
from app.core.redis_client import get_redis, cache_invalidate_pattern


CACHE_TTL = 300


def _task_cache_key(user_id: str, task_id: str = None, project_id=None, status=None):
    if task_id:
        return f"tasks:get:{user_id}:{task_id}"
    return f"tasks:list:{user_id}:p:{project_id or ''}:s:{status or ''}"


def _serialize_task(t):
    return {
        "id": str(t.id),
        "project_id": str(t.project_id),
        "parent_task_id": str(t.parent_task_id) if t.parent_task_id else None,
        "title": t.title,
        "description": t.description,
        "status": t.status,
        "priority": t.priority,
        "assigned_agent": t.assigned_agent,
        "meta": t.meta or {},
        "created_by": str(t.created_by),
        "created_at": t.created_at.isoformat() if t.created_at else None,
    }


class TaskService:
    @staticmethod
    def list_tasks(db: Session, user_id: str, project_id=None, status=None):
        cache_key = _task_cache_key(user_id, project_id=project_id, status=status)
        r = get_redis()
        if r:
            cached = r.get(cache_key)
            if cached:
                return json.loads(cached)

        tasks = TaskRepository.list(db, user_id, project_id=project_id, status=status)
        if r:
            r.setex(cache_key, CACHE_TTL, json.dumps([_serialize_task(t) for t in tasks], default=str))
        return tasks

    @staticmethod
    def create_task(db: Session, user_id: str, task_in: TaskCreateSchema):
        task = TaskRepository.create(db, user_id, task_in)
        cache_invalidate_pattern(f"tasks:list:{user_id}:*")
        return task

    @staticmethod
    def get_task(db: Session, task_id: str, user_id: str):
        cache_key = _task_cache_key(user_id, task_id=task_id)
        r = get_redis()
        if r:
            cached = r.get(cache_key)
            if cached:
                return json.loads(cached)

        task = TaskRepository.get(db, task_id, user_id)
        if r and task:
            r.setex(cache_key, CACHE_TTL, json.dumps(_serialize_task(task), default=str))
        return task

    @staticmethod
    def update_task(db: Session, task_id: str, user_id: str, task_in: TaskUpdateSchema):
        task = TaskRepository.get(db, task_id, user_id)
        if not task:
            return None
        task = TaskRepository.update(db, task, task_in)
        cache_invalidate_pattern(f"tasks:*:{user_id}:*")
        return task

    @staticmethod
    def delete_task(db: Session, task_id: str, user_id: str):
        task = TaskRepository.get(db, task_id, user_id)
        if not task:
            return False
        TaskRepository.delete(db, task)
        cache_invalidate_pattern(f"tasks:*:{user_id}:*")
        return True
