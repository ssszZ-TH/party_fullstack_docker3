from pydantic import BaseModel
from typing import Optional

class CommunicationEventPurposeCreate(BaseModel):
    communication_event_id: int
    communication_event_purpose_type_id: int

class CommunicationEventPurposeUpdate(BaseModel):
    communication_event_id: Optional[int] = None
    communication_event_purpose_type_id: Optional[int] = None

class CommunicationEventPurposeOut(BaseModel):
    id: int
    communication_event_id: int
    communication_event_purpose_type_id: int
    communication_event_note: Optional[str] = None
    communication_event_purpose_type_description: Optional[str] = None

    class Config:
        from_attributes = True