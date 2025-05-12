from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.citizenship import (
    create_citizenship, get_citizenship, get_all_citizenships,
    update_citizenship, delete_citizenship
)
from app.schemas.citizenship import CitizenshipCreate, CitizenshipUpdate, CitizenshipOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/citizenship", tags=["citizenship"])

@router.post("/", response_model=CitizenshipOut)
async def create_citizenship_endpoint(citizenship: CitizenshipCreate, current_user: dict = Depends(get_current_user)):
    result = await create_citizenship(citizenship)
    if not result:
        logger.warning(f"Failed to create citizenship: person_id={citizenship.person_id}, country_id={citizenship.country_id}")
        raise HTTPException(status_code=400, detail="Citizenship already exists")
    logger.info(f"Created citizenship: id={result.id}, person_id={result.person_id}")
    return result

@router.get("/{citizenship_id}", response_model=CitizenshipOut)
async def get_citizenship_endpoint(citizenship_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_citizenship(citizenship_id)
    if not result:
        logger.warning(f"Citizenship not found: id={citizenship_id}")
        raise HTTPException(status_code=404, detail="Citizenship not found")
    logger.info(f"Retrieved citizenship: id={result.id}, person_id={result.person_id}")
    return result

@router.get("/", response_model=List[CitizenshipOut])
async def get_all_citizenships_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_citizenships()
    logger.info(f"Retrieved {len(results)} citizenships")
    return results

@router.put("/{citizenship_id}", response_model=CitizenshipOut)
async def update_citizenship_endpoint(citizenship_id: int, citizenship: CitizenshipUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_citizenship(citizenship_id, citizenship)
    if not result:
        logger.warning(f"Failed to update citizenship: id={citizenship_id}")
        raise HTTPException(status_code=404, detail="Citizenship not found or already exists")
    logger.info(f"Updated citizenship: id={result.id}, person_id={result.person_id}")
    return result

@router.delete("/{citizenship_id}")
async def delete_citizenship_endpoint(citizenship_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_citizenship(citizenship_id)
    if not result:
        logger.warning(f"Citizenship not found for deletion or referenced: id={citizenship_id}")
        raise HTTPException(status_code=404, detail="Citizenship not found or referenced in passport")
    logger.info(f"Deleted citizenship: id={citizenship_id}")
    return {"message": "Citizenship deleted"}