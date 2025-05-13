from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.legal_organization import (
    create_legal_organization, get_legal_organization, get_all_legal_organizations,
    update_legal_organization, delete_legal_organization
)
from app.schemas.legal_organization import LegalOrganizationCreate, LegalOrganizationUpdate, LegalOrganizationOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/legalorganization", tags=["legalorganization"])

@router.post("/", response_model=LegalOrganizationOut)
async def create_legal_organization_endpoint(legal_organization: LegalOrganizationCreate, current_user: dict = Depends(get_current_user)):
    result = await create_legal_organization(legal_organization)
    if not result:
        logger.warning(f"Failed to create legal organization: federal_tax_id_number={legal_organization.federal_tax_id_number}")
        raise HTTPException(status_code=400, detail="Legal organization already exists")
    logger.info(f"Created legal organization: id={result.id}")
    return result

@router.get("/{legal_organization_id}", response_model=LegalOrganizationOut)
async def get_legal_organization_endpoint(legal_organization_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_legal_organization(legal_organization_id)
    if not result:
        logger.warning(f"Legal organization not found: id={legal_organization_id}")
        raise HTTPException(status_code=404, detail="Legal organization not found")
    logger.info(f"Retrieved legal organization: id={result.id}")
    return result

@router.get("/", response_model=List[LegalOrganizationOut])
async def get_all_legal_organizations_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_legal_organizations()
    logger.info(f"Retrieved {len(results)} legal organizations")
    return results

@router.put("/{legal_organization_id}", response_model=LegalOrganizationOut)
async def update_legal_organization_endpoint(legal_organization_id: int, legal_organization: LegalOrganizationUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_legal_organization(legal_organization_id, legal_organization)
    if not result:
        logger.warning(f"Failed to update legal organization: id={legal_organization_id}")
        raise HTTPException(status_code=404, detail="Legal organization not found or federal_tax_id_number already exists")
    logger.info(f"Updated legal organization: id={result.id}")
    return result

@router.delete("/{legal_organization_id}")
async def delete_legal_organization_endpoint(legal_organization_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_legal_organization(legal_organization_id)
    if not result:
        logger.warning(f"Legal organization not found for deletion: id={legal_organization_id}")
        raise HTTPException(status_code=404, detail="Legal organization not found")
    logger.info(f"Deleted legal organization: id={legal_organization_id}")
    return {"message": "Legal organization deleted"}