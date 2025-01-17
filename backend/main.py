from fastapi import FastAPI

from core.config import settings
from api.main import api_router

app = FastAPI(
    title="Appointment Manager API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(api_router, prefix=settings.API_V1_STR)