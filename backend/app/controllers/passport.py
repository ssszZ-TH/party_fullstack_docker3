from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.passport import (
    create_passport, get_passport, get_all_passports,
    update_passport, delete_passport
)
from app.schemas.passport import PassportCreate, PassportUpdate, PassportOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/passport", tags=["passport"])

@router.post("/", response_model=PassportOut)
async def create_passport_endpoint(passport: PassportCreate, current_user: dict = Depends(get_current_user)):
    result = await create_passport(passport)
    if not result:
        logger.warning(f"Failed to create passport: passportnumber={passport.passportnumber}")
        raise HTTPException(status_code=400, detail="Passport already exists")
    logger.info(f"Created passport: id={result.id}, passportnumber={result.passportnumber}")
    return result

@router.get("/{passport_id}", response_model=PassportOut)
async def get_passport_endpoint(passport_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_passport(passport_id)
    if not result:
        logger.warning(f"Passport not found: id={passport_id}")
        raise HTTPException(status_code=404, detail="Passport not found")
    logger.info(f"Retrieved passport: id={result.id}, passportnumber={result.passportnumber}")
    return result

@router.get("/", response_model=List[PassportOut])
async def get_all_passports_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_passports()
    logger.info(f"Retrieved {len(results)} passports")
    return results

@router.put("/{passport_id}", response_model=PassportOut)
async def update_passport_endpoint(passport_id: int, passport: PassportUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_passport(passport_id, passport)
    if not result:
        logger.warning(f"Failed to update passport: id={passport_id}")
        raise HTTPException(status_code=404, detail="Passport not found or already exists")
    logger.info(f"Updated passport: id={result.id}, passportnumber={result.passportnumber}")
    return result

@router.delete("/{passport_id}")
async def delete_passport_endpoint(passport_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_passport(passport_id)
    if not result:
        logger.warning(f"Passport not found for deletion: id={passport_id}")
        raise HTTPException(status_code=404, detail="Passport not found")
    logger.info(f"Deleted passport: id={passport_id}")
    return {"message": "Passport deleted"}