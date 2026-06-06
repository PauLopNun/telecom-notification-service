from unittest.mock import AsyncMock

import pytest

from src.application.use_cases.delete_notification import DeleteNotificationUseCase
from src.domain.exceptions import NotificationNotFoundError
from src.domain.models.notification import Notification


@pytest.mark.asyncio
async def test_should_delete_notification_when_notification_exists(
    notification_repository: AsyncMock,
    event_publisher: AsyncMock,
    sample_notification: Notification,
) -> None:
    notification_repository.get_by_id.return_value = sample_notification
    use_case = DeleteNotificationUseCase(notification_repository, event_publisher)

    await use_case.execute(sample_notification.id)

    notification_repository.delete.assert_awaited_once_with(sample_notification.id)
    event_publisher.publish_event.assert_awaited_once()


@pytest.mark.asyncio
async def test_should_raise_not_found_when_notification_is_absent(
    notification_repository: AsyncMock,
    event_publisher: AsyncMock,
    sample_notification: Notification,
) -> None:
    notification_repository.get_by_id.return_value = None
    use_case = DeleteNotificationUseCase(notification_repository, event_publisher)

    with pytest.raises(NotificationNotFoundError):
        await use_case.execute(sample_notification.id)
