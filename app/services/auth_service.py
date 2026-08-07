from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from schemas.user import UserCreate
from models.user import User
from utils.security import hash_password

def create_user(user: UserCreate, db: Session):
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    db.refresh(new_user)
    return new_user