from os import getenv

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

HEALTH_PATH = "/health"
RENDER_EXTERNAL_URL_ENV_NAME = "RENDER_EXTERNAL_URL"
SELF_PING_JOB_ID = "render-self-ping"
SELF_PING_INTERVAL_MINUTES = 10
SELF_PING_TIMEOUT_SECONDS = 10

scheduler = AsyncIOScheduler()


def register_self_ping_scheduler(app: FastAPI) -> None:
    app.router.on_startup.append(start_self_ping_scheduler)
    app.router.on_shutdown.append(stop_self_ping_scheduler)


async def start_self_ping_scheduler() -> None:
    app_url = getenv(RENDER_EXTERNAL_URL_ENV_NAME)
    if app_url is None or scheduler.running:
        return
    scheduler.add_job(
        ping_self,
        "interval",
        minutes=SELF_PING_INTERVAL_MINUTES,
        args=[app_url],
        id=SELF_PING_JOB_ID,
        replace_existing=True,
    )
    scheduler.start()


async def stop_self_ping_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)


async def ping_self(app_url: str) -> None:
    try:
        async with httpx.AsyncClient() as client:
            await client.get(_health_url(app_url), timeout=SELF_PING_TIMEOUT_SECONDS)
    except httpx.HTTPError:
        return


def _health_url(app_url: str) -> str:
    return f"{app_url.rstrip('/')}{HEALTH_PATH}"
