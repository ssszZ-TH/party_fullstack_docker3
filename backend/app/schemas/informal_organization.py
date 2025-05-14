from pydantic import BaseModel, constr
from typing import Optional

class InformalOrganizationCreate(BaseModel):
    name_en: constr(max_length=128)
    name_th: constr(max_length=128)

class InformalOrganizationUpdate(BaseModel):
    name_en: Optional[constr(max_length=128)] = None
    name_th: Optional[constr(max_length=128)] = None

class InformalOrganizationOut(BaseModel):
    id: int
    name_en: str
    name_th: str

    class Config:
        from_attributes = True