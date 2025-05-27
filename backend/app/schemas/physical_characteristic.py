from pydantic import BaseModel
from typing import Optional
from datetime import date

class PhysicalCharacteristicCreate(BaseModel):
    fromdate: date
    thrudate: Optional[date] = None
    val: int
    person_id: int
    physicalcharacteristictype_id: int

class PhysicalCharacteristicUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    val: Optional[int] = None
    person_id: Optional[int] = None
    physicalcharacteristictype_id: Optional[int] = None

class PhysicalCharacteristicOut(BaseModel):
    id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    val: Optional[int] = None
    person_id: int
    physicalcharacteristictype_id: int

    class Config:
        from_attributes = True