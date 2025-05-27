from pydantic import BaseModel, constr
from typing import Optional

class IndustryTypeCreate(BaseModel):
    naics_code: constr(max_length=64)
    description: Optional[constr(max_length=128)] = None

class IndustryTypeUpdate(BaseModel):
    naics_code: Optional[constr(max_length=64)] = None
    description: Optional[constr(max_length=128)] = None

class IndustryTypeOut(BaseModel):
    id: int
    naics_code: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True