from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional



class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role_id: int = 2


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"



class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    is_active: bool
    role_id: int

    class Config:
        from_attributes = True


class UserWithRole(UserResponse):
    role_name: str