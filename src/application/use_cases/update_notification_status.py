from uuid import UUID

from src.application.dtos.notification_dtos import (
    NotificationOutput,
    UpdateNotificationStatusInput,
    notification_to_output,
)
from src.domain.exceptions import NotificationNotFoundError
from src.domain.ports.event_publisher import EventPublisherPort
from src.domain.ports.notification_repository import NotificationRepositoryPort


class UpdateNotificationStatusUseCase:
    """Updates the status of an existing notification."""

    def __init__(
        self,
        notification_repository: NotificationRepositoryPort,
        event_publisher: EventPublisherPort,
    ) -> None:
        self._notification_repository = notification_repository
        self._event_publisher = event_publisher

    async def execute(
        self,
        notification_id: UUID,
        input_data: UpdateNotificationStatusInput,
    ) -> NotificationOutput:
        notification = await self._notification_repository.get_by_id(notification_id)
        if notification is None:
            raise NotificationNotFoundError("notification not found")
        notification.update_status(input_data.status)
        saved_notification = await self._notification_repository.save(notification)
        await self._event_publisher.publish_event(
            saved_notification.status_updated_event()
        )
        return notification_to_output(saved_notification)
