from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.classify_by_size import (
    create_classify_by_size, get_classify_by_size, get_all_classify_by_sizes,
    update_classify_by_size, delete_classify_by_size
)
from app.schemas.classify_by_size import ClassifyBySizeCreate, ClassifyBySizeUpdate, ClassifyBySizeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/classifybysize", tags=["classifybysize"])

@router.post("/", response_model=ClassifyBySizeOut)
async def create_classify_by_size_endpoint(classify_by_size: ClassifyBySizeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_classify_by_size(classify_by_size)
    if not result:
        logger.warning(f"Failed to create classify_by_size")
        raise HTTPException(status_code=400, detail="Failed to create classify_by_size")
    logger.info(f"Created classify_by_size: id={result.id}")
    return result

@router.get("/{classify_by_size_id}", response_model=ClassifyBySizeOut)
async def get_classify_by_size_endpoint(classify_by_size_id: int, current_user: dict | None = Depends(get_current_user)):
    result = await get_classify_by_size(classify_by_size_id)
    if not result:
        logger.warning(f"Classify_by_size not found: id={classify_by_size_id}")
        raise HTTPException(status_code=404, detail="Classify_by_size not found")
    logger.info(f"Retrieved classify_by_size: id={result.id}")
    return result

@router.get("/", response_model=List[ClassifyBySizeOut])
async def get_all_classify_by_sizes_endpoint(current_user: dict | None = Depends(get_current_user)):
    results = await get_all_classify_by_sizes()
    logger.info(f"Retrieved {len(results)} classify_by_sizes")
    return results

@router.put("/{classify_by_size_id}", response_model=ClassifyBySizeOut)
async def update_classify_by_size_endpoint(classify_by_size_id: int, classify_by_size: ClassifyBySizeUpdate, current_user: dict | None = Depends(get_current_user)):
    result = await update_classify_by_size(classify_by_size_id, classify_by_size)
    if not result:
        logger.warning(f"Classify_by_size not found for update: id={classify_by_size_id}")
        raise HTTPException(status_code=404, detail="Classify_by_size not found")
    logger.info(f"Updated classify_by_size: id={result.id}")
    return result

@router.delete("/{classify_by_size_id}")
async def delete_classify_by_size_endpoint(classify_by_size_id: int, current_user: dict | None = Depends(get_current_user)):
    result = await delete_classify_by_size(classify_by_size_id)
    if not result:
        logger.warning(f"Classify_by_size not found for deletion: id={classify_by_size_id}")
        raise HTTPException(status_code=404, detail="Classify_by_size not found")
    logger.info(f"Deleted classify_by_size: id={classify_by_size_id}")
    return {"message": "Classify_by_size deleted"}