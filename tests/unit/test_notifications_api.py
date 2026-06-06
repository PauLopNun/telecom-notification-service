from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from src.application.dtos.notification_dtos import NotificationOutput
from src.config.app import create_app
from src.config.settings import Settings
from src.domain.enums import EventType, NotificationStatus
from src.domain.exceptions import NotificationNotFoundError
from src.domain.models.notification import Notification
from src.infrastructure.web.fastapi.dependencies import (
    get_create_notification_use_case,
    get_delete_notification_use_case,
    get_get_notification_use_case,
    get_list_notifications_use_case,
    get_update_notification_status_use_case,
)

TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/app"
TEST_NOTIFICATION_ID = uuid4()


def test_should_create_notification_when_request_is_valid() -> None:
    client = _client_with_override(
        get_create_notification_use_case,
        lambda: _SuccessfulCreateUseCase(),
    )

    response = client.post("/api/v1/notifications", json=_create_payload())

    assert response.status_code == 201
    assert response.json()["client_id"] == "client-789"


def test_should_list_notifications_when_filters_are_provided() -> None:
    client = _client_with_override(
        get_list_notifications_use_case,
        lambda: _SuccessfulListUseCase(),
    )

    response = client.get("/api/v1/notifications?client_id=client-789")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_should_return_404_when_notification_not_found() -> None:
    client = _client_with_override(
        get_get_notification_use_case,
        lambda: _MissingNotificationUseCase(),
    )

    response = client.get(f"/api/v1/notifications/{TEST_NOTIFICATION_ID}")

    assert response.status_code == 404
    assert response.json() == {"detail": "notification not found"}


def test_should_update_status_when_request_is_valid() -> None:
    client = _client_with_override(
        get_update_notification_status_use_case,
        lambda: _SuccessfulUpdateUseCase(),
    )

    response = client.patch(
        f"/api/v1/notifications/{TEST_NOTIFICATION_ID}/status",
        json={"status": "SENT"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "SENT"


def test_should_delete_notification_when_notification_exists() -> None:
    client = _client_with_override(
        get_delete_notification_use_case,
        lambda: _SuccessfulDeleteUseCase(),
    )

    response = client.delete(f"/api/v1/notifications/{TEST_NOTIFICATION_ID}")

    assert response.status_code == 204


class _SuccessfulCreateUseCase:
    async def execute(self, input_data: object) -> NotificationOutput:
        return _notification_output()


class _SuccessfulListUseCase:
    async def execute(self, input_data: object) -> list[NotificationOutput]:
        return [_notification_output()]


class _MissingNotificationUseCase:
    async def execute(self, notification_id: UUID) -> NotificationOutput:
        raise NotificationNotFoundError("notification not found")


class _SuccessfulUpdateUseCase:
    async def execute(
        self,
        notification_id: UUID,
        input_data: object,
    ) -> NotificationOutput:
        return _notification_output(NotificationStatus.SENT)


class _SuccessfulDeleteUseCase:
    async def execute(self, notification_id: UUID) -> None:
        return None


def _client_with_override(dependency: object, replacement: object) -> TestClient:
    app = create_app(_settings())
    app.dependency_overrides[dependency] = replacement
    return TestClient(app)


def _settings() -> Settings:
    return Settings(
        app_name="test-app",
        api_prefix="/api/v1",
        database_url=TEST_DATABASE_URL,
        environment="test",
    )


def _create_payload() -> dict[str, object]:
    return {
        "client_id": "client-789",
        "event_type": "SECURITY_ALERT",
        "message": "Suspicious access detected",
        "metadata": {"region": "west"},
    }


def _notification_output(
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
