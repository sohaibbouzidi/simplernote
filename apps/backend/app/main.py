import os
from sqlalchemy import text
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from app.api.routes import api_router
from app.core.config import settings
from app.core.redis_client import init_redis, close_redis, get_redis
from app.core.logging import setup_logging, RequestLoggingMiddleware
from app.core.exceptions import AppException
from app.core.metrics import PrometheusMiddleware, metrics_response
from app.db.session import engine, SessionLocal
from app.models import base

os.makedirs("logs", exist_ok=True)
setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="AI Memory & Task Management API",
)

if settings.SENTRY_DSN:
    import sentry_sdk
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        enable_tracing=True,
        traces_sample_rate=0.1,
    )
    logger.info("Sentry initialized")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(PrometheusMiddleware)

app.include_router(api_router, prefix="/api")


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    rid = getattr(request.state, "request_id", "unknown")
    logger.opt(exception=True).error(f"Unhandled exception [rid={rid}]")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.on_event("startup")
async def startup_event():
    base.Base.metadata.create_all(bind=engine)
    init_redis()
    logger.info("Application started")


@app.on_event("shutdown")
async def shutdown_event():
    close_redis()
    logger.info("Application shutting down")


@app.get("/metrics")
def metrics():
    return metrics_response()


@app.get("/health")
def health_check():
    r = get_redis()
    redis_status = "ok" if r and r.ping() else "unavailable"
    db_status = "unavailable"
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "unavailable"
    finally:
        db.close()
    return {"status": "ok" if redis_status == "ok" and db_status == "ok" else "degraded", "redis": redis_status, "database": db_status}
