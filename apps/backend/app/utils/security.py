import re
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def validate_password_strength(password: str) -> Optional[str]:
    if len(password) < 8:
        return "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return "Password must contain at least one digit"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\';/`~]", password):
        return "Password must contain at least one special character"
    return None


def create_token(data: dict, secret_key: str, algorithm: str, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_token(token: str, secret_key: str, algorithms: list[str]):
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithms)
        return payload
    except JWTError:
        return None
