from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from src.application.dtos.notification_dtos import NotificationOutput
from src.config.app import create_app
from src.config.settings import Settings
from src.domain.enums import EventType, NotificationStatus
from src.domain.exceptions import NotificationNotFoundError
from src.domain.models.notification import Notification

TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/app"
TEST_NOTIFICATION_ID = uuid4()


class SuccessfulCreateUseCase:
    async def execute(self, input_data: object) -> NotificationOutput:
        return notification_output()


class SuccessfulListUseCase:
    async def execute(self, input_data: object) -> list[NotificationOutput]:
        return [notification_output()]


class SuccessfulGetUseCase:
    async def execute(self, notification_id: UUID) -> NotificationOutput:
        return notification_output()


class MissingNotificationUseCase:
    async def execute(self, notification_id: UUID) -> NotificationOutput:
        raise NotificationNotFoundError("notification not found")


class SuccessfulUpdateUseCase:
    async def execute(
        self,
        notification_id: UUID,
        input_data: object,
    ) -> NotificationOutput:
        return notification_output(NotificationStatus.SENT)


class SuccessfulDeleteUseCase:
    async def execute(self, notification_id: UUID) -> None:
        return None


def client_with_override(dependency: object, replacement: object) -> TestClient:
    app = create_app(settings())
    app.dependency_overrides[dependency] = replacement
    return TestClient(app)


def create_payload() -> dict[str, object]:
    return {
        "client_id": "client-789",
        "event_type": "SECURITY_ALERT",
        "message": "Suspicious access detected",
        "metadata": {"region": "west"},
    }


def notification_output(
    status: NotificationStatus = NotificationStatus.PENDING,
) -> NotificationOutput:
    notification = Notification.create(
        client_id="client-789",
        event_type=EventType.SECURITY_ALERT,
        message="Suspicious access detected",
        metadata={"region": "west"},
    )
    notification.update_status(status)
    return NotificationOutput(
        id=TEST_NOTIFICATION_ID,
        client_id=notification.client_id,
        event_type=notification.event_type,
        status=notification.status,
        message=notification.message,
        metadata=notification.metadata,
        created_at=notification.created_at,
        updated_at=notification.updated_at,
    )


def settings() -> Settings:
    return Settings(
        app_name="test-app",
        api_prefix="/api/v1",
        database_url=TEST_DATABASE_URL,
        environment="test",
    )
