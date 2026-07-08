import os
import traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router as chat_router
from app.api.health import router as health_router
from app.api.ui import router as ui_router
from app.core.database import initialize_database


app = FastAPI(title="NL2SQL Vanna AI")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": f"Internal Server Error: {str(exc)}",
        },
    )


@app.on_event("startup")
async def startup():
    initialize_database()


app.include_router(ui_router)
app.include_router(chat_router)
app.include_router(health_router)
