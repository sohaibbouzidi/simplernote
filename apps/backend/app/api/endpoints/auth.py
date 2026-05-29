from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.rate_limit import rate_limit
from app.db.session import get_db
from app.schemas.auth import TokenSchema, UserCreateSchema, UserSchema, TokenRefreshSchema
from app.services.auth import AuthService
from app.services.users import UserService

router = APIRouter()


@router.post("/register", response_model=UserSchema)
def register(
    user_in: UserCreateSchema,
    db: Session = Depends(get_db),
    _=Depends(rate_limit(max_requests=10, window_seconds=60)),
):
    if UserService.get_by_email(db, user_in.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = UserService.create_user(db, user_in)
    return user


@router.post("/login", response_model=TokenSchema)
def login(
    form_data: UserCreateSchema,
    db: Session = Depends(get_db),
    _=Depends(rate_limit(max_requests=10, window_seconds=60)),
):
    user = AuthService.authenticate(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = AuthService.create_access_token({"sub": str(user.id)}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = AuthService.create_refresh_token({"sub": str(user.id)}, expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=TokenSchema)
def refresh_token(refresh: TokenRefreshSchema, db: Session = Depends(get_db)):
    token_data = AuthService.verify_refresh_token(refresh.refresh_token)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    access_token = AuthService.create_access_token({"sub": token_data.sub}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "refresh_token": refresh.refresh_token, "token_type": "bearer"}
