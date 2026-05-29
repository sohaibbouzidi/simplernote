from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    id: UUID4
    email: EmailStr
    is_active: bool
    role: str

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenRefreshSchema(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str
