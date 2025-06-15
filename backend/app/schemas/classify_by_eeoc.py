from pydantic import BaseModel
from typing import Optional
from datetime import date

class ClassifyByEeocCreate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: Optional[int] = 1 # Default to 1 if not provided
    ethnicity_id: int

class ClassifyByEeocUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: Optional[int] = None
    party_type_id: Optional[int] = 1 # Default to 1 if not provided
    ethnicity_id: Optional[int] = None

class ClassifyByEeocOut(BaseModel):
    id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: Optional[int] = None
    party_type_id: Optional[int] = None
    ethnicity_id: Optional[int] = None

    class Config:
        from_attributes = True
        
class ClassifyByEeocByPersonIdOut(BaseModel):
    id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: Optional[int] = None
    party_type_id: Optional[int] = None
    ethnicity_id: Optional[int] = None
    name_en: Optional[str] = None
    name_th: Optional[str] = None

    class Config:
        from_attributes = True