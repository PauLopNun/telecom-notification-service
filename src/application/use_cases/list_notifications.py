from src.application.dtos.notification_dtos import (
    ListNotificationsInput,
    NotificationOutput,
    notification_to_output,
)
from src.domain.ports.notification_repository import NotificationRepositoryPort


class ListNotificationsUseCase:
    """Lists notifications using optional filters and pagination."""

    def __init__(self, notification_repository: NotificationRepositoryPort) -> None:
        self._notification_repository = notification_repository

    async def execute(
        self,
        input_data: ListNotificationsInput,
    ) -> list[NotificationOutput]:
        notifications = await self._notification_repository.list(
            client_id=input_data.client_id,
            event_type=input_data.event_type,
            status=input_data.status,
            limit=input_data.limit,
            offset=input_data.offset,
        )
        return [notification_to_output(notification) for notification in notifications]
