from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies.database import get_db
from schemas.user import UserCreate, UserLogin, UserResponse
from services.auth_service import create_user
from services.auth_service import login_user as login_user_service


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    return login_user_service(user.email, user.password, db)