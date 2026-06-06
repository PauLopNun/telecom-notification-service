from unittest.mock import AsyncMock

import pytest

from src.domain.enums import EventType
from src.domain.models.notification import Notification

TEST_CLIENT_ID = "client-123"
TEST_MESSAGE = "Network degradation detected"


@pytest.fixture
def sample_notification() -> Notification:
    return Notification.create(
        client_id=TEST_CLIENT_ID,
        event_type=EventType.SERVICE_DEGRADATION,
        message=TEST_MESSAGE,
        metadata={"region": "north"},
    )


@pytest.fixture
def notification_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def event_publisher() -> AsyncMock:
    return AsyncMock()
