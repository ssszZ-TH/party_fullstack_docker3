from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.physical_characteristic import (
    create_physical_characteristic, get_physical_characteristic, get_all_physical_characteristics,
    update_physical_characteristic, delete_physical_characteristic
)
from app.schemas.physical_characteristic import PhysicalCharacteristicCreate, PhysicalCharacteristicUpdate, PhysicalCharacteristicOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/physicalcharacteristic", tags=["physical_characteristic"])

@router.post("/", response_model=PhysicalCharacteristicOut)
async def create_physical_characteristic_endpoint(physical_characteristic: PhysicalCharacteristicCreate, current_user: dict = Depends(get_current_user)):
    result = await create_physical_characteristic(physical_characteristic)
    if not result:
        logger.warning(f"Failed to create physical characteristic: person_id={physical_characteristic.person_id}")
        raise HTTPException(status_code=400, detail="Physical characteristic already exists")
    logger.info(f"Created physical characteristic: id={result.id}, person_id={result.person_id}")
    return result

@router.get("/{physical_characteristic_id}", response_model=PhysicalCharacteristicOut)
async def get_physical_characteristic_endpoint(physical_characteristic_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_physical_characteristic(physical_characteristic_id)
    if not result:
        logger.warning(f"Physical characteristic not found: id={physical_characteristic_id}")
        raise HTTPException(status_code=404, detail="Physical characteristic not found")
    logger.info(f"Retrieved physical characteristic: id={result.id}, person_id={result.person_id}")
    return result

@router.get("/", response_model=List[PhysicalCharacteristicOut])
async def get_all_physical_characteristics_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_physical_characteristics()
    logger.info(f"Retrieved {len(results)} physical characteristics")
    return results

@router.put("/{physical_characteristic_id}", response_model=PhysicalCharacteristicOut)
async def update_physical_characteristic_endpoint(physical_characteristic_id: int, physical_characteristic: PhysicalCharacteristicUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_physical_characteristic(physical_characteristic_id, physical_characteristic)
    if not result:
        logger.warning(f"Failed to update physical characteristic: id={physical_characteristic_id}")
        raise HTTPException(status_code=404, detail="Physical characteristic not found or already exists")
    logger.info(f"Updated physical characteristic: id={result.id}, person_id={result.person_id}")
    return result

@router.delete("/{physical_characteristic_id}")
async def delete_physical_characteristic_endpoint(physical_characteristic_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_physical_characteristic(physical_characteristic_id)
    if not result:
        logger.warning(f"Physical characteristic not found for deletion: id={physical_characteristic_id}")
        raise HTTPException(status_code=404, detail="Physical characteristic not found")
    logger.info(f"Deleted physical characteristic: id={physical_characteristic_id}")
    return {"message": "Physical characteristic deleted"}