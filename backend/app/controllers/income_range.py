from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.income_range import (
    create_income_range, get_income_range, get_all_income_ranges,
    update_income_range, delete_income_range
)
from app.schemas.income_range import IncomeRangeCreate, IncomeRangeUpdate, IncomeRangeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/incomerange", tags=["income_range"])

@router.post("/", response_model=IncomeRangeOut)
async def create_income_range_endpoint(income_range: IncomeRangeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_income_range(income_range)
    if not result:
        logger.warning(f"Failed to create income range: description={income_range.description}")
        raise HTTPException(status_code=400, detail="Description already exists")
    logger.info(f"Created income range: id={result.id}, description={result.description}")
    return result

@router.get("/{income_range_id}", response_model=IncomeRangeOut)
async def get_income_range_endpoint(income_range_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_income_range(income_range_id)
    if not result:
        logger.warning(f"Income range not found: id={income_range_id}")
        raise HTTPException(status_code=404, detail="Income range not found")
    logger.info(f"Retrieved income range: id={result.id}, description={result.description}")
    return result

@router.get("/", response_model=List[IncomeRangeOut])
async def get_all_income_ranges_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_income_ranges()
    logger.info(f"Retrieved {len(results)} income ranges")
    return results

@router.put("/{income_range_id}", response_model=IncomeRangeOut)
async def update_income_range_endpoint(income_range_id: int, income_range: IncomeRangeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_income_range(income_range_id, income_range)
    if not result:
        logger.warning(f"Failed to update income range: id={income_range_id}")
        raise HTTPException(status_code=404, detail="Income range not found or description already exists")
    logger.info(f"Updated income range: id={result.id}, description={result.description}")
    return result

@router.delete("/{income_range_id}")
async def delete_income_range_endpoint(income_range_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_income_range(income_range_id)
    if not result:
        logger.warning(f"Income range not found for deletion: id={income_range_id}")
        raise HTTPException(status_code=404, detail="Income range not found")
    logger.info(f"Deleted income range: id={income_range_id}")
    return {"message": "Income range deleted"}