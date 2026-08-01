from fastapi import FastAPI


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
)
async def get_books():
    return books


@app.post(
    "/books",
    tags=["Books"],
    summary="Add a new book",
    status_code=201
)
async def add_book(book:dict):
    new_book = {
        "id": len(books) + 1,
        "title": book["title"],
        "author": book["author"],
    }
    books.append(new_book)
    return new_book


@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
)
async def health_check():
    return {"status": "healthy"}