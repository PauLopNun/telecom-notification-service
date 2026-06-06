from src.application.dtos.notification_dtos import (
    CreateNotificationInput,
    NotificationOutput,
    notification_to_output,
)
from src.domain.models.notification import Notification
from src.domain.ports.event_publisher import EventPublisherPort
from src.domain.ports.notification_repository import NotificationRepositoryPort


class CreateNotificationUseCase:
    """Creates a notification and publishes its domain event."""

    def __init__(
        self,
        notification_repository: NotificationRepositoryPort,
        event_publisher: EventPublisherPort,
    ) -> None:
        self._notification_repository = notification_repository
        self._event_publisher = event_publisher

    async def execute(
        self,
        input_data: CreateNotificationInput,
    ) -> NotificationOutput:
        notification = Notification.create(
            client_id=input_data.client_id,
            event_type=input_data.event_type,
            message=input_data.message,
            metadata=input_data.metadata,
        )
        saved_notification = await self._notification_repository.save(notification)
        await self._event_publisher.publish_event(saved_notification.created_event())
        return notification_to_output(saved_notification)
