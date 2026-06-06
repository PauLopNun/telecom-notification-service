from uuid import UUID

from src.domain.exceptions import NotificationNotFoundError
from src.domain.ports.event_publisher import EventPublisherPort
from src.domain.ports.notification_repository import NotificationRepositoryPort


class DeleteNotificationUseCase:
    """Deletes an existing notification."""

    def __init__(
        self,
        notification_repository: NotificationRepositoryPort,
        event_publisher: EventPublisherPort,
    ) -> None:
        self._notification_repository = notification_repository
        self._event_publisher = event_publisher

    async def execute(self, notification_id: UUID) -> None:
        notification = await self._notification_repository.get_by_id(notification_id)
        if notification is None:
            raise NotificationNotFoundError("notification not found")
        await self._notification_repository.delete(notification_id)
        await self._event_publisher.publish_event(notification.deleted_event())
