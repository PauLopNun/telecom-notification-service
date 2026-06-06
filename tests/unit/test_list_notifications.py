from unittest.mock import AsyncMock

import pytest

from src.application.dtos.notification_dtos import ListNotificationsInput
from src.application.use_cases.list_notifications import ListNotificationsUseCase
from src.domain.enums import EventType, NotificationStatus
from src.domain.models.notification import Notification


@pytest.mark.asyncio
async def test_should_return_filtered_notifications_when_filters_are_provided(
    notification_repository: AsyncMock,
    sample_notification: Notification,
) -> None:
    notification_repository.list.return_value = [sample_notification]
    use_case = ListNotificationsUseCase(notification_repository)
    input_data = ListNotificationsInput(
        client_id=sample_notification.client_id,
        event_type=EventType.SERVICE_DEGRADATION,
        status=NotificationStatus.PENDING,
    )

    output = await use_case.execute(input_data)

    assert len(output) == 1
    assert output[0].id == sample_notification.id
    notification_repository.list.assert_awaited_once()
