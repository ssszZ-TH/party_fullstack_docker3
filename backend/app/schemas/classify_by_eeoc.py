from pydantic import BaseModel
from typing import Optional
from datetime import date

class ClassifyByEeocCreate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    ethnicity_id: int

class ClassifyByEeocUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: Optional[int] = None
    party_type_id: Optional[int] = None
    ethnicity_id: Optional[int] = None

class ClassifyByEeocOut(BaseModel):
    id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    ethnicity_id: int
    name_en: str
    name_th: str

    class Config:
        from_attributes = True