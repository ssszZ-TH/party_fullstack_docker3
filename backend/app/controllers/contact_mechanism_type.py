from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.contact_mechanism_type import (
    create_contact_mechanism_type, get_contact_mechanism_type, get_all_contact_mechanism_types,
    update_contact_mechanism_type, delete_contact_mechanism_type
)
from app.schemas.contact_mechanism_type import ContactMechanismTypeCreate, ContactMechanismTypeUpdate, ContactMechanismTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/contactmechanismtype", tags=["contactmechanismtype"])

@router.post("/", response_model=ContactMechanismTypeOut)
async def create_contact_mechanism_type_endpoint(contact_mechanism_type: ContactMechanismTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_contact_mechanism_type(contact_mechanism_type)
    if not result:
        logger.warning(f"Failed to create contact_mechanism_type")
        raise HTTPException(status_code=400, detail="Failed to create contact_mechanism_type")
    logger.info(f"Created contact_mechanism_type: id={result.id}")
    return result

@router.get("/{contact_mechanism_type_id}", response_model=ContactMechanismTypeOut)
async def get_contact_mechanism_type_endpoint(contact_mechanism_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_contact_mechanism_type(contact_mechanism_type_id)
    if not result:
        logger.warning(f"Contact_mechanism_type not found: id={contact_mechanism_type_id}")
        raise HTTPException(status_code=404, detail="Contact_mechanism_type not found")
    logger.info(f"Retrieved contact_mechanism_type: id={result.id}")
    return result

@router.get("/", response_model=List[ContactMechanismTypeOut])
async def get_all_contact_mechanism_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_contact_mechanism_types()
    logger.info(f"Retrieved {len(results)} contact_mechanism_types")
    return results

@router.put("/{contact_mechanism_type_id}", response_model=ContactMechanismTypeOut)
async def update_contact_mechanism_type_endpoint(contact_mechanism_type_id: int, contact_mechanism_type: ContactMechanismTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_contact_mechanism_type(contact_mechanism_type_id, contact_mechanism_type)
    if not result:
        logger.warning(f"Contact_mechanism_type not found for update: id={contact_mechanism_type_id}")
        raise HTTPException(status_code=404, detail="Contact_mechanism_type not found")
    logger.info(f"Updated contact_mechanism_type: id={result.id}")
    return result

@router.delete("/{contact_mechanism_type_id}")
async def delete_contact_mechanism_type_endpoint(contact_mechanism_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_contact_mechanism_type(contact_mechanism_type_id)
    if not result:
        logger.warning(f"Contact_mechanism_type not found for deletion: id={contact_mechanism_type_id}")
        raise HTTPException(status_code=404, detail="Contact_mechanism_type not found")
    logger.info(f"Deleted contact_mechanism_type: id={contact_mechanism_type_id}")
    return {"message": "Contact_mechanism_type deleted"}