from pydantic import BaseModel
from datetime import datetime
from typing import Optional,List

class SessionDetail(BaseModel):
    session_id: int
    operator_name: str
    device_name: str
    status: str
    start_time: datetime
    current_command: str | None
    
    class Config:
        orm_mode = True

class TerminateSessionRequest(BaseModel):
    terminated_by: int
    reason: str | None = None

class SessionHistoryItem(BaseModel):
    session_id: int
    device_name: str
    operator_name: str
    end_status: str
    ended_at: Optional[datetime] = None 
    connected_time: Optional[datetime] = None
    last_commands: Optional[List[dict]] = []
    all_commands: Optional[List[dict]] = []

    class Config:
        orm_mode = True


class SessionCreateSchema(BaseModel):
    operator_id: int
    device_id: int

    class Config:
        orm_mode = True

class CommandCreate(BaseModel):
    session_id: int
    command_text: str

