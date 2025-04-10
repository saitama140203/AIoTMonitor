from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: UserRole


class UserCreateOperator(UserBase):
    password: str = Field(..., min_length=8)
    
    
class UserCreateSupervisor(UserBase):
    password: str = Field(..., min_length=8)
    
    
class UserCreateTeamLead(UserBase):
    password: str = Field(..., min_length=8)
    

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def password_must_be_different(cls, v, values):
        if 'current_password' in values and v == values['current_password']:
            raise ValueError('New password must be different from the current password')
        return v


class UserPasswordReset(BaseModel):
    email: EmailStr
    

class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    role: Optional[str] = None


class UserInDB(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        model_config = {
            "from_attributes": True
         }

class User(UserInDB):
    pass