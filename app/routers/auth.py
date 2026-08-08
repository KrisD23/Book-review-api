from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from dependencies.database import get_db
from schemas.user import UserCreate, UserResponse
from services.auth_service import create_user
from services.auth_service import login_user as login_user_service


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

@router.post("/login")
async def login_user( db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    return login_user_service(form_data.username, form_data.password, db)