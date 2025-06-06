from pydantic import BaseModel
from typing import Optional
from datetime import date

class PersonCreate(BaseModel):
    personal_id_number: Optional[str] = None
    birthdate: Optional[date] = None
    mothermaidenname: Optional[str] = None
    totalyearworkexperience: Optional[int] = None
    comment: Optional[str] = None
    gender_type_id: Optional[int] = None
    fname: Optional[str] = None
    mname: Optional[str] = None
    lname: Optional[str] = None
    nickname: Optional[str] = None
    marital_status_type_id: Optional[int] = None
    height_val: Optional[float] = None
    weight_val: Optional[float] = None
    country_id: Optional[int] = None

    class Config:
        orm_mode = True

class PersonUpdate(PersonCreate):
    pass

class PersonOut(PersonCreate):
    id: int
    gender_description: Optional[str] = None
    fname_id: Optional[int] = None
    fname_fromdate: Optional[date] = None
    fname_thrudate: Optional[date] = None
    fname_personnametype_id: Optional[int] = None
    fname_personnametype_description: Optional[str] = None
    mname_id: Optional[int] = None
    mname_fromdate: Optional[date] = None
    mname_thrudate: Optional[date] = None
    mname_personnametype_id: Optional[int] = None
    mname_personnametype_description: Optional[str] = None
    lname_id: Optional[int] = None
    lname_fromdate: Optional[date] = None
    lname_thrudate: Optional[date] = None
    lname_personnametype_id: Optional[int] = None
    lname_personnametype_description: Optional[str] = None
    nickname_id: Optional[int] = None
    nickname_fromdate: Optional[date] = None
    nickname_thrudate: Optional[date] = None
    nickname_personnametype_id: Optional[int] = None
    nickname_personnametype_description: Optional[str] = None
    marital_status_id: Optional[int] = None
    marital_status_fromdate: Optional[date] = None
    marital_status_thrudate: Optional[date] = None
    marital_status_type_description: Optional[str] = None
    height_id: Optional[int] = None
    height_fromdate: Optional[date] = None
    height_thrudate: Optional[date] = None
    height_type_id: Optional[int] = None
    height_type_description: Optional[str] = None
    weight_id: Optional[int] = None
    weight_fromdate: Optional[date] = None
    weight_thrudate: Optional[date] = None
    weight_type_id: Optional[int] = None
    weight_type_description: Optional[str] = None
    citizenship_id: Optional[int] = None
    citizenship_fromdate: Optional[date] = None
    citizenship_thrudate: Optional[date] = None
    country_isocode: Optional[str] = None
    country_name_en: Optional[str] = None
    country_name_th: Optional[str] = None

    class Config:
        orm_mode = True