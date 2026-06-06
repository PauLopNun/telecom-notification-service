import importlib
import sys

from pytest import MonkeyPatch

from src.config.settings import DATABASE_URL_ENV_NAME, DEFAULT_APP_NAME, get_settings

TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/database"


def test_should_create_fastapi_app_when_main_module_is_imported(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setenv(DATABASE_URL_ENV_NAME, TEST_DATABASE_URL)
    get_settings.cache_clear()
    sys.modules.pop("src.main", None)

    main_module = importlib.import_module("src.main")

    assert main_module.app.title == DEFAULT_APP_NAME
    assert main_module.app.docs_url == "/docs"
    assert main_module.app.openapi_url == "/openapi.json"
