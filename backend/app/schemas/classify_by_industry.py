from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class ClassifyByIndustryCreate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: Optional[int] = 4
    industry_type_id: int

class ClassifyByIndustryUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: Optional[int] = None
    party_type_id: Optional[int] = 4
    industry_type_id: Optional[int] = None

class ClassifyByIndustryOut(BaseModel):
    id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    industry_type_id: int
    naics_code: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True