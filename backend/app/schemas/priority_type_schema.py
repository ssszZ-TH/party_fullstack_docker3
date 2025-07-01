from pydantic import BaseModel
from typing import Optional

class PriorityTypeCreate(BaseModel):
    description: str

class PriorityTypeUpdate(BaseModel):
    description: Optional[str] = None

class PriorityTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True