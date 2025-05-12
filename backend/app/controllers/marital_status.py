from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.marital_status import (
    create_marital_status, get_marital_status, get_all_marital_statuses,
    update_marital_status, delete_marital_status
)
from app.schemas.marital_status import MaritalStatusCreate, MaritalStatusUpdate, MaritalStatusOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/maritalstatus", tags=["marital_status"])

@router.post("/", response_model=MaritalStatusOut)
async def create_marital_status_endpoint(marital_status: MaritalStatusCreate, current_user: dict = Depends(get_current_user)):
    result = await create_marital_status(marital_status)
    if not result:
        logger.warning(f"Failed to create marital status: person_id={marital_status.person_id}")
        raise HTTPException(status_code=400, detail="Marital status already exists")
    logger.info(f"Created marital status: id={result.id}, person_id={result.person_id}")
    return result

@router.get("/{marital_status_id}", response_model=MaritalStatusOut)
async def get_marital_status_endpoint(marital_status_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_marital_status(marital_status_id)
    if not result:
        logger.warning(f"Marital status not found: id={marital_status_id}")
        raise HTTPException(status_code=404, detail="Marital status not found")
    logger.info(f"Retrieved marital status: id={result.id}, person_id={result.person_id}")
    return result

@router.get("/", response_model=List[MaritalStatusOut])
async def get_all_marital_statuses_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_marital_statuses()
    logger.info(f"Retrieved {len(results)} marital statuses")
    return results

@router.put("/{marital_status_id}", response_model=MaritalStatusOut)
async def update_marital_status_endpoint(marital_status_id: int, marital_status: MaritalStatusUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_marital_status(marital_status_id, marital_status)
    if not result:
        logger.warning(f"Failed to update marital status: id={marital_status_id}")
        raise HTTPException(status_code=404, detail="Marital status not found or already exists")
    logger.info(f"Updated marital status: id={result.id}, person_id={result.person_id}")
    return result

@router.delete("/{marital_status_id}")
async def delete_marital_status_endpoint(marital_status_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_marital_status(marital_status_id)
    if not result:
        logger.warning(f"Marital status not found for deletion: id={marital_status_id}")
        raise HTTPException(status_code=404, detail="Marital status not found")
    logger.info(f"Deleted marital status: id={marital_status_id}")
    return {"message": "Marital status deleted"}