from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from src.application.dtos.notification_dtos import (
    CreateNotificationInput,
    NotificationOutput,
    UpdateNotificationStatusInput,
)
from src.domain.enums import EventType, NotificationStatus

CLIENT_ID_MAX_LENGTH = 100
MESSAGE_MAX_LENGTH = 1_000


class CreateNotificationRequest(BaseModel):
    client_id: str = Field(min_length=1, max_length=CLIENT_ID_MAX_LENGTH)
    event_type: EventType
    message: str = Field(min_length=1, max_length=MESSAGE_MAX_LENGTH)
    metadata: dict[str, Any] = Field(default_factory=dict)


class UpdateNotificationStatusRequest(BaseModel):
    status: NotificationStatus


class NotificationResponse(BaseModel):
    id: UUID
    client_id: str
    event_type: EventType
    status: NotificationStatus
    message: str
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime


def to_create_input(request: CreateNotificationRequest) -> CreateNotificationInput:
    return CreateNotificationInput(
        client_id=request.client_id,
        event_type=request.event_type,
        message=request.message,
        metadata=request.metadata,
    )


def to_update_input(
    request: UpdateNotificationStatusRequest,
) -> UpdateNotificationStatusInput:
    return UpdateNotificationStatusInput(status=request.status)


def to_response(output: NotificationOutput) -> NotificationResponse:
    return NotificationResponse(
        id=output.id,
        client_id=output.client_id,
        event_type=output.event_type,
        status=output.status,
        message=output.message,
        metadata=output.metadata,
        created_at=output.created_at,
        updated_at=output.updated_at,
    )
