"""Module to define all app settings.
"""

import logging
from typing import Any

from functools import lru_cache

from pydantic import BaseSettings, AnyHttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    ENV_NAME: str
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URI: PostgresDsn | None = None

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        case_sensitive = True
        env_file = ".env"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, value: str | list[str]) -> list[str] | str:
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        if isinstance(value, (list, str)):
            return value
        raise ValueError(value)

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, value: str | None, values: dict[str, Any]) -> Any:
        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


@lru_cache
def get_settings() -> Settings:
    """Get settings from .env file.

    Returns:
        Settings: The settings.
    """

    settings = Settings()
    logging.info("Loading settings for: %s" % settings.ENV_NAME)

    return settings


settings = get_settings()
