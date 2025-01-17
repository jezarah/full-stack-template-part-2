from fastapi import APIRouter

from api.router import users, authentication, appointments

tags_metadata = [
    {"name": "get"},
    {"name": "post"},
    {"name": "patch"},
    {"name": "delete"}
]
api_router = APIRouter()
api_router.include_router(authentication.router)
api_router.include_router(users.router)
api_router.include_router(appointments.router)