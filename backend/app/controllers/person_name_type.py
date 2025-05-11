from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.person_name_type import (
    create_person_name_type, get_person_name_type, get_all_person_name_types,
    update_person_name_type, delete_person_name_type
)
from app.schemas.person_name_type import PersonNameTypeCreate, PersonNameTypeUpdate, PersonNameTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/personnametype", tags=["person_name_type"])

@router.post("/", response_model=PersonNameTypeOut)
async def create_person_name_type_endpoint(person_name_type: PersonNameTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_person_name_type(person_name_type)
    if not result:
        logger.warning(f"Failed to create person name type: description={person_name_type.description}")
        raise HTTPException(status_code=400, detail="Description already exists")
    logger.info(f"Created person name type: id={result.id}, description={result.description}")
    return result

@router.get("/{person_name_type_id}", response_model=PersonNameTypeOut)
async def get_person_name_type_endpoint(person_name_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_person_name_type(person_name_type_id)
    if not result:
        logger.warning(f"Person name type not found: id={person_name_type_id}")
        raise HTTPException(status_code=404, detail="Person name type not found")
    logger.info(f"Retrieved person name type: id={result.id}, description={result.description}")
    return result

@router.get("/", response_model=List[PersonNameTypeOut])
async def get_all_person_name_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_person_name_types()
    logger.info(f"Retrieved {len(results)} person name types")
    return results

@router.put("/{person_name_type_id}", response_model=PersonNameTypeOut)
async def update_person_name_type_endpoint(person_name_type_id: int, person_name_type: PersonNameTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_person_name_type(person_name_type_id, person_name_type)
    if not result:
        logger.warning(f"Failed to update person name type: id={person_name_type_id}")
        raise HTTPException(status_code=404, detail="Person name type not found or description already exists")
    logger.info(f"Updated person name type: id={result.id}, description={result.description}")
    return result

@router.delete("/{person_name_type_id}")
async def delete_person_name_type_endpoint(person_name_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_person_name_type(person_name_type_id)
    if not result:
        logger.warning(f"Person name type not found for deletion: id={person_name_type_id}")
        raise HTTPException(status_code=404, detail="Person name type not found")
    logger.info(f"Deleted person name type: id={person_name_type_id}")
    return {"message": "Person name type deleted"}