from fastapi import Request
from fastapi.responses import JSONResponse
import logging

from exceptions.custom import BookNotFoundError, EmailAlreadyRegisteredError

logger = logging.getLogger("uvicorn.error")

async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
    "Unhandled exception on %s %s",
    request.method,
    request.url.path,
    exc_info=exc,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error."},
    )


async def book_not_found_handler(
    request: Request,
    exc: BookNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": "Book not found"},
    )

async def email_already_registered_handler(
    request: Request,
    exc: EmailAlreadyRegisteredError,
):
    return JSONResponse(
        status_code=400,
        content={"detail": "Email already registered"},
    )