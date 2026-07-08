import os

from fastapi import APIRouter

from app.core.config import settings
from app.core.database import get_connection


router = APIRouter()


@router.get("/health")
def health():
    db_ok = os.path.exists(settings.DATABASE_PATH)
    api_key_set = bool(settings.GOOGLE_API_KEY)

    return {
        "status": "ok",
        "database": "connected" if db_ok else "not_found",
        "api_key_configured": api_key_set,
        "vercel": settings.ON_VERCEL,
    }
