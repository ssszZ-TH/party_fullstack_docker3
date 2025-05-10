from pydantic import BaseModel, constr
from typing import Optional

class MaritalStatusTypeCreate(BaseModel):
    description: constr(max_length=128)

class MaritalStatusTypeUpdate(BaseModel):
    description: Optional[constr(max_length=128)] = None

class MaritalStatusTypeOut(BaseModel):
    id: int
    description: Optional[str] = None

    class Config:
        from_attributes = True