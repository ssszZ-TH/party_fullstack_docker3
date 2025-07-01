from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.priority_type import (
    create_priority_type, get_priority_type, get_all_priority_types,
    update_priority_type, delete_priority_type
)
from app.schemas.priority_type import PriorityTypeCreate, PriorityTypeUpdate, PriorityTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/prioritytype", tags=["prioritytype"])

@router.post("/", response_model=PriorityTypeOut)
async def create_priority_type_endpoint(priority_type: PriorityTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_priority_type(priority_type)
    if not result:
        logger.warning(f"Failed to create priority_type")
        raise HTTPException(status_code=400, detail="Failed to create priority_type")
    logger.info(f"Created priority_type: id={result.id}")
    return result

@router.get("/{priority_type_id}", response_model=PriorityTypeOut)
async def get_priority_type_endpoint(priority_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_priority_type(priority_type_id)
    if not result:
        logger.warning(f"Priority_type not found: id={priority_type_id}")
        raise HTTPException(status_code=404, detail="Priority_type not found")
    logger.info(f"Retrieved priority_type: id={result.id}")
    return result

@router.get("/", response_model=List[PriorityTypeOut])
async def get_all_priority_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_priority_types()
    logger.info(f"Retrieved {len(results)} priority_types")
    return results

@router.put("/{priority_type_id}", response_model=PriorityTypeOut)
async def update_priority_type_endpoint(priority_type_id: int, priority_type: PriorityTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_priority_type(priority_type_id, priority_type)
    if not result:
        logger.warning(f"Priority_type not found for update: id={priority_type_id}")
        raise HTTPException(status_code=404, detail="Priority_type not found")
    logger.info(f"Updated priority_type: id={result.id}")
    return result

@router.delete("/{priority_type_id}")
async def delete_priority_type_endpoint(priority_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_priority_type(priority_type_id)
    if not result:
        logger.warning(f"Priority_type not found for deletion: id={priority_type_id}")
        raise HTTPException(status_code=404, detail="Priority_type not found")
    logger.info(f"Deleted priority_type: id={priority_type_id}")
    return {"message": "Priority_type deleted"}