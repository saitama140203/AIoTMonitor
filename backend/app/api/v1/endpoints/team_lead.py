from fastapi import APIRouter, Depends, HTTPException
from app.services.device_service import DeviceService
from app.schemas.device import DeviceCreate, DeviceGroupCreate, DeviceInDB, DeviceGroupInDB
from sqlalchemy.orm import Session
from app.api.v1.deps import get_db, get_current_user
from app.models import User
from app.services.profile_sevice import ProfileService

router = APIRouter()

@router.post("/devices", response_model=DeviceInDB)
def create_device(
    device: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "team_lead":
        raise HTTPException(status_code=403, detail="Only Team Leads can create devices")
    
    service = DeviceService(db)
    return service.create_device(device, current_user.id)

@router.post("/device-groups", response_model=DeviceGroupInDB)
def create_device_group(
    group: DeviceGroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "team_lead":
        raise HTTPException(status_code=403, detail="Only Team Leads can create device groups")
    
    service = DeviceService(db)
    return service.create_device_group(group, current_user.id)

@router.post("/device-groups/{group_id}/add-devices")
def add_devices_to_group(
    group_id: int,
    device_ids: list[int],
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    service = DeviceService(db)
    result = service.add_devices_to_group(group_id, device_ids, current_user.id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Group not found or access denied")
    
    return {"message": f"Added {len(device_ids)} devices to group successfully"}

@router.post("/profiles/{profile_id}/assign-to-operator/{operator_id}")
def assign_profile_to_operator(
    profile_id: int,
    operator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ProfileService(db)
    result = service.assign_profile_to_operator(profile_id, operator_id, current_user.id)
    return result


