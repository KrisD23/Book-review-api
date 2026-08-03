from fastapi import APIRouter, HTTPException, Query
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
async def get_books(author: str | None = Query(
    default=None,
    min_length=3,
    max_length=100,
    description="Filter books by author name",
    examples=["James Clear", "Robert C. Martin"],
), limit: int | None = Query(
    default=None,
    ge=1,
    le=100,
    description="Limit the number of books returned",
    examples=[5, 10, 20],
)):
    if author:
        books_list = [book for book in books if book["author"].lower() == author.lower()]
    else:
        books_list = books

    if limit is not None:
        books_list = books_list[:limit]

    return books_list


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