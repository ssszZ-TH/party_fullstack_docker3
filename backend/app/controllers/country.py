from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.country import (
    create_country, get_country, get_all_countries,
    update_country, delete_country
)
from app.schemas.country import CountryCreate, CountryUpdate, CountryOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/country", tags=["country"])

@router.post("/", response_model=CountryOut)
async def create_country_endpoint(country: CountryCreate, current_user: dict = Depends(get_current_user)):
    result = await create_country(country)
    if not result:
        logger.warning(f"Failed to create country: isocode={country.isocode}")
        raise HTTPException(status_code=400, detail="ISO code already exists")
    logger.info(f"Created country: id={result.id}, isocode={result.isocode}")
    return result

@router.get("/{country_id}", response_model=CountryOut)
async def get_country_endpoint(country_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_country(country_id)
    if not result:
        logger.warning(f"Country not found: id={country_id}")
        raise HTTPException(status_code=404, detail="Country not found")
    logger.info(f"Retrieved country: id={result.id}, isocode={result.isocode}")
    return result

@router.get("/", response_model=List[CountryOut])
async def get_all_countries_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_countries()
    logger.info(f"Retrieved {len(results)} countries")
    return results

@router.put("/{country_id}", response_model=CountryOut)
async def update_country_endpoint(country_id: int, country: CountryUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_country(country_id, country)
    if not result:
        logger.warning(f"Failed to update country: id={country_id}")
        raise HTTPException(status_code=404, detail="Country not found or ISO code already exists")
    logger.info(f"Updated country: id={result.id}, isocode={result.isocode}")
    return result

@router.delete("/{country_id}")
async def delete_country_endpoint(country_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_country(country_id)
    if not result:
        logger.warning(f"Country not found for deletion: id={country_id}")
        raise HTTPException(status_code=404, detail="Country not found")
    logger.info(f"Deleted country: id={country_id}")
    return {"message": "Country deleted"}