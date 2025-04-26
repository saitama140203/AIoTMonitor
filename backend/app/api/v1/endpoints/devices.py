from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.models.user import User
from fastapi import APIRouter, Depends
from app.services.device_service import (
    create_device,
    get_devices,
    # update_device_status,
    create_device_group,
    devices_into_group,
)
from app.schemas.device import (
    AddDevicesToGroupRequest,
    DeviceCreate,
    DeviceResponse,
    GroupCreate,
    GroupResponse,
)
from app.api.v1.deps import get_db, get_current_team_lead, get_current_admin, get_current_supervisor, get_current_user

router = APIRouter()

@router.post("/devices/create_device", response_model=DeviceResponse)
def create_new_device(
    device_data: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_team_lead)
):
    return create_device(db, device_data, current_user)

@router.get("/devices/get_devices", response_model=List[DeviceResponse])
def list_devices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    group_id: Optional[int] = None,
    status: Optional[str] = None,
    username: Optional[str] = None,

):
    return get_devices(db, current_user, group_id, status)

@router.post("/groups/create_group", response_model=GroupResponse)
def create_new_group(
    group_data: GroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_team_lead)
):
    return create_device_group(db, group_data, current_user)

@router.post("/add-to-group", response_model=Dict[str, Any])
def add_devices_to_group(
    request_data: AddDevicesToGroupRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_team_lead)
):
    return devices_into_group(db, request_data, current_user)