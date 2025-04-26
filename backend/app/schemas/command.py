from pydantic import BaseModel, Field, field_validator
from typing import List
class CommandCreate(BaseModel):
    commands_text: str = Field(..., min_length=1, max_length=500)
    description: str = Field(..., min_length=1, max_length=255)
    @field_validator('commands_text', 'description')
    def must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError("Field must not be blank or only spaces")
        return v

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

