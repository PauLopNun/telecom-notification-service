import pytest
from pytest import MonkeyPatch

from src.config.exceptions import ConfigurationError
from src.config.settings import DATABASE_URL_ENV_NAME, get_settings


def test_should_use_asyncpg_driver_when_database_url_is_postgres_scheme(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        DATABASE_URL_ENV_NAME,
        "postgres://user:password@localhost:5432/database",
    )
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.database_url.startswith("postgresql+asyncpg://")


def test_should_keep_database_url_when_asyncpg_driver_is_already_defined(
    monkeypatch: MonkeyPatch,
) -> None:
    database_url = "postgresql+asyncpg://user:password@localhost:5432/database"
    monkeypatch.setenv(DATABASE_URL_ENV_NAME, database_url)
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.database_url == database_url


def test_should_use_asyncpg_driver_when_database_url_is_postgresql_scheme(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        DATABASE_URL_ENV_NAME,
        "postgresql://user:password@localhost:5432/database",
    )
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.database_url.startswith("postgresql+asyncpg://")


def test_should_raise_configuration_error_when_database_url_is_blank(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setenv(DATABASE_URL_ENV_NAME, " ")
    get_settings.cache_clear()

    with pytest.raises(ConfigurationError, match="DATABASE_URL is required"):
        get_settings()
