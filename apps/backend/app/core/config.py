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


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()