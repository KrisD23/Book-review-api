from fastapi import APIRouter, HTTPException
from schemas.book import BookCreate, BookResponse

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)



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

@router.get(
    "/",
    summary="Get all books",
    response_model=list[BookResponse]
)
async def get_books():
    return books


@router.get(
    "/{id}",
    response_model=BookResponse,
)
async def get_book(id: int):
    for book in books:
        if book["id"]==id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@router.post(
    "/",
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


@router.put("/{id}",
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


@router.delete("/{id}",
    summary="Delete a book",
    status_code=204
    
)
async def delete_book(id:int):
    for i, b in enumerate(books):
        if b["id"] ==id:
            books.pop(i)
            return 
    raise HTTPException(status_code=404, detail="Book not found")