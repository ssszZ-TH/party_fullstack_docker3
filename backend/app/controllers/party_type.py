from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.party_type import (
    create_party_type, get_party_type, get_all_party_types,
    update_party_type, delete_party_type
)
from app.schemas.party_type import PartyTypeCreate, PartyTypeUpdate, PartyTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/partytype", tags=["party_type"])

@router.post("/", response_model=PartyTypeOut)
async def create_party_type_endpoint(party_type: PartyTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_party_type(party_type)
    if not result:
        logger.warning(f"Failed to create party type: description={party_type.description}")
        raise HTTPException(status_code=400, detail="Description already exists")
    logger.info(f"Created party type: id={result.id}, description={result.description}")
    return result

@router.get("/{party_type_id}", response_model=PartyTypeOut)
async def get_party_type_endpoint(party_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_party_type(party_type_id)
    if not result:
        logger.warning(f"Party type not found: id={party_type_id}")
        raise HTTPException(status_code=404, detail="Party type not found")
    logger.info(f"Retrieved party type: id={result.id}, description={result.description}")
    return result

@router.get("/", response_model=List[PartyTypeOut])
async def get_all_party_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_party_types()
    logger.info(f"Retrieved {len(results)} party types")
    return results

@router.put("/{party_type_id}", response_model=PartyTypeOut)
async def update_party_type_endpoint(party_type_id: int, party_type: PartyTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_party_type(party_type_id, party_type)
    if not result:
        logger.warning(f"Failed to update party type: id={party_type_id}")
        raise HTTPException(status_code=404, detail="Party type not found or description already exists")
    logger.info(f"Updated party type: id={result.id}, description={result.description}")
    return result

@router.delete("/{party_type_id}")
async def delete_party_type_endpoint(party_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_party_type(party_type_id)
    if not result:
        logger.warning(f"Party type not found for deletion: id={party_type_id}")
        raise HTTPException(status_code=404, detail="Party type not found or referenced in party_classification")
    logger.info(f"Deleted party type: id={party_type_id}")
    return {"message": "Party type deleted"}