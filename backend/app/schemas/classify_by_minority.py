from pydantic import BaseModel
from typing import Optional
from datetime import date

class ClassifyByMinorityCreate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    minority_type_id: int

class ClassifyByMinorityUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: Optional[int] = None
    party_type_id: Optional[int] = None
    minority_type_id: Optional[int] = None

class ClassifyByMinorityOut(BaseModel):
    id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    minority_type_id: int
    name_en: str
    name_th: str

    class Config:
        from_attributes = True