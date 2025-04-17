from fastapi import APIRouter
from app.api.v1.endpoints import (auth, devices,command, profiles,user)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["User"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(devices.router, prefix="", tags=["devices, groups"])
api_router.include_router(command.router, prefix="/commands", tags=["commands"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
