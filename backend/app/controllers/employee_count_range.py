from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.employee_count_range import (
    create_employee_count_range, get_employee_count_range, get_all_employee_count_ranges,
    update_employee_count_range, delete_employee_count_range
)
from app.schemas.employee_count_range import EmployeeCountRangeCreate, EmployeeCountRangeUpdate, EmployeeCountRangeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/employeecountrange", tags=["employee_count_range"])

@router.post("/", response_model=EmployeeCountRangeOut)
async def create_employee_count_range_endpoint(employee_count_range: EmployeeCountRangeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_employee_count_range(employee_count_range)
    if not result:
        logger.warning(f"Failed to create employee count range: description={employee_count_range.description}")
        raise HTTPException(status_code=400, detail="Description already exists")
    logger.info(f"Created employee count range: id={result.id}, description={result.description}")
    return result

@router.get("/{employee_count_range_id}", response_model=EmployeeCountRangeOut)
async def get_employee_count_range_endpoint(employee_count_range_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_employee_count_range(employee_count_range_id)
    if not result:
        logger.warning(f"Employee count range not found: id={employee_count_range_id}")
        raise HTTPException(status_code=404, detail="Employee count range not found")
    logger.info(f"Retrieved employee count range: id={result.id}, description={result.description}")
    return result

@router.get("/", response_model=List[EmployeeCountRangeOut])
async def get_all_employee_count_ranges_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_employee_count_ranges()
    logger.info(f"Retrieved {len(results)} employee count ranges")
    return results

@router.put("/{employee_count_range_id}", response_model=EmployeeCountRangeOut)
async def update_employee_count_range_endpoint(employee_count_range_id: int, employee_count_range: EmployeeCountRangeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_employee_count_range(employee_count_range_id, employee_count_range)
    if not result:
        logger.warning(f"Failed to update employee count range: id={employee_count_range_id}")
        raise HTTPException(status_code=404, detail="Employee count range not found or description already exists")
    logger.info(f"Updated employee count range: id={result.id}, description={result.description}")
    return result

@router.delete("/{employee_count_range_id}")
async def delete_employee_count_range_endpoint(employee_count_range_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_employee_count_range(employee_count_range_id)
    if not result:
        logger.warning(f"Employee count range not found for deletion: id={employee_count_range_id}")
        raise HTTPException(status_code=404, detail="Employee count range not found")
    logger.info(f"Deleted employee count range: id={employee_count_range_id}")
    return {"message": "Employee count range deleted"}