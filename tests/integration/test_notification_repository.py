from collections.abc import AsyncGenerator, Generator
from os import getenv
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from src.domain.enums import EventType, NotificationStatus
from src.domain.models.notification import Notification
from src.infrastructure.persistence.sqlalchemy.base import Base
from src.infrastructure.persistence.sqlalchemy.notification_repository import (
    SqlAlchemyNotificationRepository,
)

TEST_DATABASE_URL_ENV_NAME = "TEST_DATABASE_URL"
POSTGRES_IMAGE = "postgres:16-alpine"


@pytest.fixture
def database_url() -> Generator[str, None, None]:
    configured_url = getenv(TEST_DATABASE_URL_ENV_NAME)
    if configured_url is not None:
        yield configured_url
        return
    with PostgresContainer(POSTGRES_IMAGE) as postgres:
        yield _to_async_database_url(postgres.get_connection_url())


@pytest_asyncio.fixture
async def session(database_url: str) -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(database_url)
    await _reset_database(engine)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as database_session:
        yield database_session
    await engine.dispose()


@pytest.mark.asyncio
async def test_should_save_notification_when_repository_save_is_called(
    session: AsyncSession,
) -> None:
    repository = SqlAlchemyNotificationRepository(session)
    notification = _build_notification()

    saved_notification = await repository.save(notification)

    assert saved_notification.id == notification.id


@pytest.mark.asyncio
async def test_should_return_notification_when_id_exists(
    session: AsyncSession,
) -> None:
    repository = SqlAlchemyNotificationRepository(session)
    saved_notification = await repository.save(_build_notification())

    found_notification = await repository.get_by_id(saved_notification.id)

    assert found_notification is not None
    assert found_notification.client_id == saved_notification.client_id


@pytest.mark.asyncio
async def test_should_filter_notifications_when_filters_are_provided(
    session: AsyncSession,
) -> None:
    repository = SqlAlchemyNotificationRepository(session)
    saved_notification = await repository.save(_build_notification())

    notifications = await repository.list(
        client_id=saved_notification.client_id,
        event_type=EventType.NETWORK_OUTAGE,
        status=NotificationStatus.PENDING,
        limit=10,
        offset=0,
    )

    assert [notification.id for notification in notifications] == [
        saved_notification.id,
    ]


@pytest.mark.asyncio
async def test_should_list_notifications_when_filters_are_not_provided(
    session: AsyncSession,
) -> None:
    repository = SqlAlchemyNotificationRepository(session)
    saved_notification = await repository.save(_build_notification())

    notifications = await repository.list(
        client_id=None,
        event_type=None,
        status=None,
        limit=10,
        offset=0,
    )

    assert [notification.id for notification in notifications] == [
        saved_notification.id,
    ]


@pytest.mark.asyncio
async def test_should_delete_notification_when_id_exists(
    session: AsyncSession,
) -> None:
    repository = SqlAlchemyNotificationRepository(session)
    saved_notification = await repository.save(_build_notification())

    await repository.delete(saved_notification.id)

    assert await repository.get_by_id(saved_notification.id) is None


@pytest.mark.asyncio
async def test_should_ignore_delete_when_notification_does_not_exist(
    session: AsyncSession,
) -> None:
    repository = SqlAlchemyNotificationRepository(session)

    await repository.delete(uuid4())

    assert await repository.list(None, None, None, 10, 0) == []


async def _reset_database(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


def _build_notification() -> Notification:
    return Notification.create(
        client_id="client-456",
        event_type=EventType.NETWORK_OUTAGE,
        message="Network outage detected",
        metadata={"region": "south"},
    )


def _to_async_database_url(database_url: str) -> str:
    return database_url.replace("postgresql://", "postgresql+asyncpg://")
