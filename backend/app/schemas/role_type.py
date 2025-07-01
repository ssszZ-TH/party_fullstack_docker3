from pydantic import BaseModel
from typing import Optional

class RoleTypeCreate(BaseModel):
    description: str

class RoleTypeUpdate(BaseModel):
    description: Optional[str] = None

class RoleTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True