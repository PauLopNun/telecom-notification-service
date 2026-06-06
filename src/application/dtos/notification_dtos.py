from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID

from src.domain.enums import EventType, NotificationStatus
from src.domain.exceptions import InvalidNotificationDataError
from src.domain.models.notification import Notification

DEFAULT_NOTIFICATION_LIMIT = 50
MAX_NOTIFICATION_LIMIT = 100
MIN_NOTIFICATION_LIMIT = 1
MIN_NOTIFICATION_OFFSET = 0


@dataclass(frozen=True, slots=True)
class CreateNotificationInput:
    client_id: str
    event_type: EventType
    message: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ListNotificationsInput:
    client_id: str | None = None
    event_type: EventType | None = None
    status: NotificationStatus | None = None
    limit: int = DEFAULT_NOTIFICATION_LIMIT
    offset: int = MIN_NOTIFICATION_OFFSET

    def __post_init__(self) -> None:
        _validate_limit(self.limit)
        _validate_offset(self.offset)


@dataclass(frozen=True, slots=True)
class UpdateNotificationStatusInput:
    status: NotificationStatus


@dataclass(frozen=True, slots=True)
class NotificationOutput:
    id: UUID
    client_id: str
    event_type: EventType
    status: NotificationStatus
    message: str
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime


def notification_to_output(notification: Notification) -> NotificationOutput:
    return NotificationOutput(
        id=notification.id,
        client_id=notification.client_id,
        event_type=notification.event_type,
        status=notification.status,
        message=notification.message,
        metadata=notification.metadata,
        created_at=notification.created_at,
        updated_at=notification.updated_at,
    )


def _validate_limit(limit: int) -> None:
    if limit < MIN_NOTIFICATION_LIMIT or limit > MAX_NOTIFICATION_LIMIT:
        raise InvalidNotificationDataError("limit must be between 1 and 100")


def _validate_offset(offset: int) -> None:
    if offset < MIN_NOTIFICATION_OFFSET:
        raise InvalidNotificationDataError("offset must be greater than or equal to 0")
