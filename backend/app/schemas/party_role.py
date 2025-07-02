from pydantic import BaseModel
from typing import Optional, Literal
from datetime import date

class PartyRoleCreate(BaseModel):
    party_id: int
    role_type_id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None

class PartyRoleUpdate(BaseModel):
    party_id: Optional[int] = None
    role_type_id: Optional[int] = None
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None

class PartyRoleOut(BaseModel):
    id: int
    party_id: int
    role_type_id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    type: Literal["organization", "person"]
    name_en: Optional[str] = None
    name_th: Optional[str] = None
    personal_id_number: Optional[str] = None
    comment: Optional[str] = None

    class Config:
        from_attributes = True