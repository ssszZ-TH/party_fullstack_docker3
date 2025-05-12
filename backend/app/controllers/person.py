from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.person import (
    create_person, get_person, get_all_persons,
    update_person, delete_person
)
from app.schemas.person import PersonCreate, PersonUpdate, PersonOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/person", tags=["person"])

@router.post("/", response_model=PersonOut)
async def create_person_endpoint(person: PersonCreate, current_user: dict = Depends(get_current_user)):
    result = await create_person(person)
    if not result:
        logger.warning(f"Failed to create person")
        raise HTTPException(status_code=400, detail="Failed to create person")
    logger.info(f"Created person: id={result.id}")
    return result

@router.get("/{person_id}", response_model=PersonOut)
async def get_person_endpoint(person_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_person(person_id)
    if not result:
        logger.warning(f"Person not found: id={person_id}")
        raise HTTPException(status_code=404, detail="Person not found")
    logger.info(f"Retrieved person: id={result.id}")
    return result

@router.get("/", response_model=List[PersonOut])
async def get_all_persons_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_persons()
    logger.info(f"Retrieved {len(results)} persons")
    return results

@router.put("/{person_id}", response_model=PersonOut)
async def update_person_endpoint(person_id: int, person: PersonUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_person(person_id, person)
    if not result:
        logger.warning(f"Person not found for update: id={person_id}")
        raise HTTPException(status_code=404, detail="Person not found")
    logger.info(f"Updated person: id={result.id}")
    return result

@router.delete("/{person_id}")
async def delete_person_endpoint(person_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_person(person_id)
    if not result:
        logger.warning(f"Person not found for deletion or referenced: id={person_id}")
        raise HTTPException(status_code=404, detail="Person not found or referenced in related tables")
    logger.info(f"Deleted person: id={person_id}")
    return {"message": "Person deleted"}