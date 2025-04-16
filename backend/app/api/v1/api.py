from fastapi import APIRouter

from app.api.v1.endpoints import (auth, devices)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
