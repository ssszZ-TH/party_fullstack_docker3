from pydantic import BaseModel, constr
from typing import Optional

class OtherInformalOrganizationCreate(BaseModel):
    name_en: constr(max_length=128)
    name_th: constr(max_length=128)

class OtherInformalOrganizationUpdate(BaseModel):
    name_en: Optional[constr(max_length=128)] = None
    name_th: Optional[constr(max_length=128)] = None

class OtherInformalOrganizationOut(BaseModel):
    id: int
    name_en: Optional[str] = None
    name_th: Optional[str] = None

    class Config:
        from_attributes = True