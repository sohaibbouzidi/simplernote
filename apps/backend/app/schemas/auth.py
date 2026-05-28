from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    id: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenRefreshSchema(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str
