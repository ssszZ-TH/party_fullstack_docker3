from pydantic import BaseModel, constr
from typing import Optional

class LegalOrganizationCreate(BaseModel):
    name_en: constr(max_length=128)
    name_th: constr(max_length=128)
    federal_tax_id_number: Optional[constr(max_length=64)] = None

class LegalOrganizationUpdate(BaseModel):
    name_en: Optional[constr(max_length=128)] = None
    name_th: Optional[constr(max_length=128)] = None
    federal_tax_id_number: Optional[constr(max_length=64)] = None

class LegalOrganizationOut(BaseModel):
    id: int
    name_en: str
    name_th: str
    federal_tax_id_number: Optional[str] = None

    class Config:
        from_attributes = True