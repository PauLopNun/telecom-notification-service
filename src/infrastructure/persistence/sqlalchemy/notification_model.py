from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PostgreSqlUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.enums import EventType, NotificationStatus
from src.infrastructure.persistence.sqlalchemy.base import Base

CLIENT_ID_MAX_LENGTH = 100
ENUM_MAX_LENGTH = 50
MESSAGE_MAX_LENGTH = 1_000


def _enum_column(enum_class: type[StrEnum]) -> Enum:
    return Enum(
        enum_class,
        values_callable=_enum_values,
        native_enum=False,
        validate_strings=True,
        length=ENUM_MAX_LENGTH,
    )


def _enum_values(enum_class: type[StrEnum]) -> list[str]:
    return [enum_value.value for enum_value in enum_class]


class NotificationModel(Base):
    __tablename__ = "notifications"

    id: Mapped[UUID] = mapped_column(PostgreSqlUUID(as_uuid=True), primary_key=True)
    client_id: Mapped[str] = mapped_column(String(CLIENT_ID_MAX_LENGTH), index=True)
    event_type: Mapped[EventType] = mapped_column(_enum_column(EventType))
    status: Mapped[NotificationStatus] = mapped_column(_enum_column(NotificationStatus))
    message: Mapped[str] = mapped_column(String(MESSAGE_MAX_LENGTH))
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
    )
