from datetime import UTC, datetime
from uuid import uuid4

from src.domain.enums import EventType, NotificationStatus
from src.infrastructure.persistence.sqlalchemy.mappers import to_domain
from src.infrastructure.persistence.sqlalchemy.notification_model import (
    NotificationModel,
)


def test_should_convert_naive_datetimes_to_utc_when_mapping_to_domain() -> None:
    notification_model = NotificationModel(
        id=uuid4(),
        client_id="client-123",
        event_type=EventType.NETWORK_OUTAGE,
        status=NotificationStatus.PENDING,
        message="Network outage detected",
        metadata_={"region": "north"},
        created_at=datetime(2026, 1, 1, 10, 0, 0),
        updated_at=datetime(2026, 1, 1, 10, 5, 0),
    )

    notification = to_domain(notification_model)

    assert notification.created_at.tzinfo == UTC
    assert notification.updated_at.tzinfo == UTC
