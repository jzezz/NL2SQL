import os

from fastapi import APIRouter

from app.core.config import settings
from app.core.database import get_connection


router = APIRouter()


@router.get("/health")
def health():
    db_ok = os.path.exists(settings.DATABASE_PATH)
    api_key_set = bool(settings.GOOGLE_API_KEY)
    llm_key_set = bool(settings.LLM_API_KEY)

    return {
        "status": "ok",
        "database": "connected" if db_ok else "not_found",
        "llm_provider": settings.LLM_PROVIDER,
        "api_key_configured": api_key_set or llm_key_set,
        "vercel": settings.ON_VERCEL,
    }


@router.get("/test-llm")
async def test_llm():
    try:
        from app.agent.vanna_setup import _build_llm_service

        llm = _build_llm_service()

        from vanna import LlmRequest

        resp = llm.send_request(
            LlmRequest(
                system_prompt="Reply with just the word OK",
                messages=[],
            )
        )

        return {
            "provider": settings.LLM_PROVIDER,
            "model": settings.LLM_MODEL or "default",
            "status": "works",
            "response": resp.content[:200],
        }

    except Exception as e:
        return {
            "provider": settings.LLM_PROVIDER,
            "error": str(e)[:500],
        }
