from pydantic import BaseModel, constr
from typing import Optional

class TeamCreate(BaseModel):
    name_en: constr(max_length=128)
    name_th: constr(max_length=128)

class TeamUpdate(BaseModel):
    name_en: Optional[constr(max_length=128)] = None
    name_th: Optional[constr(max_length=128)] = None

class TeamOut(BaseModel):
    id: int
    name_en: Optional[str] = None
    name_th: Optional[str] = None

    class Config:
        from_attributes = True