from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.other_informal_organization import (
    create_other_informal_organization, get_other_informal_organization, get_all_other_informal_organizations,
    update_other_informal_organization, delete_other_informal_organization
)
from app.schemas.other_informal_organization import OtherInformalOrganizationCreate, OtherInformalOrganizationUpdate, OtherInformalOrganizationOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/otherinformalorganization", tags=["otherinformalorganization"])

@router.post("/", response_model=OtherInformalOrganizationOut)
async def create_other_informal_organization_endpoint(other_informal_organization: OtherInformalOrganizationCreate, current_user: dict = Depends(get_current_user)):
    result = await create_other_informal_organization(other_informal_organization)
    if not result:
        logger.warning(f"ไม่สามารถสร้าง other informal organization")
        raise HTTPException(status_code=400, detail="ไม่สามารถสร้าง other informal organization")
    logger.info(f"สร้าง other informal organization: id={result.id}")
    return result

@router.get("/{other_informal_organization_id}", response_model=OtherInformalOrganizationOut)
async def get_other_informal_organization_endpoint(other_informal_organization_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_other_informal_organization(other_informal_organization_id)
    if not result:
        logger.warning(f"ไม่พบ other informal organization: id={other_informal_organization_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ other informal organization")
    logger.info(f"ดึงข้อมูล other informal organization: id={result.id}")
    return result

@router.get("/", response_model=List[OtherInformalOrganizationOut])
async def get_all_other_informal_organizations_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_other_informal_organizations()
    logger.info(f"ดึงข้อมูล {len(results)} other informal organizations")
    return results

@router.put("/{other_informal_organization_id}", response_model=OtherInformalOrganizationOut)
async def update_other_informal_organization_endpoint(other_informal_organization_id: int, other_informal_organization: OtherInformalOrganizationUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_other_informal_organization(other_informal_organization_id, other_informal_organization)
    if not result:
        logger.warning(f"ไม่สามารถอัปเดต other informal organization: id={other_informal_organization_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ other informal organization")
    logger.info(f"อัปเดต other informal organization: id={result.id}")
    return result

@router.delete("/{other_informal_organization_id}")
async def delete_other_informal_organization_endpoint(other_informal_organization_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_other_informal_organization(other_informal_organization_id)
    if not result:
        logger.warning(f"ไม่พบ other informal organization สำหรับลบ: id={other_informal_organization_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ other informal organization")
    logger.info(f"ลบ other informal organization: id={other_informal_organization_id}")
    return {"message": "ลบ other informal organization เรียบร้อย"}