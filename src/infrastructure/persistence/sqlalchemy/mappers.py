from datetime import UTC, datetime

from src.domain.enums import EventType, NotificationStatus
from src.domain.models.notification import Notification
from src.infrastructure.persistence.sqlalchemy.notification_model import (
    NotificationModel,
)


def to_domain(notification_model: NotificationModel) -> Notification:
    return Notification(
        id=notification_model.id,
        client_id=notification_model.client_id,
        event_type=EventType(notification_model.event_type),
        status=NotificationStatus(notification_model.status),
        message=notification_model.message,
        metadata=notification_model.metadata_,
        created_at=_ensure_utc(notification_model.created_at),
        updated_at=_ensure_utc(notification_model.updated_at),
    )


def to_model(notification: Notification) -> NotificationModel:
    return NotificationModel(
        id=notification.id,
        client_id=notification.client_id,
        event_type=notification.event_type,
        status=notification.status,
        message=notification.message,
        metadata_=notification.metadata,
        created_at=notification.created_at,
        updated_at=notification.updated_at,
    )


def _ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)
