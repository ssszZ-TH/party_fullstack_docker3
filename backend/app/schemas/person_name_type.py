from pydantic import BaseModel, constr
from typing import Optional

class PersonNameTypeCreate(BaseModel):
    description: constr(max_length=128)

class PersonNameTypeUpdate(BaseModel):
    description: Optional[constr(max_length=128)] = None

class PersonNameTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True