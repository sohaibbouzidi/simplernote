from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import UserCreateSchema
from app.utils.security import get_password_hash


class UserRepository:
    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_id(db: Session, user_id: str) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create(db: Session, user_in: UserCreateSchema) -> User:
        user = User(email=user_in.email, password_hash=get_password_hash(user_in.password))
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
