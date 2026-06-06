from json import loads

import pytest
from fastapi import Request, status

from src.domain.exceptions import InvalidNotificationDataError
from src.infrastructure.web.fastapi.error_handlers import (
    invalid_notification_data_handler,
)


@pytest.mark.asyncio
async def test_should_return_400_when_notification_data_is_invalid() -> None:
    request = Request({"type": "http"})

    response = await invalid_notification_data_handler(
        request,
        InvalidNotificationDataError("invalid notification data"),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert loads(response.body) == {"detail": "invalid notification data"}
