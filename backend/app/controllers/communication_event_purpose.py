from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.communication_event_purpose import (
    create_communication_event_purpose, get_communication_event_purpose, get_all_communication_event_purposes,
    update_communication_event_purpose, delete_communication_event_purpose,
    get_communication_event_purposes_by_communication_event_id
)
from app.schemas.communication_event_purpose import CommunicationEventPurposeCreate, CommunicationEventPurposeUpdate, CommunicationEventPurposeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/communicationeventpurpose", tags=["communicationeventpurpose"])

@router.post("/", response_model=CommunicationEventPurposeOut)
async def create_communication_event_purpose_endpoint(communication_event_purpose: CommunicationEventPurposeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_communication_event_purpose(communication_event_purpose)
    if not result:
        logger.warning(f"Failed to create communication_event_purpose")
        raise HTTPException(status_code=400, detail="Failed to create communication_event_purpose")
    logger.info(f"Created communication_event_purpose: id={result.id}")
    return result

@router.get("/{communication_event_purpose_id}", response_model=CommunicationEventPurposeOut)
async def get_communication_event_purpose_endpoint(communication_event_purpose_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_communication_event_purpose(communication_event_purpose_id)
    if not result:
        logger.warning(f"Communication_event_purpose not found: id={communication_event_purpose_id}")
        raise HTTPException(status_code=404, detail="Communication_event_purpose not found")
    logger.info(f"Retrieved communication_event_purpose: id={result.id}")
    return result

@router.get("/", response_model=List[CommunicationEventPurposeOut])
async def get_all_communication_event_purposes_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_communication_event_purposes()
    logger.info(f"Retrieved {len(results)} communication_event_purposes")
    return results

@router.get("/bycommunicationeventid/{communication_event_id}", response_model=List[CommunicationEventPurposeOut])
async def get_communication_event_purposes_by_communication_event_id_endpoint(communication_event_id: int, current_user: dict = Depends(get_current_user)):
    results = await get_communication_event_purposes_by_communication_event_id(communication_event_id)
    logger.info(f"Retrieved {len(results)} communication_event_purposes for communication_event_id={communication_event_id}")
    return results

@router.put("/{communication_event_purpose_id}", response_model=CommunicationEventPurposeOut)
async def update_communication_event_purpose_endpoint(communication_event_purpose_id: int, communication_event_purpose: CommunicationEventPurposeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_communication_event_purpose(communication_event_purpose_id, communication_event_purpose)
    if not result:
        logger.warning(f"Communication_event_purpose not found for update: id={communication_event_purpose_id}")
        raise HTTPException(status_code=404, detail="Communication_event_purpose not found")
    logger.info(f"Updated communication_event_purpose: id={result.id}")
    return result

@router.delete("/{communication_event_purpose_id}")
async def delete_communication_event_purpose_endpoint(communication_event_purpose_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_communication_event_purpose(communication_event_purpose_id)
    if not result:
        logger.warning(f"Communication_event_purpose not found for deletion: id={communication_event_purpose_id}")
        raise HTTPException(status_code=404, detail="Communication_event_purpose not found")
    logger.info(f"Deleted communication_event_purpose: id={communication_event_purpose_id}")
    return {"message": "Communication_event_purpose deleted"}