from fastapi import HTTPException
from schemas.book import BookCreate
from psycopg import Connection
from schemas.book import BookResponse




books = [
    {
        "id": 1,
        "title": "Atomic Habits",
        "author": "James Clear",
    },
    {
        "id": 2,
        "title": "Clean Code",
        "author": "Robert C. Martin",
    },
]


def get_books(db: Connection, author_name=None, limit=None):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM books")

    rows = cursor.fetchall()
    books = [
    BookResponse(
        id=row[0],
        title=row[1],
        author=row[2],
    )
    for row in rows
]

    return books


def get_book_by_id(id: int):
    for book in books:
        if book["id"] == id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")


def create_book(book: BookCreate):
    new_book = {
        "id": len(books) + 1,
        **book.model_dump(),
    }

    books.append(new_book)
    return new_book


def update_book(id: int, book: BookCreate):
    for i, b in enumerate(books):
        if b["id"] == id:
            updated_book = {**b, **book.model_dump()}
            books[i] = updated_book
            return updated_book

    raise HTTPException(status_code=404, detail="Book not found")


def delete_book(id: int):
    for i, b in enumerate(books):
        if b["id"] == id:
            books.pop(i)
            return

    raise HTTPException(status_code=404, detail="Book not found")