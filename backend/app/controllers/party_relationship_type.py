from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.party_relationship_type import (
    create_party_relationship_type, get_party_relationship_type, get_all_party_relationship_types,
    update_party_relationship_type, delete_party_relationship_type
)
from app.schemas.party_relationship_type import PartyRelationshipTypeCreate, PartyRelationshipTypeUpdate, PartyRelationshipTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/partyrelationshiptypes", tags=["partyrelationshiptypes"])

@router.post("/", response_model=PartyRelationshipTypeOut)
async def create_party_relationship_type_endpoint(party_relationship_type: PartyRelationshipTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_party_relationship_type(party_relationship_type)
    if not result:
        logger.warning(f"Failed to create party_relationship_type")
        raise HTTPException(status_code=400, detail="Failed to create party_relationship_type")
    logger.info(f"Created party_relationship_type: id={result.id}")
    return result

@router.get("/{party_relationship_type_id}", response_model=PartyRelationshipTypeOut)
async def get_party_relationship_type_endpoint(party_relationship_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_party_relationship_type(party_relationship_type_id)
    if not result:
        logger.warning(f"Party_relationship_type not found: id={party_relationship_type_id}")
        raise HTTPException(status_code=404, detail="Party_relationship_type not found")
    logger.info(f"Retrieved party_relationship_type: id={result.id}")
    return result

@router.get("/", response_model=List[PartyRelationshipTypeOut])
async def get_all_party_relationship_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_party_relationship_types()
    logger.info(f"Retrieved {len(results)} party_relationship_types")
    return results

@router.put("/{party_relationship_type_id}", response_model=PartyRelationshipTypeOut)
async def update_party_relationship_type_endpoint(party_relationship_type_id: int, party_relationship_type: PartyRelationshipTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_party_relationship_type(party_relationship_type_id, party_relationship_type)
    if not result:
        logger.warning(f"Party_relationship_type not found for update: id={party_relationship_type_id}")
        raise HTTPException(status_code=404, detail="Party_relationship_type not found")
    logger.info(f"Updated party_relationship_type: id={result.id}")
    return result

@router.delete("/{party_relationship_type_id}")
async def delete_party_relationship_type_endpoint(party_relationship_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_party_relationship_type(party_relationship_type_id)
    if not result:
        logger.warning(f"Party_relationship_type not found for deletion: id={party_relationship_type_id}")
        raise HTTPException(status_code=404, detail="Party_relationship_type not found")
    logger.info(f"Deleted party_relationship_type: id={party_relationship_type_id}")
    return {"message": "Party_relationship_type deleted"}