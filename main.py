from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

from core.config import settings
from api.routers import chat_router, trigger_router, session_router
from domain.abstractions import ResultException

# Configure Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Build Application
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi/v1.json"
)

# --- Problem Details Global Exception Handler ---
@app.exception_handler(ResultException)
async def result_exception_handler(request: Request, exc: ResultException):
    problem_details = {
        "status": exc.error.status_code,
        "title": "A problem occurred while processing your request.",
        "extensions": {
            "errors": [
                exc.error.code,
                exc.error.description
            ]
        }
    }
    return JSONResponse(status_code=exc.error.status_code, content=problem_details)

# --- Register Controllers ---
app.include_router(session_router)
app.include_router(chat_router)
app.include_router(trigger_router)

@app.get("/", tags=["System"])
async def root():
    return {
        "service": settings.app_name,
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health", tags=["System"])
async def health():
    return {"status": "ok"}

# To run this app locally:
# uvicorn main:app --reload --port 7000
