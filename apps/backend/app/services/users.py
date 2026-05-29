from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import UserCreateSchema, UserUpdateSchema
from app.utils.security import get_password_hash


class UserService:
    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_id(db: Session, user_id: str) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(db: Session, user_in: UserCreateSchema) -> User:
        hashed_password = get_password_hash(user_in.password)
        user = User(
            email=user_in.email,
            password_hash=hashed_password,
            first_name=getattr(user_in, "first_name", None),
            last_name=getattr(user_in, "last_name", None),
            country=getattr(user_in, "country", None),
            city=getattr(user_in, "city", None),
            picture=getattr(user_in, "picture", None),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_user(db: Session, user: User, user_in: UserUpdateSchema) -> User:
        updates = user_in.dict(exclude_unset=True)
        for key, value in updates.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
