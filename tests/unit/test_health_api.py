from fastapi.testclient import TestClient

from src.config.app import create_app
from src.config.settings import Settings

TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/app"


def test_should_return_ok_when_health_check_is_requested() -> None:
    client = TestClient(create_app(_settings()))

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def _settings() -> Settings:
    return Settings(
        app_name="test-app",
        api_prefix="/api/v1",
        database_url=TEST_DATABASE_URL,
        environment="test",
    )
