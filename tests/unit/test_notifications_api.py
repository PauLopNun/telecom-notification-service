from src.infrastructure.web.fastapi.dependencies import (
    get_create_notification_use_case,
    get_delete_notification_use_case,
    get_get_notification_use_case,
    get_list_notifications_use_case,
    get_update_notification_status_use_case,
)
from tests.unit.notification_api_fakes import (
    TEST_NOTIFICATION_ID,
    MissingNotificationUseCase,
    SuccessfulCreateUseCase,
    SuccessfulDeleteUseCase,
    SuccessfulGetUseCase,
    SuccessfulListUseCase,
    SuccessfulUpdateUseCase,
    client_with_override,
    create_payload,
)


def test_should_create_notification_when_request_is_valid() -> None:
    client = client_with_override(
        get_create_notification_use_case,
        lambda: SuccessfulCreateUseCase(),
    )

    response = client.post("/api/v1/notifications", json=create_payload())

    assert response.status_code == 201
    assert response.json()["client_id"] == "client-789"


def test_should_list_notifications_when_filters_are_provided() -> None:
    client = client_with_override(
        get_list_notifications_use_case,
        lambda: SuccessfulListUseCase(),
    )

    response = client.get("/api/v1/notifications?client_id=client-789")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_should_get_notification_when_notification_exists() -> None:
    client = client_with_override(
        get_get_notification_use_case,
        lambda: SuccessfulGetUseCase(),
    )

    response = client.get(f"/api/v1/notifications/{TEST_NOTIFICATION_ID}")

    assert response.status_code == 200
    assert response.json()["id"] == str(TEST_NOTIFICATION_ID)


def test_should_return_404_when_notification_not_found() -> None:
    client = client_with_override(
        get_get_notification_use_case,
        lambda: MissingNotificationUseCase(),
    )

    response = client.get(f"/api/v1/notifications/{TEST_NOTIFICATION_ID}")

    assert response.status_code == 404
    assert response.json() == {"detail": "notification not found"}


def test_should_update_status_when_request_is_valid() -> None:
    client = client_with_override(
        get_update_notification_status_use_case,
        lambda: SuccessfulUpdateUseCase(),
    )

    response = client.patch(
        f"/api/v1/notifications/{TEST_NOTIFICATION_ID}/status",
        json={"status": "SENT"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "SENT"


def test_should_delete_notification_when_notification_exists() -> None:
    client = client_with_override(
        get_delete_notification_use_case,
        lambda: SuccessfulDeleteUseCase(),
    )

    response = client.delete(f"/api/v1/notifications/{TEST_NOTIFICATION_ID}")

    assert response.status_code == 204
