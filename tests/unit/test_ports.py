from uuid import UUID, uuid4

import pytest

from src.domain.enums import DomainEventName, EventType, NotificationStatus
from src.domain.models.domain_event import DomainEvent
from src.domain.models.notification import Notification
from src.domain.ports.event_publisher import EventPublisherPort
from src.domain.ports.notification_repository import NotificationRepositoryPort


@pytest.mark.asyncio
async def test_should_raise_not_implemented_for_repository_methods() -> None:
    repository = ConcreteNotificationRepository()
    notification = _notification()

    with pytest.raises(NotImplementedError):
        await repository.save(notification)
    with pytest.raises(NotImplementedError):
        await repository.get_by_id(notification.id)
    with pytest.raises(NotImplementedError):
        await repository.list(None, None, None, 10, 0)
    with pytest.raises(NotImplementedError):
        await repository.delete(notification.id)


@pytest.mark.asyncio
async def test_should_raise_not_implemented_when_event_publisher_is_called() -> None:
    publisher = ConcreteEventPublisher()

    with pytest.raises(NotImplementedError):
        await publisher.publish_event(_domain_event())


class ConcreteNotificationRepository(NotificationRepositoryPort):
    async def save(self, notification: Notification) -> Notification:
        return await super().save(notification)

    async def get_by_id(self, notification_id: UUID) -> Notification | None:
        return await super().get_by_id(notification_id)

    async def list(
        self,
        client_id: str | None,
        event_type: EventType | None,
        status: NotificationStatus | None,
        limit: int,
        offset: int,
    ) -> list[Notification]:
        return await super().list(client_id, event_type, status, limit, offset)

    async def delete(self, notification_id: UUID) -> None:
        await super().delete(notification_id)


class ConcreteEventPublisher(EventPublisherPort):
    async def publish_event(self, event: DomainEvent) -> None:
        await super().publish_event(event)


def _notification() -> Notification:
    return Notification.create(
        client_id="client-123",
        event_type=EventType.NETWORK_OUTAGE,
        message="Network outage detected",
    )


def _domain_event() -> DomainEvent:
    return DomainEvent(
        event_name=DomainEventName.NOTIFICATION_CREATED,
        aggregate_id=uuid4(),
        payload={"client_id": "client-123"},
    )
