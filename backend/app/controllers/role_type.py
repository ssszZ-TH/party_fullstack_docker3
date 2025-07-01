from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.role_type import (
    create_role_type, get_role_type, get_all_role_types,
    update_role_type, delete_role_type
)
from app.schemas.role_type import RoleTypeCreate, RoleTypeUpdate, RoleTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/roletypes", tags=["roletypes"])

@router.post("/", response_model=RoleTypeOut)
async def create_role_type_endpoint(role_type: RoleTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_role_type(role_type)
    if not result:
        logger.warning(f"Failed to create role_type")
        raise HTTPException(status_code=400, detail="Failed to create role_type")
    logger.info(f"Created role_type: id={result.id}")
    return result

@router.get("/{role_type_id}", response_model=RoleTypeOut)
async def get_role_type_endpoint(role_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_role_type(role_type_id)
    if not result:
        logger.warning(f"Role_type not found: id={role_type_id}")
        raise HTTPException(status_code=404, detail="Role_type not found")
    logger.info(f"Retrieved role_type: id={result.id}")
    return result

@router.get("/", response_model=List[RoleTypeOut])
async def get_all_role_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_role_types()
    logger.info(f"Retrieved {len(results)} role_types")
    return results

@router.put("/{role_type_id}", response_model=RoleTypeOut)
async def update_role_type_endpoint(role_type_id: int, role_type: RoleTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_role_type(role_type_id, role_type)
    if not result:
        logger.warning(f"Role_type not found for update: id={role_type_id}")
        raise HTTPException(status_code=404, detail="Role_type not found")
    logger.info(f"Updated role_type: id={result.id}")
    return result

@router.delete("/{role_type_id}")
async def delete_role_type_endpoint(role_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_role_type(role_type_id)
    if not result:
        logger.warning(f"Role_type not found for deletion: id={role_type_id}")
        raise HTTPException(status_code=404, detail="Role_type not found")
    logger.info(f"Deleted role_type: id={role_type_id}")
    return {"message": "Role_type deleted"}