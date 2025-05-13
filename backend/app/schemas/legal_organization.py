from pydantic import BaseModel, constr
from typing import Optional

class LegalOrganizationCreate(BaseModel):
    federal_tax_id_number: Optional[constr(max_length=64)] = None
    organization_id: int

class LegalOrganizationUpdate(BaseModel):
    federal_tax_id_number: Optional[constr(max_length=64)] = None

class LegalOrganizationOut(BaseModel):
    id: int
    federal_tax_id_number: Optional[str] = None
    organization_id: int

    class Config:
        from_attributes = True