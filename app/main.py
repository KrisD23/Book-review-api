from fastapi import FastAPI
from routers.books import router

from contextlib import asynccontextmanager
from database.connection import create_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to database...")

    connection = create_connection()

    app.state.db = connection

    print("Database connected!")

    yield

    print("Closing database connection...")

    connection.close()

    print("Database connection closed.")


app = FastAPI(
    title="Book Review API",
    version="0.1.0",
    description="A REST API for managing books and reviews.",
    lifespan=lifespan,
)

app.include_router(router)


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