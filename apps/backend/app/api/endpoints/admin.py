import uuid
from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.deps import require_role
from app.db.session import get_db
from app.models.activity_log import ActivityLog
from app.models.ai_context import AiContext
from app.models.api_key import APIKey
from app.models.note import Note
from app.models.project import Project
from app.models.task import Task
from app.models.user import User
from app.schemas.auth import UserSchema
from app.services.users import UserService

router = APIRouter(dependencies=[Depends(require_role("admin"))])


class AdminCreateUserSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    role: str = "user"
    email_confirmed: bool = False


@router.post("/users", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def admin_create_user(
    data: AdminCreateUserSchema,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    if data.role not in ("admin", "user"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role must be 'admin' or 'user'")

    user = UserService.create_user(db, data)  # type: ignore[arg-type]
    user.role = data.role
    user.email_confirmed = data.email_confirmed
    db.commit()
    db.refresh(user)
    return user


@router.get("/users", response_model=List[UserSchema])
def list_users(
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    return db.query(User).order_by(User.created_at.desc()).all()


@router.patch("/users/{user_id}/role", response_model=UserSchema)
def update_user_role(
    user_id: uuid.UUID,
    role: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    if current_user.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot change your own role")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if role not in ("admin", "user"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role must be 'admin' or 'user'")

    user.role = role
    db.commit()
    db.refresh(user)
    return user


@router.patch("/users/{user_id}/verify-email", response_model=UserSchema)
def verify_user_email(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.email_confirmed = True
    db.commit()
    db.refresh(user)
    return user


@router.patch("/users/{user_id}/toggle-active", response_model=UserSchema)
def toggle_user_active(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    if current_user.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot toggle your own account")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    if current_user.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete your own account")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = False
    db.commit()


@router.delete("/users/{user_id}/hard", status_code=status.HTTP_204_NO_CONTENT)
def hard_delete_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    if current_user.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete your own account")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.query(ActivityLog).filter(ActivityLog.user_id == user_id).delete(synchronize_session=False)
    db.query(APIKey).filter(APIKey.user_id == user_id).delete(synchronize_session=False)
    db.query(AiContext).filter(AiContext.created_by == user_id).delete(synchronize_session=False)
    db.query(Task).filter(Task.created_by == user_id).delete(synchronize_session=False)
    db.query(Note).filter(Note.created_by == user_id).delete(synchronize_session=False)
    db.query(Project).filter(Project.created_by == user_id).delete(synchronize_session=False)
    db.delete(user)
    db.commit()
