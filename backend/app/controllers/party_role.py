from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.party_role import (
    create_party_role, get_party_role, get_all_party_roles,
    update_party_role, delete_party_role, get_party_roles_by_party_id
)
from app.schemas.party_role import PartyRoleCreate, PartyRoleUpdate, PartyRoleOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/partyrole", tags=["partyrole"])

@router.post("/", response_model=PartyRoleOut)
async def create_party_role_endpoint(party_role: PartyRoleCreate, current_user: dict = Depends(get_current_user)):
    result = await create_party_role(party_role)
    if not result:
        logger.warning(f"Failed to create party_role")
        raise HTTPException(status_code=400, detail="Failed to create party_role")
    logger.info(f"Created party_role: id={result.id}")
    return result

@router.get("/{party_role_id}", response_model=PartyRoleOut)
async def get_party_role_endpoint(party_role_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_party_role(party_role_id)
    if not result:
        logger.warning(f"Party_role not found: id={party_role_id}")
        raise HTTPException(status_code=404, detail="Party_role not found")
    logger.info(f"Retrieved party_role: id={result.id}")
    return result

@router.get("/", response_model=List[PartyRoleOut])
async def get_all_party_roles_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_party_roles()
    logger.info(f"Retrieved {len(results)} party_roles")
    return results

@router.get("/bypartyid/{party_id}", response_model=List[PartyRoleOut])
async def get_party_roles_by_party_id_endpoint(party_id: int, current_user: dict = Depends(get_current_user)):
    results = await get_party_roles_by_party_id(party_id)
    logger.info(f"Retrieved {len(results)} party_roles for party_id={party_id}")
    return results

@router.put("/{party_role_id}", response_model=PartyRoleOut)
async def update_party_role_endpoint(party_role_id: int, party_role: PartyRoleUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_party_role(party_role_id, party_role)
    if not result:
        logger.warning(f"Party_role not found for update: id={party_role_id}")
        raise HTTPException(status_code=404, detail="Party_role not found")
    logger.info(f"Updated party_role: id={result.id}")
    return result

@router.delete("/{party_role_id}")
async def delete_party_role_endpoint(party_role_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_party_role(party_role_id)
    if not result:
        logger.warning(f"Party_role not found for deletion: id={party_role_id}")
        raise HTTPException(status_code=404, detail="Party_role not found")
    logger.info(f"Deleted party_role: id={party_role_id}")
    return {"message": "Party_role deleted"}