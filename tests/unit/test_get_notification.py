from unittest.mock import AsyncMock

import pytest

from src.application.use_cases.get_notification import GetNotificationUseCase
from src.domain.exceptions import NotificationNotFoundError
from src.domain.models.notification import Notification


@pytest.mark.asyncio
async def test_should_return_notification_when_notification_exists(
    notification_repository: AsyncMock,
    sample_notification: Notification,
) -> None:
    notification_repository.get_by_id.return_value = sample_notification
    use_case = GetNotificationUseCase(notification_repository)

    output = await use_case.execute(sample_notification.id)

    assert output.id == sample_notification.id
    assert output.client_id == sample_notification.client_id


@pytest.mark.asyncio
async def test_should_raise_not_found_when_notification_does_not_exist(
    notification_repository: AsyncMock,
    sample_notification: Notification,
) -> None:
    notification_repository.get_by_id.return_value = None
    use_case = GetNotificationUseCase(notification_repository)

    with pytest.raises(NotificationNotFoundError):
        await use_case.execute(sample_notification.id)
