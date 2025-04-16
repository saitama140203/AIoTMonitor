from fastapi import APIRouter
from .endpoints import auth, user
from app.api.v1.endpoints import (auth, devices)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["User"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
