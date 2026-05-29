import uuid
import time
from loguru import logger
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


def setup_logging():
    logger.remove()
    logger.add(
        "logs/simplernote.log",
        rotation="10 MB",
        retention="7 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<7} | {extra[request_id]:<36} | {message}",
        enqueue=True,
    )
    logger.add(
        lambda msg: print(msg, end=""),
        level="DEBUG" if __debug__ else "INFO",
        format="<level>{level:<7}</level> | <cyan>{extra[request_id]}</cyan> | {message}",
        colorize=True,
    )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = str(uuid.uuid4())[:8]
        request.state.request_id = rid
        start = time.time()
        with logger.contextualize(request_id=rid):
            logger.info(f"{request.method} {request.url.path}")
            response: Response = await call_next(request)
            elapsed = time.time() - start
            logger.info(f"{request.method} {request.url.path} → {response.status_code} ({elapsed:.3f}s)")
        return response
