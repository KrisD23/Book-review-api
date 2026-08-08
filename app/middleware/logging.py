import time
from fastapi import Request
import logging


logger = logging.getLogger("app.request")
logger.setLevel(logging.INFO)


async def logging_middleware(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    logger.info(
    "%s %s - %s - %.4fs",
    request.method,
    request.url.path,
    response.status_code,
    process_time,
    )

    return response