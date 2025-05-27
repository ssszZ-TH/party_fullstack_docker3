from pydantic import BaseModel, constr
from typing import Optional

class MinorityTypeCreate(BaseModel):
    name_en: constr(max_length=128)
    name_th: Optional[constr(max_length=128)] = None

class MinorityTypeUpdate(BaseModel):
    name_en: Optional[constr(max_length=128)] = None
    name_th: Optional[constr(max_length=128)] = None

class MinorityTypeOut(BaseModel):
    id: int
    name_en: Optional[str] = None
    name_th: Optional[str] = None

    class Config:
        from_attributes = True