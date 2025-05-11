from pydantic import BaseModel, constr
from typing import Optional

class IncomeRangeCreate(BaseModel):
    description: constr(max_length=128)

class IncomeRangeUpdate(BaseModel):
    description: Optional[constr(max_length=128)] = None

class IncomeRangeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True