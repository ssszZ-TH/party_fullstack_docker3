from pydantic import BaseModel
from typing import Optional
from datetime import date

class MaritalStatusCreate(BaseModel):
    fromdate: date
    thrudate: Optional[date] = None
    person_id: int
    maritalstatustype_id: int

class MaritalStatusUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    person_id: Optional[int] = None
    maritalstatustype_id: Optional[int] = None

class MaritalStatusOut(BaseModel):
    id: int
    fromdate: date
    thrudate: Optional[date] = None
    person_id: int
    maritalstatustype_id: int

    class Config:
        from_attributes = True