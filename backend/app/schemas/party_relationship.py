from pydantic import BaseModel
from typing import Optional
from datetime import date

class PartyRelationshipCreate(BaseModel):
    from_date: Optional[date] = None
    thru_date: Optional[date] = None
    comment: Optional[str] = None
    from_party_role_id: int
    to_party_role_id: int
    party_relationship_type_id: int
    priority_type_id: int
    party_relationship_status_type_id: int

class PartyRelationshipUpdate(BaseModel):
    from_date: Optional[date] = None
    thru_date: Optional[date] = None
    comment: Optional[str] = None
    from_party_role_id: Optional[int] = None
    to_party_role_id: Optional[int] = None
    party_relationship_type_id: Optional[int] = None
    priority_type_id: Optional[int] = None
    party_relationship_status_type_id: Optional[int] = None

class PartyRelationshipOut(BaseModel):
    id: int
    from_date: Optional[date] = None
    thru_date: Optional[date] = None
    comment: Optional[str] = None
    from_party_role_id: int
    to_party_role_id: int
    party_relationship_type_id: int
    priority_type_id: int
    party_relationship_status_type_id: int
    party_relationship_type_description: Optional[str] = None
    priority_type_description: Optional[str] = None
    party_relationship_status_type_description: Optional[str] = None

    class Config:
        from_attributes = True