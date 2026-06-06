from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.use_cases import (
    CreateNotificationUseCase,
    DeleteNotificationUseCase,
    GetNotificationUseCase,
    ListNotificationsUseCase,
    UpdateNotificationStatusUseCase,
)
from src.config.database import get_database_session
from src.domain.ports.event_publisher import EventPublisherPort
from src.domain.ports.notification_repository import NotificationRepositoryPort
from src.infrastructure.events.noop_event_publisher import NoOpEventPublisher
from src.infrastructure.persistence.sqlalchemy.notification_repository import (
    SqlAlchemyNotificationRepository,
)


async def get_notification_repository(
    session: AsyncSession = Depends(get_database_session),
) -> NotificationRepositoryPort:
    return SqlAlchemyNotificationRepository(session)


def get_event_publisher() -> EventPublisherPort:
    return NoOpEventPublisher()


def get_create_notification_use_case(
    notification_repository: NotificationRepositoryPort = Depends(
        get_notification_repository
    ),
    event_publisher: EventPublisherPort = Depends(get_event_publisher),
) -> CreateNotificationUseCase:
    return CreateNotificationUseCase(notification_repository, event_publisher)


def get_get_notification_use_case(
    notification_repository: NotificationRepositoryPort = Depends(
        get_notification_repository
    ),
) -> GetNotificationUseCase:
    return GetNotificationUseCase(notification_repository)


def get_list_notifications_use_case(
    notification_repository: NotificationRepositoryPort = Depends(
        get_notification_repository
    ),
) -> ListNotificationsUseCase:
    return ListNotificationsUseCase(notification_repository)


def get_update_notification_status_use_case(
    notification_repository: NotificationRepositoryPort = Depends(
        get_notification_repository
    ),
    event_publisher: EventPublisherPort = Depends(get_event_publisher),
) -> UpdateNotificationStatusUseCase:
    return UpdateNotificationStatusUseCase(notification_repository, event_publisher)


def get_delete_notification_use_case(
    notification_repository: NotificationRepositoryPort = Depends(
        get_notification_repository
    ),
    event_publisher: EventPublisherPort = Depends(get_event_publisher),
) -> DeleteNotificationUseCase:
    return DeleteNotificationUseCase(notification_repository, event_publisher)
