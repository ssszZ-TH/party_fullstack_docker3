from pydantic import BaseModel
from typing import Optional

class PartyRelationshipStatusTypeCreate(BaseModel):
    description: str

class PartyRelationshipStatusTypeUpdate(BaseModel):
    description: Optional[str] = None

class PartyRelationshipStatusTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True