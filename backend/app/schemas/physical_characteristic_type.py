from pydantic import BaseModel, constr
from typing import Optional

class PhysicalCharacteristicTypeCreate(BaseModel):
    description: constr(max_length=128)

class PhysicalCharacteristicTypeUpdate(BaseModel):
    description: Optional[constr(max_length=128)] = None

class PhysicalCharacteristicTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True