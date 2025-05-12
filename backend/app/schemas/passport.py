from pydantic import BaseModel, constr
from typing import Optional
from datetime import date

class PassportCreate(BaseModel):
    passportnumber: constr(max_length=64)
    fromdate: date
    thrudate: date
    citizenship_id: int

class PassportUpdate(BaseModel):
    passportnumber: Optional[constr(max_length=64)] = None
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    citizenship_id: Optional[int] = None

class PassportOut(BaseModel):
    id: int
    passportnumber: str
    fromdate: date
    thrudate: date
    citizenship_id: int

    class Config:
        from_attributes = True