from pydantic import BaseModel
from typing import Optional
from datetime import date

class ClassifyBySizeCreate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    employee_count_range_id: int

class ClassifyBySizeUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: Optional[int] = None
    party_type_id: Optional[int] = None
    employee_count_range_id: Optional[int] = None

class ClassifyBySizeOut(BaseModel):
    id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    employee_count_range_id: int
    description: str

    class Config:
        from_attributes = True