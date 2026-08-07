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


def get_book_by_id(id: int, db: Connection):
    with db.cursor() as cursor:

        cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
        row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse(
        id=row[0],
        title=row[1],
        author=row[2],
    )


def create_book(book: BookCreate, db: Connection):
    with db.cursor() as cursor:
        cursor.execute(
            "INSERT INTO books (title, author) VALUES (%s, %s) RETURNING id",
            (book.title, book.author),
        )
        new_book_id = cursor.fetchone()[0]
        
    db.commit()
    new_book = BookResponse(
        id=new_book_id,
        title=book.title,
        author=book.author,
    )
   
    
    return new_book


def update_book(id: int, book: BookCreate, db: Connection):
    with db.cursor() as cursor:
        cursor.execute(
            "UPDATE books SET title = %s, author = %s WHERE id = %s RETURNING *",
            (book.title, book.author, id),
        )
        updated_row = cursor.fetchone()
    
    if updated_row:
        db.commit()
        return BookResponse(
            id=updated_row[0],
            title=updated_row[1],
            author=updated_row[2],
        )

    raise HTTPException(status_code=404, detail="Book not found")


def delete_book(id: int, db: Connection):
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM books WHERE id = %s RETURNING *", (id,))
        deleted_row = cursor.fetchone()
    
    if deleted_row:
        db.commit()
        return BookResponse(
            id=deleted_row[0],
            title=deleted_row[1],
            author=deleted_row[2],
        )

    raise HTTPException(status_code=404, detail="Book not found")