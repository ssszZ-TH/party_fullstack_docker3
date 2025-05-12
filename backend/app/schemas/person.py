from pydantic import BaseModel, constr
from typing import Optional
from datetime import date

class PersonCreate(BaseModel):
    socialsecuritynumber: Optional[constr(max_length=64)] = None
    birthdate: Optional[date] = None
    mothermaidenname: Optional[constr(max_length=128)] = None
    totalyearworkexperience: Optional[int] = None
    comment: Optional[str] = None

class PersonUpdate(BaseModel):
    socialsecuritynumber: Optional[constr(max_length=64)] = None
    birthdate: Optional[date] = None
    mothermaidenname: Optional[constr(max_length=128)] = None
    totalyearworkexperience: Optional[int] = None
    comment: Optional[str] = None

class PersonOut(BaseModel):
    id: int
    socialsecuritynumber: Optional[str] = None
    birthdate: Optional[date] = None
    mothermaidenname: Optional[str] = None
    totalyearworkexperience: Optional[int] = None
    comment: Optional[str] = None

    class Config:
        from_attributes = True