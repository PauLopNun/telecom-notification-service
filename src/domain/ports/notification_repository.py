from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.enums import EventType, NotificationStatus
from src.domain.models.notification import Notification


class NotificationRepositoryPort(ABC):
    """Persists and retrieves notifications."""

    @abstractmethod
    async def save(self, notification: Notification) -> Notification:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, notification_id: UUID) -> Notification | None:
        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
        client_id: str | None,
        event_type: EventType | None,
        status: NotificationStatus | None,
        limit: int,
        offset: int,
    ) -> list[Notification]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, notification_id: UUID) -> None:
        raise NotImplementedError
