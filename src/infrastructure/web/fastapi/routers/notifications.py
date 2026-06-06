from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from src.application.dtos.notification_dtos import (
    DEFAULT_NOTIFICATION_LIMIT,
    ListNotificationsInput,
    MAX_NOTIFICATION_LIMIT,
    MIN_NOTIFICATION_LIMIT,
    MIN_NOTIFICATION_OFFSET,
)
from src.application.use_cases import (
    CreateNotificationUseCase,
    DeleteNotificationUseCase,
    GetNotificationUseCase,
    ListNotificationsUseCase,
    UpdateNotificationStatusUseCase,
)
from src.domain.enums import EventType, NotificationStatus
from src.infrastructure.web.fastapi.dependencies import (
    get_create_notification_use_case,
    get_delete_notification_use_case,
    get_get_notification_use_case,
    get_list_notifications_use_case,
    get_update_notification_status_use_case,
)
from src.infrastructure.web.fastapi.schemas import (
    CreateNotificationRequest,
    NotificationResponse,
    UpdateNotificationStatusRequest,
    to_create_input,
    to_response,
    to_update_input,
)

router = APIRouter(prefix="/notifications", tags=["notifications"])

ClientIdQuery = Annotated[str | None, Query()]
EventTypeQuery = Annotated[EventType | None, Query()]
StatusQuery = Annotated[NotificationStatus | None, Query(alias="status")]
LimitQuery = Annotated[int, Query(ge=MIN_NOTIFICATION_LIMIT, le=MAX_NOTIFICATION_LIMIT)]
OffsetQuery = Annotated[int, Query(ge=MIN_NOTIFICATION_OFFSET)]


@router.post(
    "",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_notification(
    request: CreateNotificationRequest,
    use_case: CreateNotificationUseCase = Depends(get_create_notification_use_case),
) -> NotificationResponse:
    output = await use_case.execute(to_create_input(request))
    return to_response(output)


@router.get("", response_model=list[NotificationResponse])
async def list_notifications(
    client_id: ClientIdQuery = None,
    event_type: EventTypeQuery = None,
    notification_status: StatusQuery = None,
    limit: LimitQuery = DEFAULT_NOTIFICATION_LIMIT,
    offset: OffsetQuery = MIN_NOTIFICATION_OFFSET,
    use_case: ListNotificationsUseCase = Depends(get_list_notifications_use_case),
) -> list[NotificationResponse]:
    input_data = ListNotificationsInput(
        client_id=client_id,
        event_type=event_type,
        status=notification_status,
        limit=limit,
        offset=offset,
    )
    outputs = await use_case.execute(input_data)
    # TODO: add pagination metadata to response headers.
    return [to_response(output) for output in outputs]


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: UUID,
    use_case: GetNotificationUseCase = Depends(get_get_notification_use_case),
) -> NotificationResponse:
    output = await use_case.execute(notification_id)
    return to_response(output)


@router.patch("/{notification_id}/status", response_model=NotificationResponse)
async def update_notification_status(
    notification_id: UUID,
    request: UpdateNotificationStatusRequest,
    use_case: UpdateNotificationStatusUseCase = Depends(
        get_update_notification_status_use_case
    ),
) -> NotificationResponse:
    output = await use_case.execute(notification_id, to_update_input(request))
    return to_response(output)


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: UUID,
    use_case: DeleteNotificationUseCase = Depends(get_delete_notification_use_case),
) -> None:
    await use_case.execute(notification_id)
