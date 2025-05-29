from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.family import (
    create_family, get_family, get_all_families,
    update_family, delete_family
)
from app.schemas.family import FamilyCreate, FamilyUpdate, FamilyOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/family", tags=["family"])

@router.post("/", response_model=FamilyOut)
async def create_family_endpoint(family: FamilyCreate, current_user: dict = Depends(get_current_user)):
    result = await create_family(family)
    if not result:
        logger.warning(f"ไม่สามารถสร้าง family")
        raise HTTPException(status_code=400, detail="ไม่สามารถสร้าง family")
    logger.info(f"สร้าง family: id={result.id}")
    return result

@router.get("/{family_id}", response_model=FamilyOut)
async def get_family_endpoint(family_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_family(family_id)
    if not result:
        logger.warning(f"ไม่พบ family: id={family_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ family")
    logger.info(f"ดึงข้อมูล family: id={result.id}")
    return result

@router.get("/", response_model=List[FamilyOut])
async def get_all_families_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_families()
    logger.info(f"ดึงข้อมูล {len(results)} families")
    return results

@router.put("/{family_id}", response_model=FamilyOut)
async def update_family_endpoint(family_id: int, family: FamilyUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_family(family_id, family)
    if not result:
        logger.warning(f"ไม่สามารถอัปเดต family: id={family_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ family")
    logger.info(f"อัปเดต family: id={result.id}")
    return result

@router.delete("/{family_id}")
async def delete_family_endpoint(family_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_family(family_id)
    if not result:
        logger.warning(f"ไม่พบ family สำหรับลบ: id={family_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ family")
    logger.info(f"ลบ family: id={family_id}")
    return {"message": "ลบ family เรียบร้อย"}