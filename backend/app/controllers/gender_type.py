from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.gender_type import (
    create_gender_type, get_gender_type, get_all_gender_types,
    update_gender_type, delete_gender_type
)
from app.schemas.gender_type import GenderTypeCreate, GenderTypeUpdate, GenderTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/gendertype", tags=["gendertype"])

@router.post("/", response_model=GenderTypeOut)
async def create_gender_type_endpoint(gender_type: GenderTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_gender_type(gender_type)
    if not result:
        logger.warning(f"ไม่สามารถสร้างประเภทเพศ: description={gender_type.description}")
        raise HTTPException(status_code=400, detail="คำอธิบายนี้มีอยู่แล้ว")
    logger.info(f"สร้างประเภทเพศ: id={result.id}, description={result.description}")
    return result

@router.get("/{gender_type_id}", response_model=GenderTypeOut)
async def get_gender_type_endpoint(gender_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_gender_type(gender_type_id)
    if not result:
        logger.warning(f"ไม่พบประเภทเพศ: id={gender_type_id}")
        raise HTTPException(status_code=404, detail="ไม่พบประเภทเพศ")
    logger.info(f"ดึงข้อมูลประเภทเพศ: id={result.id}, description={result.description}")
    return result

@router.get("/", response_model=List[GenderTypeOut])
async def get_all_gender_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_gender_types()
    logger.info(f"ดึงข้อมูล {len(results)} ประเภทเพศ")
    return results

@router.put("/{gender_type_id}", response_model=GenderTypeOut)
async def update_gender_type_endpoint(gender_type_id: int, gender_type: GenderTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_gender_type(gender_type_id, gender_type)
    if not result:
        logger.warning(f"ไม่สามารถอัปเดตประเภทเพศ: id={gender_type_id}")
        raise HTTPException(status_code=404, detail="ไม่พบประเภทเพศหรือคำอธิบายนี้มีอยู่แล้ว")
    logger.info(f"อัปเดตประเภทเพศ: id={result.id}, description={result.description}")
    return result

@router.delete("/{gender_type_id}")
async def delete_gender_type_endpoint(gender_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_gender_type(gender_type_id)
    if not result:
        logger.warning(f"ไม่พบประเภทเพศสำหรับลบ: id={gender_type_id}")
        raise HTTPException(status_code=404, detail="ไม่พบประเภทเพศหรือถูกอ้างอิงในตารางอื่น")
    logger.info(f"ลบประเภทเพศ: id={gender_type_id}")
    return {"message": "ลบประเภทเพศเรียบร้อย"}