from fastapi import APIRouter, Query, Depends
from dependencies.auth import get_current_user
from dependencies.database import get_db
from sqlalchemy.orm import Session
from schemas.book import BookCreate, BookResponse
from services import book_service
from models.user import User

router = APIRouter(
    prefix="/books",
    tags=["Books"],
    dependencies=[Depends(get_current_user)]
)


@router.get(
    "/",
    summary="Get all books",
    response_model=list[BookResponse],
)
async def get_books(
    author_name: str | None = Query(
        default=None,
        min_length=3,
        max_length=100,
        description="Filter books by author name",
        examples=["James Clear", "Robert C. Martin"],
        alias="author",
    ),
    limit: int = Query(
    default=20,
    ge=1,
    le=100,
    description="Number of books to return",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of books to skip",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    
):
    return book_service.get_books(
    db=db,
    author_name=author_name,
    limit=limit,
    offset=offset,
    user_id=current_user.id
)


@router.get(
    "/{id}",
    response_model=BookResponse,

)
async def get_book(id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return book_service.get_book_by_id(book_id=id, db=db, user_id=current_user.id)


@router.post(
    "/",
    summary="Add a new book",
    status_code=201,
    response_model=BookResponse,
)
async def add_book(book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return book_service.create_book(book=book, db=db, user_id=current_user.id)


@router.put(
    "/{id}",
    summary="Update a book",
    response_model=BookResponse,
)
async def update_book(id: int, book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return book_service.update_book(book_id=id, book=book, db=db, user_id=current_user.id)


@router.delete(
    "/{id}",
    summary="Delete a book",
    status_code=204,
)
async def delete_book(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return book_service.delete_book(book_id=id, db=db, user_id=current_user.id)