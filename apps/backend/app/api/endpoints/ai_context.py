from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.auth import AuthService
from app.services.ai_contexts import AiContextService
from app.api.deps import PermissionChecker
from app.schemas.ai_context import AiContextCreateSchema, AiContextUpdateSchema, AiContextSchema
from app.models.user import User
from app.models.project import Project
from app.models.ai_context import AiContext

from app.core.rate_limit import rate_limit

router = APIRouter(dependencies=[Depends(rate_limit(30, 60))])


@router.get("/project/{project_id}", response_model=AiContextSchema, dependencies=[Depends(PermissionChecker(["read_ai_context"]))])
def get_ai_context(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    ctx = AiContextService.get_by_project(db, project_id)
    if not ctx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No AI context for this project")
    return ctx


@router.post("", response_model=AiContextSchema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionChecker(["write_ai_context"]))])
def create_ai_context(
    data: AiContextCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    existing = AiContextService.get_by_project(db, data.project_id)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="AI context already exists for this project")
    project = db.query(Project).filter(Project.id == data.project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return AiContextService.create(db, str(current_user.id), data)


@router.patch("/{context_id}", response_model=AiContextSchema, dependencies=[Depends(PermissionChecker(["write_ai_context"]))])
def update_ai_context(
    context_id: str,
    data: AiContextUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    ctx = db.query(AiContext).filter(AiContext.id == context_id).first()
    if not ctx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AI context not found")
    return AiContextService.update(db, ctx, data)


@router.delete("/{context_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionChecker(["write_ai_context"]))])
def delete_ai_context(
    context_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    ctx = db.query(AiContext).filter(AiContext.id == context_id).first()
    if not ctx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AI context not found")
    AiContextService.delete(db, ctx)
