# app/schemas/device.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DeviceBase(BaseModel):
    name: str
    mac: Optional[str] = None
    ip: str
    platform: str
    group_id: int

class DeviceCreate(BaseModel):
    name: str
    mac: Optional[str] = None
    ip: str
    platform: str

class DeviceUpdate(BaseModel):
    status: Optional[str] = None
    lastseen: Optional[datetime] = None

class DeviceResponse(DeviceBase):
    id: int
    status: str
    lastseen: datetime
    created_by: int
    
    class Config:
        from_attributes = True

class GroupCreate(BaseModel):
    name: str

class GroupResponse(GroupCreate):
    id: int
    created_at: datetime
    is_actived: bool

class CommandCreate(BaseModel):
    commands_text: str
    description: str

class ProfileCreate(BaseModel):
    name: str
    command_list_id: int
    device_group_id: int

class ProfileAssign(BaseModel):
    profile_id: int
    operator_id: int