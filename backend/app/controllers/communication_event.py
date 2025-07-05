from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.communication_event import (
    create_communication_event, get_communication_event, get_all_communication_events,
    update_communication_event, delete_communication_event, get_communication_events_by_party_relationship_id
)
from app.schemas.communication_event import CommunicationEventCreate, CommunicationEventUpdate, CommunicationEventOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/communicationevent", tags=["communicationevent"])

@router.post("/", response_model=CommunicationEventOut)
async def create_communication_event_endpoint(communication_event: CommunicationEventCreate, current_user: dict = Depends(get_current_user)):
    result = await create_communication_event(communication_event)
    if not result:
        logger.warning(f"Failed to create communication_event")
        raise HTTPException(status_code=400, detail="Failed to create communication_event")
    logger.info(f"Created communication_event: id={result.id}")
    return result

@router.get("/{communication_event_id}", response_model=CommunicationEventOut)
async def get_communication_event_endpoint(communication_event_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_communication_event(communication_event_id)
    if not result:
        logger.warning(f"Communication_event not found: id={communication_event_id}")
        raise HTTPException(status_code=404, detail="Communication_event not found")
    logger.info(f"Retrieved communication_event: id={result.id}")
    return result

@router.get("/", response_model=List[CommunicationEventOut])
async def get_all_communication_events_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_communication_events()
    logger.info(f"Retrieved {len(results)} communication_events")
    return results

@router.get("/bypartyrelationshipid/{party_relationship_id}", response_model=List[CommunicationEventOut])
async def get_communication_events_by_party_relationship_id_endpoint(party_relationship_id: int, current_user: dict = Depends(get_current_user)):
    results = await get_communication_events_by_party_relationship_id(party_relationship_id)
    logger.info(f"Retrieved {len(results)} communication_events for party_relationship_id={party_relationship_id}")
    return results

@router.put("/{communication_event_id}", response_model=CommunicationEventOut)
async def update_communication_event_endpoint(communication_event_id: int, communication_event: CommunicationEventUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_communication_event(communication_event_id, communication_event)
    if not result:
        logger.warning(f"Communication_event not found for update: id={communication_event_id}")
        raise HTTPException(status_code=404, detail="Communication_event not found")
    logger.info(f"Updated communication_event: id={result.id}")
    return result

@router.delete("/{communication_event_id}")
async def delete_communication_event_endpoint(communication_event_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_communication_event(communication_event_id)
    if not result:
        logger.warning(f"Communication_event not found for deletion: id={communication_event_id}")
        raise HTTPException(status_code=404, detail="Communication_event not found")
    logger.info(f"Deleted communication_event: id={communication_event_id}")
    return {"message": "Communication_event deleted"}