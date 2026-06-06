import pytest
from pytest import MonkeyPatch

from src.config import database as database_module
from src.config.settings import DATABASE_URL_ENV_NAME, get_settings

TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/database"


@pytest.mark.asyncio
async def test_should_create_session_factory_when_database_url_is_configured(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setenv(DATABASE_URL_ENV_NAME, TEST_DATABASE_URL)
    _clear_database_caches()

    engine = database_module.get_engine()
    session_factory = database_module.get_session_factory()

    assert engine.url.drivername == "postgresql+asyncpg"
    assert session_factory.kw["expire_on_commit"] is False
    await engine.dispose()
    _clear_database_caches()


@pytest.mark.asyncio
async def test_should_yield_session_when_database_session_is_requested(
    monkeypatch: MonkeyPatch,
) -> None:
    context = FakeSessionContext()
    monkeypatch.setattr(
        database_module,
        "get_session_factory",
        lambda: FakeSessionFactory(context),
    )

    session_generator = database_module.get_database_session()
    session = await anext(session_generator)
    await session_generator.aclose()

    assert session == "database-session"
    assert context.exited is True


class FakeSessionContext:
    def __init__(self) -> None:
        self.exited = False

    async def __aenter__(self) -> str:
        return "database-session"

    async def __aexit__(
        self,
        exception_type: object,
        exception: object,
        traceback: object,
    ) -> None:
        self.exited = True


class FakeSessionFactory:
    def __init__(self, context: FakeSessionContext) -> None:
        self._context = context

    def __call__(self) -> FakeSessionContext:
        return self._context


def _clear_database_caches() -> None:
    database_module.get_engine.cache_clear()
    database_module.get_session_factory.cache_clear()
    get_settings.cache_clear()
