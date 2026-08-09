from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import create_user
from app.services.auth_service import login_user as login_user_service

from fastapi import BackgroundTasks
from app.tasks.email import send_welcome_email


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(user: UserCreate,background_tasks: BackgroundTasks , db: Session = Depends(get_db), ):
    created_user = create_user(user, db)
    background_tasks.add_task(send_welcome_email, email=created_user.email)
    return created_user

@router.post("/login")
async def login_user( db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    return login_user_service(form_data.username, form_data.password, db)