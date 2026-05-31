from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.projects import ProjectCreateSchema, ProjectSchema, ProjectUpdateSchema
from app.services.projects import ProjectService
from app.services.auth import AuthService
from app.services.activity_logs import ActivityLogService

router = APIRouter()


@router.get("/", response_model=List[ProjectSchema])
def get_projects(with_deleted: bool = Query(False), db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    return ProjectService.list_projects(db, current_user.id, with_deleted=with_deleted)


@router.post("/", response_model=ProjectSchema, status_code=status.HTTP_201_CREATED)
def create_project(project_in: ProjectCreateSchema, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    project = ProjectService.create_project(db, current_user.id, project_in)
    ActivityLogService.record(db, user_id=str(current_user.id), action="create", entity_type="project", entity_id=str(project.id), project_id=str(project.id), payload={"name": project.name}, auth_method=getattr(current_user, '_auth_method', 'user'))
    return project


@router.get("/{project_id}", response_model=ProjectSchema)
def get_project(project_id: str, with_deleted: bool = Query(False), db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    project = ProjectService.get_project(db, project_id, current_user.id, with_deleted=with_deleted)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project

@router.patch("/{project_id}/restore", response_model=ProjectSchema)
def restore_project(project_id: str, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    project = ProjectService.restore_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found or not deleted")
    ActivityLogService.record(db, user_id=str(current_user.id), action="restore", entity_type="project", entity_id=project_id, project_id=project_id, payload={"name": project.name}, auth_method=getattr(current_user, '_auth_method', 'user'))
    return project

@router.patch("/{project_id}", response_model=ProjectSchema)
def update_project(project_id: str, project_in: ProjectUpdateSchema, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    project = ProjectService.update_project(db, project_id, current_user.id, project_in)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    ActivityLogService.record(db, user_id=str(current_user.id), action="update", entity_type="project", entity_id=project_id, project_id=project_id, payload={"name": project.name}, auth_method=getattr(current_user, '_auth_method', 'user'))
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    project = ProjectService.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    ActivityLogService.record(db, user_id=str(current_user.id), action="delete", entity_type="project", entity_id=project_id, project_id=project_id, payload={"name": project.name}, auth_method=getattr(current_user, '_auth_method', 'user'))
    ProjectService.delete_project(db, project_id, current_user.id)
    return None
