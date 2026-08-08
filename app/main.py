from fastapi import FastAPI
from exceptions.custom import BookNotFoundError, EmailAlreadyRegisteredError
from routers.books import router as books_router
from routers.auth import router as auth_router
from middleware.logging import logging_middleware
from fastapi.middleware.cors import CORSMiddleware
from exceptions.handlers import book_not_found_handler, email_already_registered_handler, global_exception_handler

app = FastAPI(
    title="Book Review API",
    version="0.1.0",
    description="A REST API for managing books and reviews.",
    
)


app.include_router(books_router)
app.include_router(auth_router)


app.middleware("http")(logging_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_exception_handler(
    Exception,
    global_exception_handler,
)

app.add_exception_handler(
    BookNotFoundError,
    book_not_found_handler,
)

app.add_exception_handler(
    EmailAlreadyRegisteredError,
    email_already_registered_handler,
)

@app.get(
    "/",
    tags=["Root"],
    summary="Root endpoint",
)
async def root():
    return {"message": "Book Review API"}



@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
)
async def health_check():
    return {"status": "healthy"}