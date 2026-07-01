from fastapi import FastAPI

from app.api.routes import router as chat_router
from app.api.health import router as health_router
from app.api.ui import router as ui_router


app = FastAPI(title="NL2SQL Vanna AI")

app.include_router(ui_router)
app.include_router(chat_router)
app.include_router(health_router)
