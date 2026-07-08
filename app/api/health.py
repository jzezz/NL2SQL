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


@router.get("/test-gemini")
async def test_gemini():
    try:
        from google import genai

        client = genai.Client(api_key=settings.GOOGLE_API_KEY)

        models_to_try = [
            "gemini-1.5-flash",
            "gemini-2.0-flash",
            "gemini-2.0-flash-exp",
        ]

        results = {}
        for model in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model,
                    contents="Say OK",
                )
                results[model] = "works"
            except Exception as e:
                results[model] = str(e)[:200]

        return {"api_key_set": bool(settings.GOOGLE_API_KEY), "models": results}

    except Exception as e:
        return {"api_key_set": bool(settings.GOOGLE_API_KEY), "error": str(e)[:500]}
