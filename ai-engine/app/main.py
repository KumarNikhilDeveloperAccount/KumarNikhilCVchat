from fastapi import FastAPI

from .api.chat import router as chat_router
from .api.health import router as health_router
from .api.themes import router as themes_router

app = FastAPI(title="Nikhil-OS AI Engine", version="0.1.0")

app.include_router(health_router)
app.include_router(chat_router, prefix="/v1/chat", tags=["chat"])
app.include_router(themes_router, prefix="/v1/themes", tags=["themes"])

