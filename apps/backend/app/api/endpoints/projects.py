from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.projects import ProjectCreateSchema, ProjectSchema, ProjectUpdateSchema
from app.services.projects import ProjectService
from app.services.auth import AuthService

router = APIRouter()


@router.get("/", response_model=List[ProjectSchema])
def get_projects(db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    return ProjectService.list_projects(db, current_user.id)


@router.post("/", response_model=ProjectSchema, status_code=status.HTTP_201_CREATED)
def create_project(project_in: ProjectCreateSchema, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    return ProjectService.create_project(db, current_user.id, project_in)


@router.get("/{project_id}", response_model=ProjectSchema)
def get_project(project_id: str, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    project = ProjectService.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectSchema)
def update_project(project_id: str, project_in: ProjectUpdateSchema, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    project = ProjectService.update_project(db, project_id, current_user.id, project_in)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    success = ProjectService.delete_project(db, project_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return None
