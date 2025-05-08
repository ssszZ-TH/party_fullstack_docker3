from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    password: Optional[str] = None

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: Optional[str] = None

    class Config:
        from_attributes = True