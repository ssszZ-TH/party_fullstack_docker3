from pydantic import BaseModel
from typing import Optional

class CommunicationEventPurposeTypeCreate(BaseModel):
    description: str

class CommunicationEventPurposeTypeUpdate(BaseModel):
    description: Optional[str] = None

class CommunicationEventPurposeTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True