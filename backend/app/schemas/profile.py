from pydantic import BaseModel, Field
from datetime import datetime

class ProfileCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, example="Network Config")
    group_id: int

class ProfileResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

class AssignProfile(BaseModel):
    operator_id: int
    profile_id: int
    # is_active: bool = Field(default=True, example=True)
    class Config:        
        from_attributes = True
    
class AssignProfileResponse(AssignProfile):
    pass
    class Config:        
        from_attributes = True