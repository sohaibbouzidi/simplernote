from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.tasks import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from app.services.tasks import TaskService
from app.services.auth import AuthService
from app.services.activity_logs import ActivityLogService
from app.api.deps import PermissionChecker

router = APIRouter()


@router.get("/", response_model=List[TaskSchema], dependencies=[Depends(PermissionChecker(["read_tasks"]))])
def list_tasks(project_id: Optional[str] = None, status: Optional[str] = None, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    return TaskService.list_tasks(db, current_user.id, project_id=project_id, status=status)


@router.post("/", response_model=TaskSchema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionChecker(["write_tasks"]))])
def create_task(task_in: TaskCreateSchema, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    task = TaskService.create_task(db, current_user.id, task_in)
    ActivityLogService.record(db, user_id=str(current_user.id), action="create", entity_type="task", entity_id=str(task.id), project_id=str(task.project_id), payload={"title": task.title}, auth_method=getattr(current_user, '_auth_method', 'user'))
    return task


@router.get("/{task_id}", response_model=TaskSchema, dependencies=[Depends(PermissionChecker(["read_tasks"]))])
def get_task(task_id: str, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    task = TaskService.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskSchema, dependencies=[Depends(PermissionChecker(["write_tasks"]))])
def update_task(task_id: str, task_in: TaskUpdateSchema, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    task = TaskService.update_task(db, task_id, current_user.id, task_in)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    ActivityLogService.record(db, user_id=str(current_user.id), action="update", entity_type="task", entity_id=task_id, project_id=str(task.project_id), payload={"title": task.title}, auth_method=getattr(current_user, '_auth_method', 'user'))
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionChecker(["write_tasks"]))])
def delete_task(task_id: str, db: Session = Depends(get_db), current_user=Depends(AuthService.get_current_user)):
    task = TaskService.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    ActivityLogService.record(db, user_id=str(current_user.id), action="delete", entity_type="task", entity_id=task_id, project_id=str(task.project_id), payload={"title": task.title}, auth_method=getattr(current_user, '_auth_method', 'user'))
    TaskService.delete_task(db, task_id, current_user.id)
    return None
