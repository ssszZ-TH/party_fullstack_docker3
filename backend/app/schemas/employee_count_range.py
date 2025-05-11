from pydantic import BaseModel, constr
from typing import Optional

class EmployeeCountRangeCreate(BaseModel):
    description: constr(max_length=128)

class EmployeeCountRangeUpdate(BaseModel):
    description: Optional[constr(max_length=128)] = None

class EmployeeCountRangeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True