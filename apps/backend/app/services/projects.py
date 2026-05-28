from sqlalchemy.orm import Session

from app.repositories.projects import ProjectRepository
from app.schemas.projects import ProjectCreateSchema, ProjectUpdateSchema


class ProjectService:
    @staticmethod
    def list_projects(db: Session, user_id: str):
        return ProjectRepository.list_by_user(db, user_id)

    @staticmethod
    def create_project(db: Session, user_id: str, project_in: ProjectCreateSchema):
        return ProjectRepository.create(db, user_id, project_in)

    @staticmethod
    def get_project(db: Session, project_id: str, user_id: str):
        return ProjectRepository.get(db, project_id, user_id)

    @staticmethod
    def update_project(db: Session, project_id: str, user_id: str, project_in: ProjectUpdateSchema):
        project = ProjectRepository.get(db, project_id, user_id)
        if not project:
            return None
        return ProjectRepository.update(db, project, project_in)

    @staticmethod
    def delete_project(db: Session, project_id: str, user_id: str):
        project = ProjectRepository.get(db, project_id, user_id)
        if not project:
            return False
        ProjectRepository.delete(db, project)
        return True
