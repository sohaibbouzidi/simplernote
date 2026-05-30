from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User

from app.core.config import settings
from app.core.rate_limit import rate_limit
from app.db.session import get_db
from app.schemas.auth import (
    TokenSchema, UserCreateSchema, UserLoginSchema, UserSchema,
    TokenRefreshSchema, ChangePasswordSchema,
    ForgotPasswordSchema, ResetPasswordSchema, ConfirmEmailSchema,
)
from app.services.auth import AuthService, oauth2_scheme
from app.services.users import UserService
from app.services.email import send_confirmation_email, send_password_reset_email
from app.utils.security import get_password_hash, verify_password, validate_password_strength, create_token, decode_token

router = APIRouter()

CONFIRM_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
RESET_TOKEN_EXPIRE_MINUTES = 60  # 1 hour


@router.post("/register", response_model=UserSchema, status_code=201)
def register(
    user_in: UserCreateSchema,
    db: Session = Depends(get_db),
    _=Depends(rate_limit(max_requests=10, window_seconds=60)),
):
    if UserService.get_by_email(db, user_in.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    err = validate_password_strength(user_in.password)
    if err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)
    user = UserService.create_user(db, user_in)
    token = create_token(
        {"sub": str(user.id), "type": "email_confirmation"},
        settings.JWT_SECRET, settings.JWT_ALGORITHM,
        timedelta(minutes=CONFIRM_TOKEN_EXPIRE_MINUTES),
    )
    send_confirmation_email(user.email, token)
    return user


@router.post("/confirm-email", response_model=dict)
def confirm_email(
    data: ConfirmEmailSchema,
    db: Session = Depends(get_db),
):
    payload = decode_token(data.token, settings.JWT_SECRET, [settings.JWT_ALGORITHM])
    if not payload or payload.get("type") != "email_confirmation":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired confirmation token")
    user = UserService.get_by_id(db, payload["sub"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.email_confirmed:
        return {"message": "Email already confirmed"}
    user.email_confirmed = True
    db.commit()
    return {"message": "Email confirmed successfully"}


@router.post("/forgot-password", response_model=dict)
def forgot_password(
    data: ForgotPasswordSchema,
    db: Session = Depends(get_db),
    _=Depends(rate_limit(max_requests=5, window_seconds=60)),
):
    user = UserService.get_by_email(db, data.email)
    if user:
        token = create_token(
            {"sub": str(user.id), "type": "password_reset"},
            settings.JWT_SECRET, settings.JWT_ALGORITHM,
            timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES),
        )
        send_password_reset_email(user.email, token)
    return {"message": "If an account with that email exists, a password reset link has been sent."}


@router.post("/reset-password", response_model=dict)
def reset_password(
    data: ResetPasswordSchema,
    db: Session = Depends(get_db),
    _=Depends(rate_limit(max_requests=5, window_seconds=60)),
):
    payload = decode_token(data.token, settings.JWT_SECRET, [settings.JWT_ALGORITHM])
    if not payload or payload.get("type") != "password_reset":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token")
    user = UserService.get_by_id(db, payload["sub"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    err = validate_password_strength(data.new_password)
    if err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)
    user.password_hash = get_password_hash(data.new_password)
    db.commit()
    return {"message": "Password reset successfully"}


@router.post("/login", response_model=TokenSchema)
def login(
    form_data: UserLoginSchema,
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


@router.get("/me", response_model=UserSchema)
def get_me(current_user: User = Depends(AuthService.get_current_user)):
    return current_user


@router.patch("/password", response_model=dict)
def change_password(
    data: ChangePasswordSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    if not verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    err = validate_password_strength(data.new_password)
    if err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)
    current_user.password_hash = get_password_hash(data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}
