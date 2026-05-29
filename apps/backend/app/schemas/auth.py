from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    picture: Optional[str] = None


class UserSchema(BaseModel):
    id: UUID4
    email: EmailStr
    is_active: bool
    role: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    picture: Optional[str] = None

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    picture: Optional[str] = None


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenRefreshSchema(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str
