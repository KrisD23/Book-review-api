from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.custom import BookNotFoundError
from app.schemas.book import BookCreate
from psycopg import Connection
from app.schemas.book import BookResponse
from sqlalchemy import or_

from sqlalchemy import select
from app.models.book import Book
from sqlalchemy.orm import Session


def get_books(db: Session,user_id:int,limit: int, sort_by: str, sort_order: str, offset: int, author_name=None, search: str | None = None):
    statement = select(Book).where(Book.user_id == user_id)


    if author_name:
        statement = statement.where(Book.author == author_name)

    if search:
        pattern = f"%{search}%"

        statement = statement.where(
            or_(
                Book.title.ilike(pattern),
                Book.author.ilike(pattern),
            )
        )

    sort_columns = {
        "id": Book.id,
        "title": Book.title,
        "author": Book.author,
    }

    sort_column = sort_columns[sort_by]

    if sort_order == "desc":
        statement = statement.order_by(sort_column.desc())
    else:
        statement = statement.order_by(sort_column.asc())

    statement = statement.offset(offset).limit(limit)

    result = db.execute(statement)

    books = result.scalars().all()

    return books


def get_book_by_id(book_id : int, db: Session, user_id: int):
    statement = select(Book).where(Book.id == book_id, Book.user_id == user_id)
    result = db.execute(statement)
    book = result.scalar_one_or_none()

    if book is None:
        raise BookNotFoundError()

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
    


def update_book(book_id : int, book: BookCreate, db: Session, user_id: int):
    statement = select(Book).where(Book.id == book_id, Book.user_id == user_id)
    result = db.execute(statement)
    existing_book = result.scalar_one_or_none()
    if existing_book is None:
        raise BookNotFoundError()
    existing_book.title = book.title
    existing_book.author = book.author

    try :
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    
    db.refresh(existing_book)
    return existing_book


def delete_book(book_id : int, db: Session, user_id: int):
    statement = select(Book).where(Book.id == book_id, Book.user_id == user_id)
    result = db.execute(statement)
    book = result.scalar_one_or_none()
   
    if book is None:
        raise BookNotFoundError()

    db.delete(book)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    