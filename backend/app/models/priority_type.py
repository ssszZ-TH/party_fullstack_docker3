from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.priority_type import PriorityTypeCreate, PriorityTypeUpdate, PriorityTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_priority_type(priority_type: PriorityTypeCreate) -> Optional[PriorityTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO priority_type (description)
                VALUES (:description)
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={"description": priority_type.description})
            logger.info(f"Created priority_type: id={result['id']}")
            return PriorityTypeOut(**result)
        except Exception as e:
            logger.error(f"Error creating priority_type: {str(e)}")
            raise

async def get_priority_type(priority_type_id: int) -> Optional[PriorityTypeOut]:
    query = """
        SELECT id, description
        FROM priority_type
        WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": priority_type_id})
    if not result:
        logger.warning(f"Priority_type not found: id={priority_type_id}")
        return None
    logger.info(f"Retrieved priority_type: id={result['id']}")
    return PriorityTypeOut(**result)

async def get_all_priority_types() -> List[PriorityTypeOut]:
    query = """
        SELECT id, description
        FROM priority_type
        ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} priority_types")
    return [PriorityTypeOut(**result) for result in results]

async def update_priority_type(priority_type_id: int, priority_type: PriorityTypeUpdate) -> Optional[PriorityTypeOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE priority_type
                SET description = COALESCE(:description, description)
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={
                "description": priority_type.description,
                "id": priority_type_id
            })
            if not result:
                logger.warning(f"Priority_type not found for update: id={priority_type_id}")
                return None
            logger.info(f"Updated priority_type: id={priority_type_id}")
            return PriorityTypeOut(**result)
        except Exception as e:
            logger.error(f"Error updating priority_type: {str(e)}")
            raise

async def delete_priority_type(priority_type_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM priority_type
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": priority_type_id})
            if not result:
                logger.warning(f"Priority_type not found for deletion: id={priority_type_id}")
                return False
            logger.info(f"Deleted priority_type: id={priority_type_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting priority_type: {str(e)}")
            raise