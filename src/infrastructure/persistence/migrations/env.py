from logging.config import fileConfig
from os import getenv

from alembic import context
from sqlalchemy import engine_from_config, pool

from src.config.exceptions import ConfigurationError
from src.infrastructure.persistence.sqlalchemy.base import Base
from src.infrastructure.persistence.sqlalchemy.notification_model import (
    NotificationModel,
)

DATABASE_URL_ENV_NAME = "DATABASE_URL"
REGISTERED_MODELS = (NotificationModel,)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_database_url() -> str:
    database_url = getenv(DATABASE_URL_ENV_NAME) or config.get_main_option(
        "sqlalchemy.url"
    )
    if database_url is None or not database_url.strip():
        raise ConfigurationError(f"{DATABASE_URL_ENV_NAME} is required")
    return _normalize_database_url(database_url)


def run_migrations_offline() -> None:
    context.configure(
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_database_url()
    engine = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()


def _normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
