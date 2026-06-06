from unittest.mock import AsyncMock

import pytest

from src.application.dtos.notification_dtos import UpdateNotificationStatusInput
from src.application.use_cases.update_notification_status import (
    UpdateNotificationStatusUseCase,
)
from src.domain.enums import NotificationStatus
from src.domain.exceptions import NotificationNotFoundError
from src.domain.models.notification import Notification


@pytest.mark.asyncio
async def test_should_update_status_when_notification_exists(
    notification_repository: AsyncMock,
    event_publisher: AsyncMock,
    sample_notification: Notification,
) -> None:
    notification_repository.get_by_id.return_value = sample_notification
    notification_repository.save.side_effect = _return_first_argument
    use_case = UpdateNotificationStatusUseCase(
        notification_repository,
        event_publisher,
    )

    output = await use_case.execute(
        sample_notification.id,
        UpdateNotificationStatusInput(status=NotificationStatus.SENT),
    )

    assert output.status == NotificationStatus.SENT
    notification_repository.save.assert_awaited_once()
    event_publisher.publish_event.assert_awaited_once()


@pytest.mark.asyncio
async def test_should_raise_not_found_when_notification_is_missing(
    notification_repository: AsyncMock,
    event_publisher: AsyncMock,
    sample_notification: Notification,
) -> None:
    notification_repository.get_by_id.return_value = None
    use_case = UpdateNotificationStatusUseCase(notification_repository, event_publisher)

    with pytest.raises(NotificationNotFoundError):
        await use_case.execute(
            sample_notification.id,
            UpdateNotificationStatusInput(status=NotificationStatus.SENT),
        )


async def _return_first_argument(notification: object) -> object:
    return notification
