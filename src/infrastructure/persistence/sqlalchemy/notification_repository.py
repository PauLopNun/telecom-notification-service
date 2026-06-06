from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.enums import EventType, NotificationStatus
from src.domain.models.notification import Notification
from src.domain.ports.notification_repository import NotificationRepositoryPort
from src.infrastructure.persistence.sqlalchemy.mappers import to_domain, to_model
from src.infrastructure.persistence.sqlalchemy.notification_model import (
    NotificationModel,
)


class SqlAlchemyNotificationRepository(NotificationRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, notification: Notification) -> Notification:
        notification_model = await self._session.merge(to_model(notification))
        await self._session.commit()
        await self._session.refresh(notification_model)
        return to_domain(notification_model)

    async def get_by_id(self, notification_id: UUID) -> Notification | None:
        notification_model = await self._session.get(NotificationModel, notification_id)
        return to_domain(notification_model) if notification_model else None

    async def list(
        self,
        client_id: str | None,
        event_type: EventType | None,
        status: NotificationStatus | None,
        limit: int,
        offset: int,
    ) -> list[Notification]:
        statement = _build_list_statement(client_id, event_type, status, limit, offset)
        result = await self._session.execute(statement)
        return [to_domain(model) for model in result.scalars().all()]

    async def delete(self, notification_id: UUID) -> None:
        notification_model = await self._session.get(NotificationModel, notification_id)
        if notification_model is None:
            return
        await self._session.delete(notification_model)
        await self._session.commit()


def _build_list_statement(
    client_id: str | None,
    event_type: EventType | None,
    status: NotificationStatus | None,
    limit: int,
    offset: int,
) -> Select[tuple[NotificationModel]]:
    statement = select(NotificationModel)
    statement = _filter_by_client_id(statement, client_id)
    statement = _filter_by_event_type(statement, event_type)
    statement = _filter_by_status(statement, status)
    return (
        statement.order_by(NotificationModel.created_at.desc())
        .limit(limit)
        .offset(offset)
    )


def _filter_by_client_id(
    statement: Select[tuple[NotificationModel]],
    client_id: str | None,
) -> Select[tuple[NotificationModel]]:
    if client_id is None:
        return statement
    return statement.where(NotificationModel.client_id == client_id)


def _filter_by_event_type(
    statement: Select[tuple[NotificationModel]],
    event_type: EventType | None,
) -> Select[tuple[NotificationModel]]:
    if event_type is None:
        return statement
    return statement.where(NotificationModel.event_type == event_type)


def _filter_by_status(
    statement: Select[tuple[NotificationModel]],
    status: NotificationStatus | None,
) -> Select[tuple[NotificationModel]]:
    if status is None:
        return statement
    return statement.where(NotificationModel.status == status)
