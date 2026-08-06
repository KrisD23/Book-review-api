from fastapi import APIRouter, Query, Depends
from dependencies.database import get_db
from fastapi import Depends
from psycopg import Connection

from schemas.book import BookCreate, BookResponse
from services import book_service

router = APIRouter(
    prefix="/books",
    tags=["Books"],
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
    limit: int | None = Query(
        default=None,
        ge=1,
        le=100,
        description="Limit the number of books returned",
        examples=[5, 10, 20],
    ),
    db: Connection = Depends(get_db),
):
    return book_service.get_books(
    db=db,
    author_name=author_name,
    limit=limit,
)


@router.get(
    "/{id}",
    response_model=BookResponse,
)
async def get_book(id: int, db: Connection = Depends(get_db)):
    return book_service.get_book_by_id(id=id, db=db)


@router.post(
    "/",
    summary="Add a new book",
    status_code=201,
    response_model=BookResponse,
)
async def add_book(book: BookCreate, db: Connection = Depends(get_db)):
    return book_service.create_book(book=book, db=db)


@router.put(
    "/{id}",
    summary="Update a book",
    response_model=BookResponse,
)
async def update_book(id: int, book: BookCreate):
    return book_service.update_book(id, book)


@router.delete(
    "/{id}",
    summary="Delete a book",
    status_code=204,
)
async def delete_book(id: int):
    return book_service.delete_book(id)