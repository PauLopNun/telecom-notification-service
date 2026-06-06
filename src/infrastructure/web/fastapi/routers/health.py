from fastapi import APIRouter

HEALTHY_STATUS = "ok"
SERVICE_NAME = "telecom-notification-service"
SERVICE_VERSION = "0.1.0"

router = APIRouter(tags=["health"])


@router.get("/")
async def get_service_info() -> dict[str, str]:
    return {
        "name": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "health": "/health",
        "docs": "/docs",
    }


@router.get("/health")
async def check_health() -> dict[str, str]:
    return {"status": HEALTHY_STATUS}
