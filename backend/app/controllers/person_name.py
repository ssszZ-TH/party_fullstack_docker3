from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.person_name import (
    create_person_name, get_person_name, get_all_person_names,
    update_person_name, delete_person_name
)
from app.schemas.person_name import PersonNameCreate, PersonNameUpdate, PersonNameOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/personname", tags=["person_name"])

@router.post("/", response_model=PersonNameOut)
async def create_person_name_endpoint(person_name: PersonNameCreate, current_user: dict = Depends(get_current_user)):
    result = await create_person_name(person_name)
    if not result:
        logger.warning(f"Failed to create person name: name={person_name.name}")
        raise HTTPException(status_code=400, detail="Person name already exists")
    logger.info(f"Created person name: id={result.id}, name={result.name}")
    return result

@router.get("/{person_name_id}", response_model=PersonNameOut)
async def get_person_name_endpoint(person_name_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_person_name(person_name_id)
    if not result:
        logger.warning(f"Person name not found: id={person_name_id}")
        raise HTTPException(status_code=404, detail="Person name not found")
    logger.info(f"Retrieved person name: id={result.id}, name={result.name}")
    return result

@router.get("/", response_model=List[PersonNameOut])
async def get_all_person_names_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_person_names()
    logger.info(f"Retrieved {len(results)} person names")
    return results

@router.put("/{person_name_id}", response_model=PersonNameOut)
async def update_person_name_endpoint(person_name_id: int, person_name: PersonNameUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_person_name(person_name_id, person_name)
    if not result:
        logger.warning(f"Failed to update person name: id={person_name_id}")
        raise HTTPException(status_code=404, detail="Person name not found or already exists")
    logger.info(f"Updated person name: id={result.id}, name={result.name}")
    return result

@router.delete("/{person_name_id}")
async def delete_person_name_endpoint(person_name_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_person_name(person_name_id)
    if not result:
        logger.warning(f"Person name not found for deletion: id={person_name_id}")
        raise HTTPException(status_code=404, detail="Person name not found")
    logger.info(f"Deleted person name: id={person_name_id}")
    return {"message": "Person name deleted"}