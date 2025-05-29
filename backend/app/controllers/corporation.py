from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.corporation import (
    create_corporation, get_corporation, get_all_corporations,
    update_corporation, delete_corporation
)
from app.schemas.corporation import CorporationCreate, CorporationUpdate, CorporationOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/corporation", tags=["corporation"])

@router.post("/", response_model=CorporationOut)
async def create_corporation_endpoint(corporation: CorporationCreate, current_user: dict = Depends(get_current_user)):
    result = await create_corporation(corporation)
    if not result:
        logger.warning(f"ไม่สามารถสร้าง corporation")
        raise HTTPException(status_code=400, detail="ไม่สามารถสร้าง corporation")
    logger.info(f"สร้าง corporation: id={result.id}")
    return result

@router.get("/{corporation_id}", response_model=CorporationOut)
async def get_corporation_endpoint(corporation_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_corporation(corporation_id)
    if not result:
        logger.warning(f"ไม่พบ corporation: id={corporation_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ corporation")
    logger.info(f"ดึงข้อมูล corporation: id={result.id}")
    return result

@router.get("/", response_model=List[CorporationOut])
async def get_all_corporations_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_corporations()
    logger.info(f"ดึงข้อมูล {len(results)} corporations")
    return results

@router.put("/{corporation_id}", response_model=CorporationOut)
async def update_corporation_endpoint(corporation_id: int, corporation: CorporationUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_corporation(corporation_id, corporation)
    if not result:
        logger.warning(f"ไม่สามารถอัปเดต corporation: id={corporation_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ corporation")
    logger.info(f"อัปเดต corporation: id={result.id}")
    return result

@router.delete("/{corporation_id}")
async def delete_corporation_endpoint(corporation_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_corporation(corporation_id)
    if not result:
        logger.warning(f"ไม่พบ corporation สำหรับลบ: id={corporation_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ corporation")
    logger.info(f"ลบ corporation: id={corporation_id}")
    return {"message": "ลบ corporation เรียบร้อย"}