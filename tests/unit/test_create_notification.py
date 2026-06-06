from unittest.mock import AsyncMock

import pytest

from src.application.dtos.notification_dtos import CreateNotificationInput
from src.application.use_cases.create_notification import CreateNotificationUseCase
from src.domain.enums import EventType
from tests.conftest import TEST_CLIENT_ID, TEST_MESSAGE


@pytest.mark.asyncio
async def test_should_create_notification_when_input_is_valid(
    notification_repository: AsyncMock,
    event_publisher: AsyncMock,
) -> None:
    input_data = CreateNotificationInput(
        client_id=TEST_CLIENT_ID,
        event_type=EventType.SERVICE_DEGRADATION,
        message=TEST_MESSAGE,
        metadata={"region": "north"},
    )
    notification_repository.save.side_effect = _return_first_argument
    use_case = CreateNotificationUseCase(notification_repository, event_publisher)

    output = await use_case.execute(input_data)

    assert output.client_id == TEST_CLIENT_ID
    assert output.event_type == EventType.SERVICE_DEGRADATION
    notification_repository.save.assert_awaited_once()
    event_publisher.publish_event.assert_awaited_once()


async def _return_first_argument(notification: object) -> object:
    return notification
