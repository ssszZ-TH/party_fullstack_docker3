from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.minority_type import (
    create_minority_type, get_minority_type, get_all_minority_types,
    update_minority_type, delete_minority_type
)
from app.schemas.minority_type import MinorityTypeCreate, MinorityTypeUpdate, MinorityTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/minority_type", tags=["minority_type"])

@router.post("/", response_model=MinorityTypeOut)
async def create_minority_type_endpoint(minority_type: MinorityTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_minority_type(minority_type)
    if not result:
        logger.warning(f"Failed to create minority type: name_en={minority_type.name_en}")
        raise HTTPException(status_code=400, detail="Name_en already exists")
    logger.info(f"Created minority type: id={result.id}, name_en={result.name_en}")
    return result

@router.get("/{minority_type_id}", response_model=MinorityTypeOut)
async def get_minority_type_endpoint(minority_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_minority_type(minority_type_id)
    if not result:
        logger.warning(f"Minority type not found: id={minority_type_id}")
        raise HTTPException(status_code=404, detail="Minority type not found")
    logger.info(f"Retrieved minority type: id={result.id}, name_en={result.name_en}")
    return result

@router.get("/", response_model=List[MinorityTypeOut])
async def get_all_minority_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_minority_types()
    logger.info(f"Retrieved {len(results)} minority types")
    return results

@router.put("/{minority_type_id}", response_model=MinorityTypeOut)
async def update_minority_type_endpoint(minority_type_id: int, minority_type: MinorityTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_minority_type(minority_type_id, minority_type)
    if not result:
        logger.warning(f"Failed to update minority type: id={minority_type_id}")
        raise HTTPException(status_code=404, detail="Minority type not found or name_en already exists")
    logger.info(f"Updated minority type: id={result.id}, name_en={result.name_en}")
    return result

@router.delete("/{minority_type_id}")
async def delete_minority_type_endpoint(minority_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_minority_type(minority_type_id)
    if not result:
        logger.warning(f"Minority type not found for deletion: id={minority_type_id}")
        raise HTTPException(status_code=404, detail="Minority type not found")
    logger.info(f"Deleted minority type: id={minority_type_id}")
    return {"message": "Minority type deleted"}