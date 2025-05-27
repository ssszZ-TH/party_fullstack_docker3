from pydantic import BaseModel, constr
from typing import Optional
from datetime import date

class PersonNameCreate(BaseModel):
    fromdate: date
    thrudate: Optional[date] = None
    person_id: int
    personnametype_id: int
    name: constr(max_length=128)

class PersonNameUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    person_id: Optional[int] = None
    personnametype_id: Optional[int] = None
    name: Optional[constr(max_length=128)] = None

class PersonNameOut(BaseModel):
    id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    person_id: int
    personnametype_id: int
    name: Optional[str] = None

    class Config:
        from_attributes = True