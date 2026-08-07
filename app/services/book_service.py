from fastapi import HTTPException
from schemas.book import BookCreate
from psycopg import Connection
from schemas.book import BookResponse

from sqlalchemy import select
from models.book import Book
from sqlalchemy.orm import Session


def get_books(db: Session, author_name=None, limit=None):
    statement = select(Book)

    if author_name:
        statement = statement.where(Book.author == author_name)

    if limit:
        statement = statement.limit(limit)

    result = db.execute(statement)

    books = result.scalars().all()

    return books


def get_book_by_id(id: int, db: Session):
    statement = select(Book).where(Book.id == id)
    result = db.execute(statement)
    book = result.scalar_one_or_none()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


def create_book(book: BookCreate, db: Session):
    new_book = Book(title=book.title, author=book.author)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book
    


def update_book(id: int, book: BookCreate, db: Session):
    statement = select(Book).where(Book.id == id)
    result = db.execute(statement)
    existing_book = result.scalar_one_or_none()
    if existing_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    existing_book.title = book.title
    existing_book.author = book.author
    db.commit()
    db.refresh(existing_book)
    return existing_book


def delete_book(id: int, db: Session):
    statement = select(Book).where(Book.id == id)
    result = db.execute(statement)
    book = result.scalar_one_or_none()
   
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return book