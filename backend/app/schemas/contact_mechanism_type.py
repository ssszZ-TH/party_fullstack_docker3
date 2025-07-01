from pydantic import BaseModel
from typing import Optional

class ContactMechanismTypeCreate(BaseModel):
    description: str

class ContactMechanismTypeUpdate(BaseModel):
    description: Optional[str] = None

class ContactMechanismTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True