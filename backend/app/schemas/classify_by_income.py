from pydantic import BaseModel
from typing import Optional
from datetime import date

class ClassifyByIncomeCreate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: Optional[int] = 2 # Default to 2 if not provided
    income_range_id: int

class ClassifyByIncomeUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: Optional[int] = None
    party_type_id: Optional[int] = 2 # Default to 2 if not provided
    income_range_id: Optional[int] = None

class ClassifyByIncomeOut(BaseModel):
    id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    income_range_id: int


    class Config:
        from_attributes = True
        
class ClassifyByIncomeByPersonIdOut(BaseModel):
    id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    income_range_id: int
    description: Optional[str] = None

    class Config:
        from_attributes = True