from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.use_cases import (
    CreateNotificationUseCase,
    DeleteNotificationUseCase,
    GetNotificationUseCase,
    ListNotificationsUseCase,
    UpdateNotificationStatusUseCase,
)
from src.domain.enums import DomainEventName
from src.domain.models.domain_event import DomainEvent
from src.infrastructure.events.noop_event_publisher import NoOpEventPublisher
from src.infrastructure.persistence.sqlalchemy.notification_repository import (
    SqlAlchemyNotificationRepository,
)
from src.infrastructure.web.fastapi.dependencies import (
    get_create_notification_use_case,
    get_delete_notification_use_case,
    get_event_publisher,
    get_get_notification_use_case,
    get_list_notifications_use_case,
    get_notification_repository,
    get_update_notification_status_use_case,
)


@pytest.mark.asyncio
async def test_should_return_repository_when_session_is_available() -> None:
    repository = await get_notification_repository(AsyncMock(spec=AsyncSession))

    assert isinstance(repository, SqlAlchemyNotificationRepository)


@pytest.mark.asyncio
async def test_should_return_noop_publisher_when_dependency_is_requested() -> None:
    publisher = get_event_publisher()

    await publisher.publish_event(_domain_event())

    assert isinstance(publisher, NoOpEventPublisher)


def test_should_return_create_use_case_when_dependencies_are_available() -> None:
    use_case = get_create_notification_use_case(AsyncMock(), AsyncMock())

    assert isinstance(use_case, CreateNotificationUseCase)


def test_should_return_get_use_case_when_repository_is_available() -> None:
    use_case = get_get_notification_use_case(AsyncMock())

    assert isinstance(use_case, GetNotificationUseCase)


def test_should_return_list_use_case_when_repository_is_available() -> None:
    use_case = get_list_notifications_use_case(AsyncMock())

    assert isinstance(use_case, ListNotificationsUseCase)


def test_should_return_update_use_case_when_dependencies_are_available() -> None:
    use_case = get_update_notification_status_use_case(AsyncMock(), AsyncMock())

    assert isinstance(use_case, UpdateNotificationStatusUseCase)


def test_should_return_delete_use_case_when_dependencies_are_available() -> None:
    use_case = get_delete_notification_use_case(AsyncMock(), AsyncMock())

    assert isinstance(use_case, DeleteNotificationUseCase)


def _domain_event() -> DomainEvent:
    return DomainEvent(
        event_name=DomainEventName.NOTIFICATION_CREATED,
        aggregate_id=uuid4(),
        payload={"client_id": "client-123"},
    )
