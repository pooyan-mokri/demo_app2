from __future__ import annotations

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration pulled from environment variables."""

    api_prefix: str = "/api"
    app_name: str = "TheMoak ERP API"
    debug: bool = False

    database_url: str | None = None

    secret_key: str = "super-secret-key-change-me"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7
    algorithm: str = "HS256"

    woo_base_url: str | None = None
    woo_consumer_key: str | None = None
    woo_consumer_secret: str | None = None

    s3_endpoint_url: str | None = None
    s3_access_key: str | None = None
    s3_secret_key: str | None = None
    s3_bucket_name: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="THEMOAK_")


@lru_cache
def get_settings() -> Settings:
    return Settings()
