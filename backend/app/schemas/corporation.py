from pydantic import BaseModel, constr
from typing import Optional

class CorporationCreate(BaseModel):
    name_en: constr(max_length=128)
    name_th: constr(max_length=128)
    federal_tax_id_number: Optional[constr(max_length=64)] = None

class CorporationUpdate(BaseModel):
    name_en: Optional[constr(max_length=128)] = None
    name_th: Optional[constr(max_length=128)] = None
    federal_tax_id_number: Optional[constr(max_length=64)] = None

class CorporationOut(BaseModel):
    id: int
    name_en: Optional[str] = None
    name_th: Optional[str] = None
    federal_tax_id_number: Optional[str] = None

    class Config:
        from_attributes = True