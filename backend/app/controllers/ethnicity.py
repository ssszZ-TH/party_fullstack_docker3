from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.ethnicity import (
    create_ethnicity, get_ethnicity, get_all_ethnicities,
    update_ethnicity, delete_ethnicity
)
from app.schemas.ethnicity import EthnicityCreate, EthnicityUpdate, EthnicityOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/ethnicity", tags=["ethnicity"])

@router.post("/", response_model=EthnicityOut)
async def create_ethnicity_endpoint(ethnicity: EthnicityCreate, current_user: dict = Depends(get_current_user)):
    result = await create_ethnicity(ethnicity)
    if not result:
        logger.warning(f"Failed to create ethnicity: name_en={ethnicity.name_en}")
        raise HTTPException(status_code=400, detail="Name_en already exists")
    logger.info(f"Created ethnicity: id={result.id}, name_en={result.name_en}")
    return result

@router.get("/{ethnicity_id}", response_model=EthnicityOut)
async def get_ethnicity_endpoint(ethnicity_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_ethnicity(ethnicity_id)
    if not result:
        logger.warning(f"Ethnicity not found: id={ethnicity_id}")
        raise HTTPException(status_code=404, detail="Ethnicity not found")
    logger.info(f"Retrieved ethnicity: id={result.id}, name_en={result.name_en}")
    return result

@router.get("/", response_model=List[EthnicityOut])
async def get_all_ethnicities_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_ethnicities()
    logger.info(f"Retrieved {len(results)} ethnicities")
    return results

@router.put("/{ethnicity_id}", response_model=EthnicityOut)
async def update_ethnicity_endpoint(ethnicity_id: int, ethnicity: EthnicityUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_ethnicity(ethnicity_id, ethnicity)
    if not result:
        logger.warning(f"Failed to update ethnicity: id={ethnicity_id}")
        raise HTTPException(status_code=404, detail="Ethnicity not found or name_en already exists")
    logger.info(f"Updated ethnicity: id={result.id}, name_en={result.name_en}")
    return result

@router.delete("/{ethnicity_id}")
async def delete_ethnicity_endpoint(ethnicity_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_ethnicity(ethnicity_id)
    if not result:
        logger.warning(f"Ethnicity not found for deletion: id={ethnicity_id}")
        raise HTTPException(status_code=404, detail="Ethnicity not found")
    logger.info(f"Deleted ethnicity: id={ethnicity_id}")
    return {"message": "Ethnicity deleted"}