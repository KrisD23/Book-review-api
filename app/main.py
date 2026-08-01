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


@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
)
async def health_check():
    return {"status": "healthy"}