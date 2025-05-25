from pydantic import BaseModel
from datetime import datetime

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
    ended_at: datetime
    connected_time: datetime

    class Config:
        orm_mode = True