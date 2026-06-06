from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.domain.exceptions import (
    InvalidNotificationDataError,
    NotificationNotFoundError,
)

ERROR_DETAIL_KEY = "detail"


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        NotificationNotFoundError,
        notification_not_found_handler,
    )
    app.add_exception_handler(
        InvalidNotificationDataError,
        invalid_notification_data_handler,
    )


async def notification_not_found_handler(
    request: Request,
    exception: NotificationNotFoundError,
) -> JSONResponse:
    return _error_response(status.HTTP_404_NOT_FOUND, str(exception))


async def invalid_notification_data_handler(
    request: Request,
    exception: InvalidNotificationDataError,
) -> JSONResponse:
    return _error_response(status.HTTP_400_BAD_REQUEST, str(exception))


def _error_response(status_code: int, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={ERROR_DETAIL_KEY: detail},
    )
