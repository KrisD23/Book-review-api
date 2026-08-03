from fastapi import HTTPException
from schemas.book import BookCreate

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


def get_books(author_name: str | None = None, limit: int | None = None):
    if author_name:
        books_list = [
            book
            for book in books
            if book["author"].lower() == author_name.lower()
        ]
    else:
        books_list = books

    if limit is not None:
        books_list = books_list[:limit]

    return books_list


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