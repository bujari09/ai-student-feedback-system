import logging

from fastapi import APIRouter

from app.config import get_settings
from app.database import get_feedback_collection

router = APIRouter(prefix="/api", tags=["health"])
logger = logging.getLogger(__name__)


@router.get("/health")
def health() -> dict:
    """Liveness plus a cheap Firestore connectivity check."""
    settings = get_settings()
    try:
        list(get_feedback_collection().limit(1).stream())
        database = "ok"
    except Exception as exc:  # report, don't crash the health endpoint
        logger.warning("Firestore health check failed: %s", exc)
        database = "error"

    return {
        "status": "ok" if database == "ok" else "degraded",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "database": database,
    }
