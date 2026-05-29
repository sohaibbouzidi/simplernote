from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from pydantic import PostgresDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "simplernote"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    DATABASE_URL: PostgresDsn
    REDIS_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440

    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    SENTRY_DSN: Optional[str] = None
    S3_ENDPOINT_URL: Optional[str] = None
    S3_PUBLIC_ENDPOINT: Optional[str] = None
    S3_ACCESS_KEY_ID: Optional[str] = None
    S3_SECRET_ACCESS_KEY: Optional[str] = None
    S3_BUCKET_NAME: Optional[str] = None
    S3_REGION: Optional[str] = None
    S3_USE_SSL: Optional[bool] = False
    # Profile picture validation
    # Max size in bytes (default 5 MB)
    MAX_PROFILE_PIC_SIZE_BYTES: int = 5 * 1024 * 1024
    # Allowed content types for profile images
    ALLOWED_IMAGE_CONTENT_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()