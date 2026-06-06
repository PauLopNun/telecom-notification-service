# Telecom Notification Service

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=githubactions&logoColor=white)

`telecom-notification-service` is a REST microservice for managing telecom
network notifications and service alerts. It receives events, persists
notifications, and exposes query endpoints by client, event type, and status.

The project follows Hexagonal Architecture so the domain and application layers
stay independent from FastAPI, SQLAlchemy, PostgreSQL, and future message
broker integrations.

## Tech Stack

| Area | Technology |
| --- | --- |
| API | FastAPI |
| Validation | Pydantic v2 |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0 async |
| Migrations | Alembic |
| Tests | pytest, pytest-asyncio, pytest-cov, testcontainers-python |
| Tooling | Ruff, Docker, Docker Compose, GitHub Actions |

## Architecture

```mermaid
flowchart LR
    HTTP[REST API] --> WEB[FastAPI Adapter]
    WEB --> APP[Application Use Cases]
    APP --> DOMAIN[Domain Model]
    APP --> REPO_PORT[NotificationRepositoryPort]
    APP --> EVENT_PORT[EventPublisherPort]
    REPO_PORT --> REPO[SQLAlchemy Repository]
    REPO --> DB[(PostgreSQL)]
    EVENT_PORT --> NOOP[NoOpEventPublisher]
    FUTURE[event-processor-service] -. planned .-> RABBIT[(RabbitMQ)]
```

## Run Locally

Create a local environment file:

```bash
cp .env.example .env
```

Start the full stack:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API docs:

```text
http://localhost:8000/docs
```

## Run Tests

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run linting:

```bash
ruff check .
```

Run the test suite with coverage:

```bash
pytest
```

Integration tests use `TEST_DATABASE_URL` when it is defined. If it is not
defined, they start a PostgreSQL container with testcontainers-python.

## API Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/api/v1/notifications` | Create a notification |
| `GET` | `/api/v1/notifications` | List notifications with filters and pagination |
| `GET` | `/api/v1/notifications/{id}` | Get a notification by ID |
| `PATCH` | `/api/v1/notifications/{id}/status` | Update notification status |
| `DELETE` | `/api/v1/notifications/{id}` | Delete a notification |
| `GET` | `/health` | Health check |

Supported filters for `GET /api/v1/notifications`:

| Query parameter | Values |
| --- | --- |
| `client_id` | Telecom client identifier |
| `event_type` | `NETWORK_OUTAGE`, `SERVICE_DEGRADATION`, `MAINTENANCE`, `BILLING_ALERT`, `SECURITY_ALERT` |
| `status` | `PENDING`, `SENT`, `FAILED`, `ACKNOWLEDGED` |
| `limit` | 1 to 100 |
| `offset` | 0 or greater |

## Environment Variables

| Variable | Description | Example |
| --- | --- | --- |
| `APP_NAME` | Application name | `telecom-notification-service` |
| `ENVIRONMENT` | Runtime environment | `local` |
| `API_PREFIX` | Versioned API prefix | `/api/v1` |
| `DATABASE_URL` | Async PostgreSQL URL used by the app | `postgresql+asyncpg://user:pass@localhost:5432/db` |
| `POSTGRES_DB` | Docker Compose PostgreSQL database | `telecom_notifications` |
| `POSTGRES_USER` | Docker Compose PostgreSQL user | `telecom_user` |
| `POSTGRES_PASSWORD` | Docker Compose PostgreSQL password | `change_me` |
| `RABBITMQ_DEFAULT_USER` | RabbitMQ management user | `telecom_user` |
| `RABBITMQ_DEFAULT_PASS` | RabbitMQ management password | `change_me` |
| `TEST_DATABASE_URL` | PostgreSQL URL for integration tests | `postgresql+asyncpg://user:pass@localhost:5432/test_db` |

## Roadmap

- Add `event-processor-service` as a second microservice.
- Replace `NoOpEventPublisher` with a RabbitMQ adapter.
- Publish notification lifecycle events to RabbitMQ.
- Add consumer-side processing for delivery workflows and retries.
