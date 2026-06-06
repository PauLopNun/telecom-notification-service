from functools import lru_cache
from os import getenv

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict

from src.config.exceptions import ConfigurationError

APP_NAME_ENV_NAME = "APP_NAME"
API_PREFIX_ENV_NAME = "API_PREFIX"
DATABASE_URL_ENV_NAME = "DATABASE_URL"
ENVIRONMENT_ENV_NAME = "ENVIRONMENT"

DEFAULT_API_PREFIX = "/api/v1"
DEFAULT_APP_NAME = "telecom-notification-service"
DEFAULT_ENVIRONMENT = "local"


class Settings(BaseModel):
    app_name: str
    api_prefix: str
    database_url: str
    environment: str

    model_config = ConfigDict(frozen=True)


@lru_cache
def get_settings() -> Settings:
    """Returns validated application settings loaded from the environment."""
    load_dotenv()
    database_url = _normalize_database_url(_get_required_value(DATABASE_URL_ENV_NAME))
    return Settings(
        app_name=getenv(APP_NAME_ENV_NAME, DEFAULT_APP_NAME),
        api_prefix=getenv(API_PREFIX_ENV_NAME, DEFAULT_API_PREFIX),
        database_url=database_url,
        environment=getenv(ENVIRONMENT_ENV_NAME, DEFAULT_ENVIRONMENT),
    )


def _get_required_value(name: str) -> str:
    value = getenv(name)
    if value is None or not value.strip():
        raise ConfigurationError(f"{name} is required")
    return value


def _normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+asyncpg://", 1)
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return database_url
