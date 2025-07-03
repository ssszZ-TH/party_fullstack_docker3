from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.party_relationship import (
    create_party_relationship, get_party_relationship, get_all_party_relationships,
    update_party_relationship, delete_party_relationship,
    get_party_relationships_by_from_party_role_id, get_party_relationships_by_to_party_role_id
)
from app.schemas.party_relationship import PartyRelationshipCreate, PartyRelationshipUpdate, PartyRelationshipOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/partyrelationship", tags=["partyrelationship"])

@router.post("/", response_model=PartyRelationshipOut)
async def create_party_relationship_endpoint(party_relationship: PartyRelationshipCreate, current_user: dict = Depends(get_current_user)):
    result = await create_party_relationship(party_relationship)
    if not result:
        logger.warning(f"Failed to create party_relationship")
        raise HTTPException(status_code=400, detail="Failed to create party_relationship")
    logger.info(f"Created party_relationship: id={result.id}")
    return result

@router.get("/{party_relationship_id}", response_model=PartyRelationshipOut)
async def get_party_relationship_endpoint(party_relationship_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_party_relationship(party_relationship_id)
    if not result:
        logger.warning(f"Party_relationship not found: id={party_relationship_id}")
        raise HTTPException(status_code=404, detail="Party_relationship not found")
    logger.info(f"Retrieved party_relationship: id={result.id}")
    return result

@router.get("/", response_model=List[PartyRelationshipOut])
async def get_all_party_relationships_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_party_relationships()
    logger.info(f"Retrieved {len(results)} party_relationships")
    return results

@router.get("/byfrompartyroleid/{from_party_role_id}", response_model=List[PartyRelationshipOut])
async def get_party_relationships_by_from_party_role_id_endpoint(from_party_role_id: int, current_user: dict = Depends(get_current_user)):
    results = await get_party_relationships_by_from_party_role_id(from_party_role_id)
    logger.info(f"Retrieved {len(results)} party_relationships for from_party_role_id={from_party_role_id}")
    return results

@router.get("/bytopartyroleid/{to_party_role_id}", response_model=List[PartyRelationshipOut])
async def get_party_relationships_by_to_party_role_id_endpoint(to_party_role_id: int, current_user: dict = Depends(get_current_user)):
    results = await get_party_relationships_by_to_party_role_id(to_party_role_id)
    logger.info(f"Retrieved {len(results)} party_relationships for to_party_role_id={to_party_role_id}")
    return results

@router.put("/{party_relationship_id}", response_model=PartyRelationshipOut)
async def update_party_relationship_endpoint(party_relationship_id: int, party_relationship: PartyRelationshipUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_party_relationship(party_relationship_id, party_relationship)
    if not result:
        logger.warning(f"Party_relationship not found for update: id={party_relationship_id}")
        raise HTTPException(status_code=404, detail="Party_relationship not found")
    logger.info(f"Updated party_relationship: id={result.id}")
    return result

@router.delete("/{party_relationship_id}")
async def delete_party_relationship_endpoint(party_relationship_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_party_relationship(party_relationship_id)
    if not result:
        logger.warning(f"Party_relationship not found for deletion: id={party_relationship_id}")
        raise HTTPException(status_code=404, detail="Party_relationship not found")
    logger.info(f"Deleted party_relationship: id={party_relationship_id}")
    return {"message": "Party_relationship deleted"}