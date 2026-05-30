from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    country: str
    city: str
    picture: Optional[str] = None


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class UserSchema(BaseModel):
    id: UUID4
    email: EmailStr
    is_active: bool
    email_confirmed: bool = True
    role: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    picture: Optional[str] = None
    created_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    profile_updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    picture: Optional[str] = None


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenRefreshSchema(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str


class ForgotPasswordSchema(BaseModel):
    email: EmailStr


class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str


class ConfirmEmailSchema(BaseModel):
    token: str


class ResendConfirmationSchema(BaseModel):
    email: EmailStr
