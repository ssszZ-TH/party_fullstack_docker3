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
    try:
        result = await create_person(person)
        if not result:
            logger.warning(f"Failed to create person for user: {current_user.get('username')}")
            raise HTTPException(status_code=400, detail="Failed to create person")
        logger.info(f"Created person: id={result.id} by user: {current_user.get('username')}")
        return result
    except Exception as e:
        logger.error(f"Error creating person: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{person_id}", response_model=PersonOut)
async def get_person_endpoint(person_id: int, current_user: dict = Depends(get_current_user)):
    try:
        result = await get_person(person_id)
        if not result:
            logger.warning(f"Person not found: id={person_id} by user: {current_user.get('username')}")
            raise HTTPException(status_code=404, detail="Person not found")
        logger.info(f"Retrieved person: id={result.id} by user: {current_user.get('username')}")
        return result
    except Exception as e:
        logger.error(f"Error retrieving person id={person_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[PersonOut])
async def get_all_persons_endpoint(current_user: dict = Depends(get_current_user)):
    try:
        results = await get_all_persons()
        logger.info(f"Retrieved {len(results)} persons by user: {current_user.get('username')}")
        return results
    except Exception as e:
        logger.error(f"Error retrieving all persons: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{person_id}", response_model=PersonOut)
async def update_person_endpoint(person_id: int, person: PersonUpdate, current_user: dict = Depends(get_current_user)):
    try:
        result = await update_person(person_id, person)
        if not result:
            logger.warning(f"Person not found for update: id={person_id} by user: {current_user.get('username')}")
            raise HTTPException(status_code=404, detail="Person not found")
        logger.info(f"Updated person: id={result.id} by user: {current_user.get('username')}")
        return result
    except Exception as e:
        logger.error(f"Error updating person id={person_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{person_id}", response_model=dict)
async def delete_person_endpoint(person_id: int, current_user: dict = Depends(get_current_user)):
    try:
        result = await delete_person(person_id)
        if not result:
            logger.warning(f"Person not found or referenced for deletion: id={person_id} by user: {current_user.get('username')}")
            raise HTTPException(status_code=400, detail="Person not found or referenced in related tables")
        logger.info(f"Deleted person: id={person_id} by user: {current_user.get('username')}")
        return {"message": "Person deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting person id={person_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")