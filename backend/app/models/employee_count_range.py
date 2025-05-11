from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.employee_count_range import EmployeeCountRangeCreate, EmployeeCountRangeUpdate, EmployeeCountRangeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_employee_count_range(employee_count_range: EmployeeCountRangeCreate) -> Optional[EmployeeCountRangeOut]:
    query = """
        SELECT id, description FROM employee_count_range WHERE description = :description
    """
    existing = await database.fetch_one(query=query, values={"description": employee_count_range.description})
    if existing:
        logger.warning(f"Employee count range with description '{employee_count_range.description}' already exists")
        return None

    query = """
        INSERT INTO employee_count_range (description)
        VALUES (:description)
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": employee_count_range.description})
        logger.info(f"Created employee count range: id={result['id']}, description={result['description']}")
        return EmployeeCountRangeOut(**result)
    except Exception as e:
        logger.error(f"Error creating employee count range: {str(e)}")
        raise

async def get_employee_count_range(employee_count_range_id: int) -> Optional[EmployeeCountRangeOut]:
    query = """
        SELECT id, description FROM employee_count_range WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": employee_count_range_id})
    if not result:
        logger.warning(f"Employee count range not found: id={employee_count_range_id}")
        return None
    logger.info(f"Retrieved employee count range: id={result['id']}, description={result['description']}")
    return EmployeeCountRangeOut(**result)

async def get_all_employee_count_ranges() -> List[EmployeeCountRangeOut]:
    query = """
        SELECT id, description FROM employee_count_range
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} employee count ranges")
    return [EmployeeCountRangeOut(**result) for result in results]

async def update_employee_count_range(employee_count_range_id: int, employee_count_range: EmployeeCountRangeUpdate) -> Optional[EmployeeCountRangeOut]:
    if employee_count_range.description:
        query = """
            SELECT id, description FROM employee_count_range WHERE description = :description AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"description": employee_count_range.description, "id": employee_count_range_id})
        if existing:
            logger.warning(f"Employee count range with description '{employee_count_range.description}' already exists")
            return None

    query = """
        UPDATE employee_count_range
        SET description = COALESCE(:description, description)
        WHERE id = :id
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": employee_count_range.description, "id": employee_count_range_id})
        if not result:
            logger.warning(f"Employee count range not found for update: id={employee_count_range_id}")
            return None
        logger.info(f"Updated employee count range: id={result['id']}, description={result['description']}")
        return EmployeeCountRangeOut(**result)
    except Exception as e:
        logger.error(f"Error updating employee count range: {str(e)}")
        raise

async def delete_employee_count_range(employee_count_range_id: int) -> bool:
    query = """
        DELETE FROM employee_count_range WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": employee_count_range_id})
    if not result:
        logger.warning(f"Employee count range not found for deletion: id={employee_count_range_id}")
        return False
    logger.info(f"Deleted employee count range: id={employee_count_range_id}")
    return True