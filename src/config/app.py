from fastapi import FastAPI

from src.config.settings import Settings, get_settings
from src.infrastructure.web.fastapi.error_handlers import register_error_handlers
from src.infrastructure.web.fastapi.routers.health import router as health_router
from src.infrastructure.web.fastapi.routers.notifications import (
    router as notifications_router,
)


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or get_settings()
    app = FastAPI(title=app_settings.app_name)
    register_error_handlers(app)
    app.include_router(health_router)
    app.include_router(notifications_router, prefix=app_settings.api_prefix)
    return app
