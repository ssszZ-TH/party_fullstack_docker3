from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.classify_by_minority import (
    create_classify_by_minority, get_classify_by_minority, get_all_classify_by_minorities,
    update_classify_by_minority, delete_classify_by_minority, get_classify_by_minorities_by_organization
)
from app.schemas.classify_by_minority import ClassifyByMinorityCreate, ClassifyByMinorityUpdate, ClassifyByMinorityOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/classifybyminority", tags=["classifybyminority"])

@router.post("/", response_model=ClassifyByMinorityOut)
async def create_classify_by_minority_endpoint(classify_by_minority: ClassifyByMinorityCreate, current_user: dict = Depends(get_current_user)):
    result = await create_classify_by_minority(classify_by_minority)
    if not result:
        logger.warning(f"Failed to create classify_by_minority")
        raise HTTPException(status_code=400, detail="Failed to create classify_by_minority")
    logger.info(f"Created classify_by_minority: id={result.id}")
    return result

@router.get("/{classify_by_minority_id}", response_model=ClassifyByMinorityOut)
async def get_classify_by_minority_endpoint(classify_by_minority_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_classify_by_minority(classify_by_minority_id)
    if not result:
        logger.warning(f"Classify_by_minority not found: id={classify_by_minority_id}")
        raise HTTPException(status_code=404, detail="Classify_by_minority not found")
    logger.info(f"Retrieved classify_by_minority: id={result.id}")
    return result

@router.get("/", response_model=List[ClassifyByMinorityOut])
async def get_all_classify_by_minorities_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_classify_by_minorities()
    logger.info(f"Retrieved {len(results)} classify_by_minorities")
    return results

@router.get("/byorganizationid/{organization_id}", response_model=List[ClassifyByMinorityOut])
async def get_classify_by_minorities_by_organization_endpoint(organization_id: int, current_user: dict = Depends(get_current_user)):
    results = await get_classify_by_minorities_by_organization(organization_id)
    logger.info(f"Retrieved {len(results)} classify_by_minorities for organization_id={organization_id}")
    return results

@router.put("/{classify_by_minority_id}", response_model=ClassifyByMinorityOut)
async def update_classify_by_minority_endpoint(classify_by_minority_id: int, classify_by_minority: ClassifyByMinorityUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_classify_by_minority(classify_by_minority_id, classify_by_minority)
    if not result:
        logger.warning(f"Classify_by_minority not found for update: id={classify_by_minority_id}")
        raise HTTPException(status_code=404, detail="Classify_by_minority not found")
    logger.info(f"Updated classify_by_minority: id={result.id}")
    return result

@router.delete("/{classify_by_minority_id}")
async def delete_classify_by_minority_endpoint(classify_by_minority_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_classify_by_minority(classify_by_minority_id)
    if not result:
        logger.warning(f"Classify_by_minority not found for deletion: id={classify_by_minority_id}")
        raise HTTPException(status_code=404, detail="Classify_by_minority not found")
    logger.info(f"Deleted classify_by_minority: id={classify_by_minority_id}")
    return {"message": "Classify_by_minority deleted"}