from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User
from fastapi import APIRouter, Depends
from app.services.device_service import (
    create_device,
    get_devices,
    update_device_status,
    create_device_group,
    create_command_list,
    create_profile,
    assign_profile_to_operator
)
from app.schemas.device import (
    DeviceCreate,
    DeviceResponse,
    GroupCreate,
    CommandCreate,
    ProfileCreate,
    ProfileAssign
)
from app.api.v1.deps import get_db, get_current_team_lead

router = APIRouter()

@router.post("", response_model=DeviceResponse)
def create_new_device(
    device_data: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_team_lead)
):
    return create_device(db, device_data, current_user)

@router.get("", response_model=List[DeviceResponse])
def list_devices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_team_lead),
    group_id: Optional[int] = None,
    status: Optional[str] = None
):
    return get_devices(db, current_user, group_id, status)
