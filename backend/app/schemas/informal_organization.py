from pydantic import BaseModel
from typing import Optional

class InformalOrganizationCreate(BaseModel):
    organization_id: int

class InformalOrganizationUpdate(BaseModel):
    pass

class InformalOrganizationOut(BaseModel):
    id: int
    organization_id: int

    class Config:
        from_attributes = True