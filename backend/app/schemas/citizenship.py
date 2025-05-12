from pydantic import BaseModel
from typing import Optional
from datetime import date

class CitizenshipCreate(BaseModel):
    fromdate: date
    thrudate: Optional[date] = None
    person_id: int
    country_id: int

class CitizenshipUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    person_id: Optional[int] = None
    country_id: Optional[int] = None

class CitizenshipOut(BaseModel):
    id: int
    fromdate: date
    thrudate: Optional[date] = None
    person_id: int
    country_id: int

    class Config:
        from_attributes = True