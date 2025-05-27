from pydantic import BaseModel, constr
from typing import Optional

class CountryCreate(BaseModel):
    isocode: constr(max_length=2)
    name_en: constr(max_length=128)
    name_th: Optional[constr(max_length=128)] = None

class CountryUpdate(BaseModel):
    isocode: Optional[constr(max_length=2)] = None
    name_en: Optional[constr(max_length=128)] = None
    name_th: Optional[constr(max_length=128)] = None

class CountryOut(BaseModel):
    id: int
    isocode: Optional[str] = None
    name_en: Optional[str] = None
    name_th: Optional[str] = None

    class Config:
        from_attributes = True