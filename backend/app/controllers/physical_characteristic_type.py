from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.physical_characteristic_type import (
    create_physical_characteristic_type, get_physical_characteristic_type, get_all_physical_characteristic_types,
    update_physical_characteristic_type, delete_physical_characteristic_type
)
from app.schemas.physical_characteristic_type import PhysicalCharacteristicTypeCreate, PhysicalCharacteristicTypeUpdate, PhysicalCharacteristicTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/physicalcharacteristictype", tags=["physical_characteristic_type"])

@router.post("/", response_model=PhysicalCharacteristicTypeOut)
async def create_physical_characteristic_type_endpoint(physical_characteristic_type: PhysicalCharacteristicTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_physical_characteristic_type(physical_characteristic_type)
    if not result:
        logger.warning(f"Failed to create physical characteristic type: description={physical_characteristic_type.description}")
        raise HTTPException(status_code=400, detail="Description already exists")
    logger.info(f"Created physical characteristic type: id={result.id}, description={result.description}")
    return result

@router.get("/{physical_characteristic_type_id}", response_model=PhysicalCharacteristicTypeOut)
async def get_physical_characteristic_type_endpoint(physical_characteristic_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_physical_characteristic_type(physical_characteristic_type_id)
    if not result:
        logger.warning(f"Physical characteristic type not found: id={physical_characteristic_type_id}")
        raise HTTPException(status_code=404, detail="Physical characteristic type not found")
    logger.info(f"Retrieved physical characteristic type: id={result.id}, description={result.description}")
    return result

@router.get("/", response_model=List[PhysicalCharacteristicTypeOut])
async def get_all_physical_characteristic_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_physical_characteristic_types()
    logger.info(f"Retrieved {len(results)} physical characteristic types")
    return results

@router.put("/{physical_characteristic_type_id}", response_model=PhysicalCharacteristicTypeOut)
async def update_physical_characteristic_type_endpoint(physical_characteristic_type_id: int, physical_characteristic_type: PhysicalCharacteristicTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_physical_characteristic_type(physical_characteristic_type_id, physical_characteristic_type)
    if not result:
        logger.warning(f"Failed to update physical characteristic type: id={physical_characteristic_type_id}")
        raise HTTPException(status_code=404, detail="Physical characteristic type not found or description already exists")
    logger.info(f"Updated physical characteristic type: id={result.id}, description={result.description}")
    return result

@router.delete("/{physical_characteristic_type_id}")
async def delete_physical_characteristic_type_endpoint(physical_characteristic_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_physical_characteristic_type(physical_characteristic_type_id)
    if not result:
        logger.warning(f"Physical characteristic type not found for deletion: id={physical_characteristic_type_id}")
        raise HTTPException(status_code=404, detail="Physical characteristic type not found")
    logger.info(f"Deleted physical characteristic type: id={physical_characteristic_type_id}")
    return {"message": "Physical characteristic type deleted"}