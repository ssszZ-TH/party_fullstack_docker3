from pydantic import BaseModel
from typing import Optional
from datetime import date

class ClassifyByIndustryCreate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: Optional[int] = 4 # Default to 4 if not provided
    industry_type_id: int

class ClassifyByIndustryUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: Optional[int] = None
    party_type_id: Optional[int] = 4 # Default to 4 if not provided
    industry_type_id: Optional[int] = None

class ClassifyByIndustryOut(BaseModel):
    id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    industry_type_id: int

    class Config:
        from_attributes = True