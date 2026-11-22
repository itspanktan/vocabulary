"""FastAPI application entrypoint."""
from __future__ import annotations

from fastapi import FastAPI

from app.api.routers.words import router as words_router

app = FastAPI(title="Vocabulary API")
app.include_router(words_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
