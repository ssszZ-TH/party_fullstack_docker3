from pydantic import BaseModel, constr
from typing import Optional

class GenderTypeCreate(BaseModel):
    description: constr(max_length=128)

class GenderTypeUpdate(BaseModel):
    description: Optional[constr(max_length=128)] = None

class GenderTypeOut(BaseModel):
    id: int
    description: Optional[str] = None

    class Config:
        from_attributes = True