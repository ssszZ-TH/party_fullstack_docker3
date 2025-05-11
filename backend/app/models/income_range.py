from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.income_range import IncomeRangeCreate, IncomeRangeUpdate, IncomeRangeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_income_range(income_range: IncomeRangeCreate) -> Optional[IncomeRangeOut]:
    query = """
        SELECT id, description FROM income_range WHERE description = :description
    """
    existing = await database.fetch_one(query=query, values={"description": income_range.description})
    if existing:
        logger.warning(f"Income range with description '{income_range.description}' already exists")
        return None

    query = """
        INSERT INTO income_range (description)
        VALUES (:description)
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": income_range.description})
        logger.info(f"Created income range: id={result['id']}, description={result['description']}")
        return IncomeRangeOut(**result)
    except Exception as e:
        logger.error(f"Error creating income range: {str(e)}")
        raise

async def get_income_range(income_range_id: int) -> Optional[IncomeRangeOut]:
    query = """
        SELECT id, description FROM income_range WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": income_range_id})
    if not result:
        logger.warning(f"Income range not found: id={income_range_id}")
        return None
    logger.info(f"Retrieved income range: id={result['id']}, description={result['description']}")
    return IncomeRangeOut(**result)

async def get_all_income_ranges() -> List[IncomeRangeOut]:
    query = """
        SELECT id, description FROM income_range
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} income ranges")
    return [IncomeRangeOut(**result) for result in results]

async def update_income_range(income_range_id: int, income_range: IncomeRangeUpdate) -> Optional[IncomeRangeOut]:
    if income_range.description:
        query = """
            SELECT id, description FROM income_range WHERE description = :description AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"description": income_range.description, "id": income_range_id})
        if existing:
            logger.warning(f"Income range with description '{income_range.description}' already exists")
            return None

    query = """
        UPDATE income_range
        SET description = COALESCE(:description, description)
        WHERE id = :id
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": income_range.description, "id": income_range_id})
        if not result:
            logger.warning(f"Income range not found for update: id={income_range_id}")
            return None
        logger.info(f"Updated income range: id={result['id']}, description={result['description']}")
        return IncomeRangeOut(**result)
    except Exception as e:
        logger.error(f"Error updating income range: {str(e)}")
        raise

async def delete_income_range(income_range_id: int) -> bool:
    query = """
        DELETE FROM income_range WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": income_range_id})
    if not result:
        logger.warning(f"Income range not found for deletion: id={income_range_id}")
        return False
    logger.info(f"Deleted income range: id={income_range_id}")
    return True