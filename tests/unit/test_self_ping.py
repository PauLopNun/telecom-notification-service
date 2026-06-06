import httpx
import pytest
from pytest import MonkeyPatch

from src.infrastructure.web.fastapi import self_ping

APP_URL = "https://telecom-notification-service.onrender.com/"


@pytest.mark.asyncio
async def test_should_skip_scheduler_start_when_render_url_is_missing(
    monkeypatch: MonkeyPatch,
) -> None:
    scheduler = FakeScheduler()
    _use_scheduler(monkeypatch, scheduler)
    monkeypatch.setattr(self_ping, "getenv", lambda name: None)

    await self_ping.start_self_ping_scheduler()

    assert scheduler.jobs == []
    assert scheduler.started is False


@pytest.mark.asyncio
async def test_should_skip_scheduler_start_when_scheduler_is_running(
    monkeypatch: MonkeyPatch,
) -> None:
    scheduler = FakeScheduler(running=True)
    _use_scheduler(monkeypatch, scheduler)
    monkeypatch.setattr(self_ping, "getenv", lambda name: APP_URL)

    await self_ping.start_self_ping_scheduler()

    assert scheduler.jobs == []


@pytest.mark.asyncio
async def test_should_start_scheduler_when_render_url_exists(
    monkeypatch: MonkeyPatch,
) -> None:
    scheduler = FakeScheduler()
    _use_scheduler(monkeypatch, scheduler)
    monkeypatch.setattr(self_ping, "getenv", lambda name: APP_URL)

    await self_ping.start_self_ping_scheduler()

    assert scheduler.started is True
    assert scheduler.jobs == [_expected_job()]


@pytest.mark.asyncio
async def test_should_shutdown_scheduler_when_scheduler_is_running(
    monkeypatch: MonkeyPatch,
) -> None:
    scheduler = FakeScheduler(running=True)
    _use_scheduler(monkeypatch, scheduler)

    await self_ping.stop_self_ping_scheduler()

    assert scheduler.shutdown_wait is False


@pytest.mark.asyncio
async def test_should_keep_scheduler_idle_when_scheduler_is_stopped(
    monkeypatch: MonkeyPatch,
) -> None:
    scheduler = FakeScheduler()
    _use_scheduler(monkeypatch, scheduler)

    await self_ping.stop_self_ping_scheduler()

    assert scheduler.shutdown_wait is None


@pytest.mark.asyncio
async def test_should_call_health_endpoint_when_ping_succeeds(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(self_ping.httpx, "AsyncClient", SuccessfulAsyncClient)

    await self_ping.ping_self(APP_URL)

    assert SuccessfulAsyncClient.requested_url == (
        "https://telecom-notification-service.onrender.com/health"
    )
    assert SuccessfulAsyncClient.request_timeout == self_ping.SELF_PING_TIMEOUT_SECONDS


@pytest.mark.asyncio
async def test_should_ignore_http_error_when_ping_fails(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(self_ping.httpx, "AsyncClient", FailingAsyncClient)

    await self_ping.ping_self(APP_URL)


class FakeScheduler:
    def __init__(self, running: bool = False) -> None:
        self.running = running
        self.started = False
        self.jobs: list[dict[str, object]] = []
        self.shutdown_wait: bool | None = None

    def add_job(self, callback: object, trigger: str, **kwargs: object) -> None:
        self.jobs.append({"callback": callback, "trigger": trigger, **kwargs})

    def start(self) -> None:
        self.started = True
        self.running = True

    def shutdown(self, wait: bool) -> None:
        self.shutdown_wait = wait
        self.running = False


class SuccessfulAsyncClient:
    requested_url: str | None = None
    request_timeout: int | None = None

    async def __aenter__(self) -> "SuccessfulAsyncClient":
        return self

    async def __aexit__(
        self,
        exception_type: object,
        exception: object,
        traceback: object,
    ) -> None:
        return None

    async def get(self, url: str, **request_options: object) -> None:
        SuccessfulAsyncClient.requested_url = url
        SuccessfulAsyncClient.request_timeout = request_options["timeout"]


class FailingAsyncClient(SuccessfulAsyncClient):
    async def get(self, url: str, **request_options: object) -> None:
        raise httpx.ConnectError("service unavailable")


def _use_scheduler(monkeypatch: MonkeyPatch, scheduler: FakeScheduler) -> None:
    monkeypatch.setattr(self_ping, "scheduler", scheduler)


def _expected_job() -> dict[str, object]:
    return {
        "callback": self_ping.ping_self,
        "trigger": "interval",
        "minutes": self_ping.SELF_PING_INTERVAL_MINUTES,
        "args": [APP_URL],
        "id": self_ping.SELF_PING_JOB_ID,
        "replace_existing": True,
    }
