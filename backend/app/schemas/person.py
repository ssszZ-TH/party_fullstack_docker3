from pydantic import BaseModel, constr
from typing import Optional
from datetime import date

class NameDetail(BaseModel):
    id: int
    name: str
    fromdate: date
    thrudate: Optional[date] = None
    personnametype_id: int
    personnametype_description: str

class MaritalStatusDetail(BaseModel):
    id: int
    fromdate: date
    thrudate: Optional[date] = None
    maritalstatustype_id: int
    maritalstatustype_description: str

class PhysicalCharacteristicDetail(BaseModel):
    id: int
    val: int
    fromdate: date
    thrudate: Optional[date] = None
    physicalcharacteristictype_id: int
    physicalcharacteristictype_description: str

class CitizenshipDetail(BaseModel):
    id: int
    fromdate: date
    thrudate: Optional[date] = None
    country_id: int
    country_isocode: str
    country_name_en: str
    country_name_th: str

class PersonCreate(BaseModel):
    personal_id_number: Optional[constr(max_length=64)] = None
    birthdate: Optional[date] = None
    mothermaidenname: Optional[constr(max_length=128)] = None
    totalyearworkexperience: Optional[int] = None
    comment: Optional[str] = None
    gender_type_id: Optional[int] = None

class PersonUpdate(BaseModel):
    personal_id_number: Optional[constr(max_length=64)] = None
    birthdate: Optional[date] = None
    mothermaidenname: Optional[constr(max_length=128)] = None
    totalyearworkexperience: Optional[int] = None
    comment: Optional[str] = None
    gender_type_id: Optional[int] = None

class PersonOut(BaseModel):
    id: int
    personal_id_number: Optional[str] = None
    birthdate: Optional[date] = None
    mothermaidenname: Optional[str] = None
    totalyearworkexperience: Optional[int] = None
    comment: Optional[str] = None
    gender_type_id: Optional[int] = None
    gender_description: Optional[str] = None
    firstname: Optional[NameDetail] = None
    middlename: Optional[NameDetail] = None
    lastname: Optional[NameDetail] = None
    marital_status: Optional[MaritalStatusDetail] = None
    height: Optional[PhysicalCharacteristicDetail] = None
    weight: Optional[PhysicalCharacteristicDetail] = None
    citizenship: Optional[CitizenshipDetail] = None

    class Config:
        from_attributes = True