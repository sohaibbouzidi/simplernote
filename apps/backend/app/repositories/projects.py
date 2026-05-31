from datetime import datetime
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.note import Note
from app.models.task import Task
from app.models.ai_context import AiContext
from app.schemas.projects import ProjectCreateSchema, ProjectUpdateSchema


class ProjectRepository:
    @staticmethod
    def list_by_user(db: Session, user_id: str, with_deleted=False):
        query = db.query(Project).filter(Project.created_by == user_id)
        if not with_deleted:
            query = query.filter(Project.deleted_at.is_(None))
        return query.all()

    @staticmethod
    def get(db: Session, project_id: str, user_id: str, with_deleted=False):
        query = db.query(Project).filter(Project.id == project_id, Project.created_by == user_id)
        if not with_deleted:
            query = query.filter(Project.deleted_at.is_(None))
        return query.first()

    @staticmethod
    def create(db: Session, user_id: str, project_in: ProjectCreateSchema):
        project = Project(created_by=user_id, **project_in.model_dump())
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def update(db: Session, project: Project, project_in: ProjectUpdateSchema):
        for field, value in project_in.model_dump(exclude_unset=True).items():
            setattr(project, field, value)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def delete(db: Session, project: Project):
        now = datetime.utcnow()
        project.deleted_at = now
        db.query(Note).filter(Note.project_id == project.id, Note.deleted_at.is_(None)).update({"deleted_at": now})
        db.query(Task).filter(Task.project_id == project.id, Task.deleted_at.is_(None)).update({"deleted_at": now})
        db.query(AiContext).filter(AiContext.project_id == project.id, AiContext.deleted_at.is_(None)).update({"deleted_at": now})
        db.commit()

    @staticmethod
    def restore(db: Session, project: Project):
        project.deleted_at = None
        db.query(Note).filter(Note.project_id == project.id, Note.deleted_at.is_not(None)).update({"deleted_at": None})
        db.query(Task).filter(Task.project_id == project.id, Task.deleted_at.is_not(None)).update({"deleted_at": None})
        db.query(AiContext).filter(AiContext.project_id == project.id, AiContext.deleted_at.is_not(None)).update({"deleted_at": None})
        db.commit()
        db.refresh(project)
        return project
