from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.industry_type import (
    create_industry_type, get_industry_type, get_all_industry_types,
    update_industry_type, delete_industry_type
)
from app.schemas.industry_type import IndustryTypeCreate, IndustryTypeUpdate, IndustryTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/industrytype", tags=["industry_type"])

@router.post("/", response_model=IndustryTypeOut)
async def create_industry_type_endpoint(industry_type: IndustryTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_industry_type(industry_type)
    if not result:
        logger.warning(f"Failed to create industry type: naics_code={industry_type.naics_code}")
        raise HTTPException(status_code=400, detail="NAICS code already exists")
    logger.info(f"Created industry type: id={result.id}, naics_code={result.naics_code}")
    return result

@router.get("/{industry_type_id}", response_model=IndustryTypeOut)
async def get_industry_type_endpoint(industry_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_industry_type(industry_type_id)
    if not result:
        logger.warning(f"Industry type not found: id={industry_type_id}")
        raise HTTPException(status_code=404, detail="Industry type not found")
    logger.info(f"Retrieved industry type: id={result.id}, naics_code={result.naics_code}")
    return result

@router.get("/", response_model=List[IndustryTypeOut])
async def get_all_industry_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_industry_types()
    logger.info(f"Retrieved {len(results)} industry types")
    return results

@router.put("/{industry_type_id}", response_model=IndustryTypeOut)
async def update_industry_type_endpoint(industry_type_id: int, industry_type: IndustryTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_industry_type(industry_type_id, industry_type)
    if not result:
        logger.warning(f"Failed to update industry type: id={industry_type_id}")
        raise HTTPException(status_code=404, detail="Industry type not found or NAICS code already exists")
    logger.info(f"Updated industry type: id={result.id}, naics_code={result.naics_code}")
    return result

@router.delete("/{industry_type_id}")
async def delete_industry_type_endpoint(industry_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_industry_type(industry_type_id)
    if not result:
        logger.warning(f"Industry type not found for deletion: id={industry_type_id}")
        raise HTTPException(status_code=404, detail="Industry type not found")
    logger.info(f"Deleted industry type: id={industry_type_id}")
    return {"message": "Industry type deleted"}