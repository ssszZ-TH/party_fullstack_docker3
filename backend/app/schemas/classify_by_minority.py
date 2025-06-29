from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class ClassifyByMinorityCreate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: Optional[int] = 3
    minority_type_id: int

class ClassifyByMinorityUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: Optional[int] = None
    party_type_id: Optional[int] = 3
    minority_type_id: Optional[int] = None

class ClassifyByMinorityOut(BaseModel):
    id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    minority_type_id: int
    name_en: Optional[str] = None
    name_th: Optional[str] = None

    class Config:
        from_attributes = True