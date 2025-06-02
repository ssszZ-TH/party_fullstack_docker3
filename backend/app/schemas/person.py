from pydantic import BaseModel, constr
from typing import Optional
from datetime import date

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
    personal_id_number: Optional[str]
    birthdate: Optional[date]
    mothermaidenname: Optional[str]
    totalyearworkexperience: Optional[int]
    comment: Optional[str]
    gender_type_id: Optional[int]
    gender_description: Optional[str]
    fname_id: Optional[int]
    fname: Optional[str]
    fname_fromdate: Optional[date]
    fname_thrudate: Optional[date]
    fname_personnametype_id: Optional[int]
    fname_personnametype_description: Optional[str]
    mname_id: Optional[int]
    mname: Optional[str]
    mname_fromdate: Optional[date]
    mname_thrudate: Optional[date]
    mname_personnametype_id: Optional[int]
    mname_personnametype_description: Optional[str]
    lname_id: Optional[int]
    lname: Optional[str]
    lname_fromdate: Optional[date]
    lname_thrudate: Optional[date]
    lname_personnametype_id: Optional[int]
    lname_personnametype_description: Optional[str]
    nickname_id: Optional[int]  # เพิ่ม
    nickname: Optional[str]  # เพิ่ม
    nickname_fromdate: Optional[date]  # เพิ่ม
    nickname_thrudate: Optional[date]  # เพิ่ม
    nickname_personnametype_id: Optional[int]  # เพิ่ม
    nickname_personnametype_description: Optional[str]  # เพิ่ม
    marital_status_id: Optional[int]
    marital_status_fromdate: Optional[date]
    marital_status_thrudate: Optional[date]
    marital_status_type_id: Optional[int]
    marital_status_type_description: Optional[str]
    height_id: Optional[int]
    height_val: Optional[float]
    height_fromdate: Optional[date]
    height_thrudate: Optional[date]
    height_type_id: Optional[int]
    height_type_description: Optional[str]
    weight_id: Optional[int]
    weight_val: Optional[float]
    weight_fromdate: Optional[date]
    weight_thrudate: Optional[date]
    weight_type_id: Optional[int]
    weight_type_description: Optional[str]
    citizenship_id: Optional[int]
    citizenship_fromdate: Optional[date]
    citizenship_thrudate: Optional[date]
    country_id: Optional[int]
    country_isocode: Optional[str]
    country_name_en: Optional[str]
    country_name_th: Optional[str]

    class Config:
        orm_mode = True