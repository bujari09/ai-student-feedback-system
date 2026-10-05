from fastapi import APIRouter, Query

from app.schemas.analytics import Analytics
from app.services.analytics_service import get_analytics

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("", response_model=Analytics)
def analytics(top_n: int = Query(10, ge=1, le=50)) -> Analytics:
    return get_analytics(top_n)
