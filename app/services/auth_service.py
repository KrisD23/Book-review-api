from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from sqlalchemy.orm import Session
from schemas.user import UserCreate
from models.user import User
from utils.security import hash_password
from fastapi import HTTPException


def create_user(user: UserCreate, db: Session):
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    
    except SQLAlchemyError:
        db.rollback()
        raise
    db.refresh(new_user)
    return new_user