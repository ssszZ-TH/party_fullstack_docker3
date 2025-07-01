from pydantic import BaseModel
from typing import Optional

class PartyRelationshipTypeCreate(BaseModel):
    description: str

class PartyRelationshipTypeUpdate(BaseModel):
    description: Optional[str] = None

class PartyRelationshipTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True