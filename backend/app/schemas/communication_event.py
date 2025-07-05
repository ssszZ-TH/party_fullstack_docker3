from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommunicationEventCreate(BaseModel):
    datetime_start: Optional[datetime] = None
    datetime_end: Optional[datetime] = None
    note: Optional[str] = None
    contact_mechanism_type_id: int
    communication_event_status_type_id: int
    party_relationship_id: int

class CommunicationEventUpdate(BaseModel):
    datetime_start: Optional[datetime] = None
    datetime_end: Optional[datetime] = None
    note: Optional[str] = None
    contact_mechanism_type_id: Optional[int] = None
    communication_event_status_type_id: Optional[int] = None
    party_relationship_id: Optional[int] = None

class CommunicationEventOut(BaseModel):
    id: int
    datetime_start: Optional[datetime] = None
    datetime_end: Optional[datetime] = None
    note: Optional[str] = None
    contact_mechanism_type_id: int
    communication_event_status_type_id: int
    party_relationship_id: int
    contact_mechanism_type_description: Optional[str] = None
    communication_event_status_type_description: Optional[str] = None
    party_relationship_comment: Optional[str] = None

    class Config:
        from_attributes = True