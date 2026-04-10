from fastapi import APIRouter
from app.utils.metrics import tracker
from app.core.config import settings

router = APIRouter()


@router.get(
    "/metrics",
    tags=["System"],
    summary="API performance metrics",
)
async def get_metrics():
    """
    Returns real-time performance metrics for the API.
    No authentication required — useful for monitoring tools.
    """
    metrics = tracker.get_metrics()
    metrics["app_version"] = settings.app_version
    metrics["ai_backend"] = settings.ai_backend
    return metrics