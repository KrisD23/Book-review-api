from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from schemas.book import BookCreate
from psycopg import Connection
from schemas.book import BookResponse

from sqlalchemy import select
from models.book import Book
from sqlalchemy.orm import Session


def get_books(db: Session,user_id:int, author_name=None, limit=None):
    statement = select(Book).where(Book.user_id == user_id)

    if author_name:
        statement = statement.where(Book.author == author_name)

    if limit:
        statement = statement.limit(limit)

    result = db.execute(statement)

    books = result.scalars().all()

    return books


def get_book_by_id(book_id : int, db: Session):
    statement = select(Book).where(Book.id == book_id)
    result = db.execute(statement)
    book = result.scalar_one_or_none()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


def create_book(book: BookCreate, db: Session, user_id: int):
    new_book = Book(title=book.title, author=book.author, user_id=user_id)
    db.add(new_book)
    try :
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise 
    db.refresh(new_book)
    return new_book
    


def update_book(book_id : int, book: BookCreate, db: Session):
    statement = select(Book).where(Book.id == book_id)
    result = db.execute(statement)
    existing_book = result.scalar_one_or_none()
    if existing_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    existing_book.title = book.title
    existing_book.author = book.author

    try :
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    
    db.refresh(existing_book)
    return existing_book


def delete_book(book_id : int, db: Session):
    statement = select(Book).where(Book.id == book_id)
    result = db.execute(statement)
    book = result.scalar_one_or_none()
   
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    return book