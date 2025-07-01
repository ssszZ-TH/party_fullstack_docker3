from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.communication_event_purpose_type import (
    create_communication_event_purpose_type, get_communication_event_purpose_type, get_all_communication_event_purpose_types,
    update_communication_event_purpose_type, delete_communication_event_purpose_type
)
from app.schemas.communication_event_purpose_type import CommunicationEventPurposeTypeCreate, CommunicationEventPurposeTypeUpdate, CommunicationEventPurposeTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/communicationeventpurposetype", tags=["communicationeventpurposetype"])

@router.post("/", response_model=CommunicationEventPurposeTypeOut)
async def create_communication_event_purpose_type_endpoint(communication_event_purpose_type: CommunicationEventPurposeTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_communication_event_purpose_type(communication_event_purpose_type)
    if not result:
        logger.warning(f"Failed to create communication_event_purpose_type")
        raise HTTPException(status_code=400, detail="Failed to create communication_event_purpose_type")
    logger.info(f"Created communication_event_purpose_type: id={result.id}")
    return result

@router.get("/{communication_event_purpose_type_id}", response_model=CommunicationEventPurposeTypeOut)
async def get_communication_event_purpose_type_endpoint(communication_event_purpose_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_communication_event_purpose_type(communication_event_purpose_type_id)
    if not result:
        logger.warning(f"Communication_event_purpose_type not found: id={communication_event_purpose_type_id}")
        raise HTTPException(status_code=404, detail="Communication_event_purpose_type not found")
    logger.info(f"Retrieved communication_event_purpose_type: id={result.id}")
    return result

@router.get("/", response_model=List[CommunicationEventPurposeTypeOut])
async def get_all_communication_event_purpose_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_communication_event_purpose_types()
    logger.info(f"Retrieved {len(results)} communication_event_purpose_types")
    return results

@router.put("/{communication_event_purpose_type_id}", response_model=CommunicationEventPurposeTypeOut)
async def update_communication_event_purpose_type_endpoint(communication_event_purpose_type_id: int, communication_event_purpose_type: CommunicationEventPurposeTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_communication_event_purpose_type(communication_event_purpose_type_id, communication_event_purpose_type)
    if not result:
        logger.warning(f"Communication_event_purpose_type not found for update: id={communication_event_purpose_type_id}")
        raise HTTPException(status_code=404, detail="Communication_event_purpose_type not found")
    logger.info(f"Updated communication_event_purpose_type: id={result.id}")
    return result

@router.delete("/{communication_event_purpose_type_id}")
async def delete_communication_event_purpose_type_endpoint(communication_event_purpose_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_communication_event_purpose_type(communication_event_purpose_type_id)
    if not result:
        logger.warning(f"Communication_event_purpose_type not found for deletion: id={communication_event_purpose_type_id}")
        raise HTTPException(status_code=404, detail="Communication_event_purpose_type not found")
    logger.info(f"Deleted communication_event_purpose_type: id={communication_event_purpose_type_id}")
    return {"message": "Communication_event_purpose_type deleted"}