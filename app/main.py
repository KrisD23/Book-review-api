from fastapi import FastAPI, HTTPException
from schemas.book import BookCreate
from schemas.book import BookResponse



app = FastAPI(
    title="Book Review API",
    version="0.1.0",
    description="A REST API for managing books and reviews.",
)


@app.get(
    "/",
    tags=["Root"],
    summary="Root endpoint",
)
async def root():
    return {"message": "Book Review API"}


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

@app.get(
    "/books",
    tags=["Books"],
    summary="Get all books",
    response_model=list[BookResponse]
)
async def get_books():
    return books


@app.get(
    "/books/{id}",
    response_model=BookResponse,
)
async def get_book(id: int):
    for book in books:
        if book["id"]==id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post(
    "/books",
    tags=["Books"],
    summary="Add a new book",
    status_code=201,
    response_model=BookResponse
)
async def add_book(book:BookCreate):
    new_book = {
    "id": len(books) + 1,
    **book.model_dump(),
}
    
    books.append(new_book)
    return new_book


@app.put("/books/{id}",
    tags=["Books"],
    summary="Update a book",
    response_model=BookResponse
)
async def update_book(id: int, book: BookCreate):
    for i, b in enumerate(books):
        if b["id"] == id:
            updated_book = {**b, **book.model_dump()}
            books[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{id}",
    tags=["Books"],
    summary="Delete a book",
    status_code=204
    
)
async def delete_book(id:int):
    for i, b in enumerate(books):
        if b["id"] ==id:
            books.pop(i)
            return 
    raise HTTPException(status_code=404, detail="Book not found")

@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
)
async def health_check():
    return {"status": "healthy"}