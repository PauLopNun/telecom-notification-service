from uuid import UUID

from src.application.dtos.notification_dtos import (
    NotificationOutput,
    notification_to_output,
)
from src.domain.exceptions import NotificationNotFoundError
from src.domain.ports.notification_repository import NotificationRepositoryPort


class GetNotificationUseCase:
    """Returns one notification by its identifier."""

    def __init__(self, notification_repository: NotificationRepositoryPort) -> None:
        self._notification_repository = notification_repository

    async def execute(self, notification_id: UUID) -> NotificationOutput:
        notification = await self._notification_repository.get_by_id(notification_id)
        if notification is None:
            raise NotificationNotFoundError("notification not found")
        return notification_to_output(notification)
