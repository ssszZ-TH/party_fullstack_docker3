from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.classify_by_income import (
    create_classify_by_income, get_classify_by_income, get_all_classify_by_incomes,
    update_classify_by_income, delete_classify_by_income, get_classify_by_income_by_person_id
)
from app.schemas.classify_by_income import ClassifyByIncomeCreate, ClassifyByIncomeUpdate, ClassifyByIncomeOut, ClassifyByIncomeByPersonIdOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/classifybyincome", tags=["classifybyincome"])

@router.post("/", response_model=ClassifyByIncomeOut)
async def create_classify_by_income_endpoint(classify_by_income: ClassifyByIncomeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_classify_by_income(classify_by_income)
    if not result:
        logger.warning(f"Failed to create classify_by_income")
        raise HTTPException(status_code=400, detail="Failed to create classify_by_income")
    logger.info(f"Created classify_by_income: id={result.id}")
    return result

@router.get("/{classify_by_income_id}", response_model=ClassifyByIncomeOut)
async def get_classify_by_income_endpoint(classify_by_income_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_classify_by_income(classify_by_income_id)
    if not result:
        logger.warning(f"Classify_by_income not found: id={classify_by_income_id}")
        raise HTTPException(status_code=404, detail="Classify_by_income not found")
    logger.info(f"Retrieved classify_by_income: id={result.id}")
    return result

@router.get("/", response_model=List[ClassifyByIncomeOut])
async def get_all_classify_by_incomes_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_classify_by_incomes()
    logger.info(f"Retrieved {len(results)} classify_by_incomes")
    return results

@router.get("/bypersonid/{person_id}", response_model=List[ClassifyByIncomeByPersonIdOut])
async def get_classify_by_income_by_person_id_endpoint(
    person_id: int, 
    current_user: dict = Depends(get_current_user)
):
    results = await get_classify_by_income_by_person_id(person_id)
    if not results:
        logger.warning(f"No classify_by_income found for person_id: {person_id}")
        return []
    logger.info(f"Retrieved {len(results)} classify_by_income by person_id: {person_id}")
    return results

@router.put("/{classify_by_income_id}", response_model=ClassifyByIncomeOut)
async def update_classify_by_income_endpoint(classify_by_income_id: int, classify_by_income: ClassifyByIncomeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_classify_by_income(classify_by_income_id, classify_by_income)
    if not result:
        logger.warning(f"Classify_by_income not found for update: id={classify_by_income_id}")
        raise HTTPException(status_code=404, detail="Classify_by_income not found")
    logger.info(f"Updated classify_by_income: id={result.id}")
    return result

@router.delete("/{classify_by_income_id}")
async def delete_classify_by_income_endpoint(classify_by_income_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_classify_by_income(classify_by_income_id)
    if not result:
        logger.warning(f"Classify_by_income not found for deletion: id={classify_by_income_id}")
        raise HTTPException(status_code=404, detail="Classify_by_income not found")
    logger.info(f"Deleted classify_by_income: id={classify_by_income_id}")
    return {"message": "Classify_by_income deleted"}