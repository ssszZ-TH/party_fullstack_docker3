from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.marital_status_type import (
    create_marital_status_type, get_marital_status_type, get_all_marital_status_types,
    update_marital_status_type, delete_marital_status_type
)
from app.schemas.marital_status_type import MaritalStatusTypeCreate, MaritalStatusTypeUpdate, MaritalStatusTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/maritalstatustype", tags=["maritalstatustype"])

@router.post("/", response_model=MaritalStatusTypeOut)
async def create_marital_status_type_endpoint(marital_status_type: MaritalStatusTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_marital_status_type(marital_status_type)
    if not result:
        logger.warning(f"Failed to create marital status type: description={marital_status_type.description}")
        raise HTTPException(status_code=400, detail="Description already exists")
    logger.info(f"Created marital status type: id={result.id}, description={result.description}")
    return result

@router.get("/{marital_status_type_id}", response_model=MaritalStatusTypeOut)
async def get_marital_status_type_endpoint(marital_status_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_marital_status_type(marital_status_type_id)
    if not result:
        logger.warning(f"Marital status type not found: id={marital_status_type_id}")
        raise HTTPException(status_code=404, detail="Marital status type not found")
    logger.info(f"Retrieved marital status type: id={result.id}, description={result.description}")
    return result

@router.get("/", response_model=List[MaritalStatusTypeOut])
async def get_all_marital_status_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_marital_status_types()
    logger.info(f"Retrieved {len(results)} marital status types")
    return results

@router.put("/{marital_status_type_id}", response_model=MaritalStatusTypeOut)
async def update_marital_status_type_endpoint(marital_status_type_id: int, marital_status_type: MaritalStatusTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_marital_status_type(marital_status_type_id, marital_status_type)
    if not result:
        logger.warning(f"Failed to update marital status type: id={marital_status_type_id}")
        raise HTTPException(status_code=404, detail="Marital status type not found or description already exists")
    logger.info(f"Updated marital status type: id={result.id}, description={result.description}")
    return result

@router.delete("/{marital_status_type_id}")
async def delete_marital_status_type_endpoint(marital_status_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_marital_status_type(marital_status_type_id)
    if not result:
        logger.warning(f"Marital status type not found for deletion: id={marital_status_type_id}")
        raise HTTPException(status_code=404, detail="Marital status type not found")
    logger.info(f"Deleted marital status type: id={marital_status_type_id}")
    return {"message": "Marital status type deleted"}