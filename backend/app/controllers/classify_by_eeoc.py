from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.classify_by_eeoc import (
    create_classify_by_eeoc, get_classify_by_eeoc, get_all_classify_by_eeocs,
    update_classify_by_eeoc, delete_classify_by_eeoc, get_classify_by_eeoc_by_person_id
)
from app.schemas.classify_by_eeoc import ClassifyByEeocCreate, ClassifyByEeocUpdate, ClassifyByEeocOut, ClassifyByEeocByPersonIdOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/classifybyeeoc", tags=["classifybyeeoc"])
@router.post("/", response_model=ClassifyByEeocOut)
async def create_classify_by_eeoc_endpoint(classify_by_eeoc: ClassifyByEeocCreate, current_user: dict = Depends(get_current_user)):
    result = await create_classify_by_eeoc(classify_by_eeoc)
    if not result:
        logger.warning(f"Failed to create classify_by_eeoc")
        raise HTTPException(status_code=400, detail="Failed to create classify_by_eeoc")
    logger.info(f"Created classify_by_eeoc: id={result.id}")
    return result

@router.get("/{classify_by_eeoc_id}", response_model=ClassifyByEeocOut)
async def get_classify_by_eeoc_endpoint(classify_by_eeoc_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_classify_by_eeoc(classify_by_eeoc_id)
    if not result:
        logger.warning(f"Classify_by_eeoc not found: id={classify_by_eeoc_id}")
        raise HTTPException(status_code=404, detail="Classify_by_eeoc not found")
    logger.info(f"Retrieved classify_by_eeoc: id={result.id}")
    return result

@router.get("/", response_model=List[ClassifyByEeocOut])
async def get_all_classify_by_eeocs_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_classify_by_eeocs()
    logger.info(f"Retrieved {len(results)} classify_by_eeocs")
    return results

@router.get("/bypersonid/{person_id}", response_model=List[ClassifyByEeocByPersonIdOut])
async def get_classify_by_eeoc_by_person_id_endpoint(person_id: int, current_user: dict = Depends(get_current_user)):
    results = await get_classify_by_eeoc_by_person_id(person_id)
    if not results:
        logger.warning(f"No classify_by_eeoc found for person_id: {person_id}")
        return []
    logger.info(f"Retrieved {len(results)} classify_by_eeoc by person_id: {person_id}")
    return results

@router.put("/{classify_by_eeoc_id}", response_model=ClassifyByEeocOut)
async def update_classify_by_eeoc_endpoint(classify_by_eeoc_id: int, classify_by_eeoc: ClassifyByEeocUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_classify_by_eeoc(classify_by_eeoc_id, classify_by_eeoc)
    if not result:
        logger.warning(f"Classify_by_eeoc not found for update: id={classify_by_eeoc_id}")
        raise HTTPException(status_code=404, detail="Classify_by_eeoc not found")
    logger.info(f"Updated classify_by_eeoc: id={result.id}")
    return result

@router.delete("/{classify_by_eeoc_id}")
async def delete_classify_by_eeoc_endpoint(classify_by_eeoc_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_classify_by_eeoc(classify_by_eeoc_id)
    if not result:
        logger.warning(f"Classify_by_eeoc not found for deletion: id={classify_by_eeoc_id}")
        raise HTTPException(status_code=404, detail="Classify_by_eeoc not found")
    logger.info(f"Deleted classify_by_eeoc: id={classify_by_eeoc_id}")
    return {"message": "Classify_by_eeoc deleted"}