from pydantic import BaseModel
from typing import Optional
from datetime import date

class ClassifyByMinorityCreate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: Optional[int] = 3 # Default to 3 if not provided
    minority_type_id: int

class ClassifyByMinorityUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: Optional[int] = None
    party_type_id: Optional[int] = 3 # Default to 3 if not provided
    minority_type_id: Optional[int] = None

class ClassifyByMinorityOut(BaseModel):
    id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    minority_type_id: int


    class Config:
        from_attributes = True