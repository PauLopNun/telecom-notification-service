from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from src.domain.enums import DomainEventName, EventType, NotificationStatus
from src.domain.exceptions import InvalidNotificationDataError
from src.domain.models.domain_event import DomainEvent


@dataclass(slots=True)
class Notification:
    id: UUID = field(default_factory=uuid4)
    client_id: str = ""
    event_type: EventType = EventType.NETWORK_OUTAGE
    status: NotificationStatus = NotificationStatus.PENDING
    message: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        _ensure_not_blank(self.client_id, "client_id")
        _ensure_not_blank(self.message, "message")

    @classmethod
    def create(
        cls,
        client_id: str,
        event_type: EventType,
        message: str,
        metadata: dict[str, Any] | None = None,
    ) -> "Notification":
        created_at = datetime.now(UTC)
        return cls(
            client_id=client_id,
            event_type=event_type,
            message=message,
            metadata=metadata or {},
            created_at=created_at,
            updated_at=created_at,
        )

    def update_status(self, status: NotificationStatus) -> None:
        self.status = status
        self.updated_at = datetime.now(UTC)

    def created_event(self) -> DomainEvent:
        return self._build_event(DomainEventName.NOTIFICATION_CREATED)

    def status_updated_event(self) -> DomainEvent:
        return self._build_event(DomainEventName.NOTIFICATION_STATUS_UPDATED)

    def deleted_event(self) -> DomainEvent:
        return self._build_event(DomainEventName.NOTIFICATION_DELETED)

    def _build_event(self, event_name: DomainEventName) -> DomainEvent:
        return DomainEvent(
            event_name=event_name,
            aggregate_id=self.id,
            payload={"client_id": self.client_id, "status": self.status.value},
        )


def _ensure_not_blank(value: str, field_name: str) -> None:
    if not value.strip():
        raise InvalidNotificationDataError(f"{field_name} must not be blank")
