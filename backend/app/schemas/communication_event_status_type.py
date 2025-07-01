from pydantic import BaseModel
from typing import Optional

class CommunicationEventStatusTypeCreate(BaseModel):
    description: str

class CommunicationEventStatusTypeUpdate(BaseModel):
    description: Optional[str] = None

class CommunicationEventStatusTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True