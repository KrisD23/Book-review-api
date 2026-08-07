from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies.database import get_db
from schemas.user import UserCreate, UserResponse
from services.auth_service import create_user


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)
   