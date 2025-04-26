from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DeviceBase(BaseModel):
    name: str
    username: Optional[str] = None
    ip: str
    platform: str
    group_id: int

class DeviceCreate(BaseModel):
    name: str
    username: Optional[str] = None
    ip: str
    port: int
    platform: str
    class Config:
        from_attributes = True

class DeviceUpdate(BaseModel):
    name: str
    username: Optional[str] = None
    ip: str
    platform: str
    status: str

class DeviceResponse(BaseModel):
    name: str
    username: Optional[str] = None
    ip: str
    port: int
    platform: str    
    class Config:
        from_attributes = True

class AddDevicesToGroupRequest(BaseModel):
    device_ids: List[int] = Field(..., min_items=1)
    group_id: int

class GroupCreate(BaseModel):
    name: str

class GroupResponse(GroupCreate):
    created_at: datetime
    is_actived: bool
