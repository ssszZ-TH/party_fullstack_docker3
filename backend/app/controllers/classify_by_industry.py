from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.classify_by_industry import (
    create_classify_by_industry, get_classify_by_industry, get_all_classify_by_industries,
    update_classify_by_industry, delete_classify_by_industry, get_classify_by_industries_by_organization
)
from app.schemas.classify_by_industry import ClassifyByIndustryCreate, ClassifyByIndustryUpdate, ClassifyByIndustryOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/classifybyindustry", tags=["classifybyindustry"])

@router.post("/", response_model=ClassifyByIndustryOut)
async def create_classify_by_industry_endpoint(classify_by_industry: ClassifyByIndustryCreate, current_user: dict = Depends(get_current_user)):
    result = await create_classify_by_industry(classify_by_industry)
    if not result:
        logger.warning(f"Failed to create classify_by_industry")
        raise HTTPException(status_code=400, detail="Failed to create classify_by_industry")
    logger.info(f"Created classify_by_industry: id={result.id}")
    return result

@router.get("/{classify_by_industry_id}", response_model=ClassifyByIndustryOut)
async def get_classify_by_industry_endpoint(classify_by_industry_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_classify_by_industry(classify_by_industry_id)
    if not result:
        logger.warning(f"Classify_by_industry not found: id={classify_by_industry_id}")
        raise HTTPException(status_code=404, detail="Classify_by_industry not found")
    logger.info(f"Retrieved classify_by_industry: id={result.id}")
    return result

@router.get("/", response_model=List[ClassifyByIndustryOut])
async def get_all_classify_by_industries_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_classify_by_industries()
    logger.info(f"Retrieved {len(results)} classify_by_industries")
    return results

@router.get("/byorganizationid/{organization_id}", response_model=List[ClassifyByIndustryOut])
async def get_classify_by_industries_by_organization_endpoint(organization_id: int, current_user: dict = Depends(get_current_user)):
    results = await get_classify_by_industries_by_organization(organization_id)
    logger.info(f"Retrieved {len(results)} classify_by_industries for organization_id={organization_id}")
    return results

@router.put("/{classify_by_industry_id}", response_model=ClassifyByIndustryOut)
async def update_classify_by_industry_endpoint(classify_by_industry_id: int, classify_by_industry: ClassifyByIndustryUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_classify_by_industry(classify_by_industry_id, classify_by_industry)
    if not result:
        logger.warning(f"Classify_by_industry not found for update: id={classify_by_industry_id}")
        raise HTTPException(status_code=404, detail="Classify_by_industry not found")
    logger.info(f"Updated classify_by_industry: id={result.id}")
    return result

@router.delete("/{classify_by_industry_id}")
async def delete_classify_by_industry_endpoint(classify_by_industry_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_classify_by_industry(classify_by_industry_id)
    if not result:
        logger.warning(f"Classify_by_industry not found for deletion: id={classify_by_industry_id}")
        raise HTTPException(status_code=404, detail="Classify_by_industry not found")
    logger.info(f"Deleted classify_by_industry: id={classify_by_industry_id}")
    return {"message": "Classify_by_industry deleted"}