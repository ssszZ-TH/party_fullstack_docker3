from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.government_agency import (
    create_government_agency, get_government_agency, get_all_government_agencies,
    update_government_agency, delete_government_agency
)
from app.schemas.government_agency import GovernmentAgencyCreate, GovernmentAgencyUpdate, GovernmentAgencyOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/governmentagency", tags=["government_agency"])

@router.post("/", response_model=GovernmentAgencyOut)
async def create_government_agency_endpoint(government_agency: GovernmentAgencyCreate, current_user: dict = Depends(get_current_user)):
    result = await create_government_agency(government_agency)
    if not result:
        logger.warning(f"ไม่สามารถสร้าง government agency")
        raise HTTPException(status_code=400, detail="ไม่สามารถสร้าง government agency")
    logger.info(f"สร้าง government agency: id={result.id}")
    return result

@router.get("/{government_agency_id}", response_model=GovernmentAgencyOut)
async def get_government_agency_endpoint(government_agency_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_government_agency(government_agency_id)
    if not result:
        logger.warning(f"ไม่พบ government agency: id={government_agency_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ government agency")
    logger.info(f"ดึงข้อมูล government agency: id={result.id}")
    return result

@router.get("/", response_model=List[GovernmentAgencyOut])
async def get_all_government_agencies_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_government_agencies()
    logger.info(f"ดึงข้อมูล {len(results)} government agencies")
    return results

@router.put("/{government_agency_id}", response_model=GovernmentAgencyOut)
async def update_government_agency_endpoint(government_agency_id: int, government_agency: GovernmentAgencyUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_government_agency(government_agency_id, government_agency)
    if not result:
        logger.warning(f"ไม่สามารถอัปเดต government agency: id={government_agency_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ government agency")
    logger.info(f"อัปเดต government agency: id={result.id}")
    return result

@router.delete("/{government_agency_id}")
async def delete_government_agency_endpoint(government_agency_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_government_agency(government_agency_id)
    if not result:
        logger.warning(f"ไม่พบ government agency สำหรับลบ: id={government_agency_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ government agency")
    logger.info(f"ลบ government agency: id={government_agency_id}")
    return {"message": "ลบ government agency เรียบร้อย"}