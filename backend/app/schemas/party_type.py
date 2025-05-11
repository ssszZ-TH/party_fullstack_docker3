from pydantic import BaseModel, constr
from typing import Optional

class PartyTypeCreate(BaseModel):
    description: constr(max_length=128)

class PartyTypeUpdate(BaseModel):
    description: Optional[constr(max_length=128)] = None

class PartyTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True