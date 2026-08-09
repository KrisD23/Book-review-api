from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.exceptions.custom import EmailAlreadyRegisteredError
from app.schemas.user import UserCreate
from app.models.user import User
from app.utils.security import create_access_token, hash_password, verify_password
from fastapi import HTTPException


def create_user(user: UserCreate, db: Session):
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise EmailAlreadyRegisteredError()
    
    except SQLAlchemyError:
        db.rollback()
        raise
    db.refresh(new_user)
    return new_user

def login_user(email: str, password: str, db: Session):
    statement = select(User).where(User.email == email)
    result = db.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
    