from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.informal_organization import (
    create_informal_organization, get_informal_organization, get_all_informal_organizations,
    update_informal_organization, delete_informal_organization
)
from app.schemas.informal_organization import InformalOrganizationCreate, InformalOrganizationUpdate, InformalOrganizationOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/informalorganization", tags=["informalorganization"])

@router.post("/", response_model=InformalOrganizationOut)
async def create_informal_organization_endpoint(informal_organization: InformalOrganizationCreate, current_user: dict = Depends(get_current_user)):
    result = await create_informal_organization(informal_organization)
    if not result:
        logger.warning(f"Failed to create informal organization")
        raise HTTPException(status_code=400, detail="Failed to create informal organization")
    logger.info(f"Created informal organization: id={result.id}")
    return result

@router.get("/{informal_organization_id}", response_model=InformalOrganizationOut)
async def get_informal_organization_endpoint(informal_organization_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_informal_organization(informal_organization_id)
    if not result:
        logger.warning(f"Informal organization not found: id={informal_organization_id}")
        raise HTTPException(status_code=404, detail="Informal organization not found")
    logger.info(f"Retrieved informal organization: id={result.id}")
    return result

@router.get("/", response_model=List[InformalOrganizationOut])
async def get_all_informal_organizations_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_informal_organizations()
    logger.info(f"Retrieved {len(results)} informal organizations")
    return results

@router.put("/{informal_organization_id}", response_model=InformalOrganizationOut)
async def update_informal_organization_endpoint(informal_organization_id: int, informal_organization: InformalOrganizationUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_informal_organization(informal_organization_id, informal_organization)
    if not result:
        logger.warning(f"Failed to update informal organization: id={informal_organization_id}")
        raise HTTPException(status_code=404, detail="Informal organization not found")
    logger.info(f"Updated informal organization: id={result.id}")
    return result

@router.delete("/{informal_organization_id}")
async def delete_informal_organization_endpoint(informal_organization_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_informal_organization(informal_organization_id)
    if not result:
        logger.warning(f"Informal organization not found for deletion: id={informal_organization_id}")
        raise HTTPException(status_code=404, detail="Informal organization not found")
    logger.info(f"Deleted informal organization: id={informal_organization_id}")
    return {"message": "Informal organization deleted"}