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


def get_book_by_id(id: int, db: Connection):
    cursor = db.cursor()
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
    cursor = db.cursor()
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