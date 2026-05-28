from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.projects import ProjectCreateSchema, ProjectUpdateSchema


class ProjectRepository:
    @staticmethod
    def list_by_user(db: Session, user_id: str):
        return db.query(Project).filter(Project.created_by == user_id).all()

    @staticmethod
    def get(db: Session, project_id: str, user_id: str):
        return db.query(Project).filter(Project.id == project_id, Project.created_by == user_id).first()

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
        db.delete(project)
        db.commit()
