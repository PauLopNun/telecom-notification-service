from fastapi import APIRouter

HEALTHY_STATUS = "ok"

router = APIRouter(tags=["health"])


@router.get("/health")
async def check_health() -> dict[str, str]:
    return {"status": HEALTHY_STATUS}
