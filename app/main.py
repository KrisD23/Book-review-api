from fastapi import FastAPI
from routers.books import router as books_router
from routers.auth import router as auth_router
from middleware.logging import logging_middleware


app = FastAPI(
    title="Book Review API",
    version="0.1.0",
    description="A REST API for managing books and reviews.",
    
)

app.include_router(books_router)
app.include_router(auth_router)

app.middleware("http")(logging_middleware)


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