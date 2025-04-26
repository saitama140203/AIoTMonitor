from pydantic import BaseModel, Field
from typing import List
class CommandCreate(BaseModel):
    commands_text: str
    description: str

class CommandResponse(CommandCreate):
    pass

class CreateCommandList(BaseModel):
    command_ids: List[int] = Field(..., min_items=1)
    profile_id : int

class CommandProfileSchema(BaseModel):
    id: int
    command_id: int
    profile_id: int

    class Config:
        from_attributes=True

