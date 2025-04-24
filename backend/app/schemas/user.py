from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    roles: List[str] = Field(..., min_items=1)
    
    @validator('roles')
    def validate_roles(cls, v):
        valid_roles = {'admin', 'operator', 'supervisor', 'team_lead'}
        for role in v:
            if role.lower() not in valid_roles:
                raise ValueError(f"Invalid role: {role}")
        return [role.lower() for role in v]
class RoleResponse(BaseModel):
    id: int
    name: str
    

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    is_active: bool
    roles: List[RoleResponse]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def password_must_be_different(cls, v, values):
        if 'current_password' in values and v == values['current_password']:
            raise ValueError('New password must be different from current password')
        return v

class UserPasswordReset(BaseModel):
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    roles: List[str] = []

class TokenPayload(BaseModel):
    sub: Optional[int] = None
    roles: List[str] = []
    exp: Optional[datetime] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    email: str
    full_name: str | None = None
    roles: Optional[List[str]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
class User(UserInDB):
    pass