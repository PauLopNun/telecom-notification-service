import pytest

from src.application.dtos.notification_dtos import ListNotificationsInput
from src.domain.enums import EventType
from src.domain.exceptions import InvalidNotificationDataError
from src.domain.models.notification import Notification

LIMIT_BELOW_MINIMUM = 0
LIMIT_ABOVE_MAXIMUM = 101
NEGATIVE_OFFSET = -1


@pytest.mark.parametrize("limit", [LIMIT_BELOW_MINIMUM, LIMIT_ABOVE_MAXIMUM])
def test_should_reject_limit_when_value_is_out_of_range(limit: int) -> None:
    with pytest.raises(InvalidNotificationDataError, match="limit must be"):
        ListNotificationsInput(limit=limit)


def test_should_reject_offset_when_value_is_negative() -> None:
    with pytest.raises(InvalidNotificationDataError, match="offset must be"):
        ListNotificationsInput(offset=NEGATIVE_OFFSET)


def test_should_reject_client_id_when_value_is_blank() -> None:
    with pytest.raises(InvalidNotificationDataError, match="client_id"):
        Notification.create(
            client_id=" ",
            event_type=EventType.NETWORK_OUTAGE,
            message="Network outage detected",
        )


def test_should_reject_message_when_value_is_blank() -> None:
    with pytest.raises(InvalidNotificationDataError, match="message"):
        Notification.create(
            client_id="client-123",
            event_type=EventType.NETWORK_OUTAGE,
            message=" ",
        )
