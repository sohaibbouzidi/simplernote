import json
from sqlalchemy.orm import Session

from app.repositories.projects import ProjectRepository
from app.schemas.projects import ProjectCreateSchema, ProjectUpdateSchema
from app.core.redis_client import get_redis, cache_invalidate_pattern


CACHE_TTL = 300


def _project_cache_key(user_id: str, project_id: str = None):
    if project_id:
        return f"projects:get:{user_id}:{project_id}"
    return f"projects:list:{user_id}"


def _invalidate_project_cache(user_id: str):
    cache_invalidate_pattern(f"projects:get:{user_id}:*")
    cache_invalidate_pattern(f"projects:list:{user_id}")


def _serialize_project(p):
    return {
        "id": str(p.id),
        "name": p.name,
        "description": p.description,
        "created_by": str(p.created_by),
        "created_at": p.created_at.isoformat() if p.created_at else None,
    }


class ProjectService:
    @staticmethod
    def list_projects(db: Session, user_id: str):
        cache_key = _project_cache_key(user_id)
        r = get_redis()
        if r:
            cached = r.get(cache_key)
            if cached:
                return json.loads(cached)

        projects = ProjectRepository.list_by_user(db, user_id)
        if r:
            r.setex(cache_key, CACHE_TTL, json.dumps([_serialize_project(p) for p in projects], default=str))
        return projects

    @staticmethod
    def create_project(db: Session, user_id: str, project_in: ProjectCreateSchema):
        project = ProjectRepository.create(db, user_id, project_in)
        _invalidate_project_cache(user_id)
        return project

    @staticmethod
    def get_project(db: Session, project_id: str, user_id: str):
        cache_key = _project_cache_key(user_id, project_id=project_id)
        r = get_redis()
        if r:
            cached = r.get(cache_key)
            if cached:
                return json.loads(cached)

        project = ProjectRepository.get(db, project_id, user_id)
        if r and project:
            r.setex(cache_key, CACHE_TTL, json.dumps(_serialize_project(project), default=str))
        return project

    @staticmethod
    def update_project(db: Session, project_id: str, user_id: str, project_in: ProjectUpdateSchema):
        project = ProjectRepository.get(db, project_id, user_id)
        if not project:
            return None
        project = ProjectRepository.update(db, project, project_in)
        _invalidate_project_cache(user_id)
        return project

    @staticmethod
    def delete_project(db: Session, project_id: str, user_id: str):
        project = ProjectRepository.get(db, project_id, user_id)
        if not project:
            return False
        ProjectRepository.delete(db, project)
        _invalidate_project_cache(user_id)
        return True
