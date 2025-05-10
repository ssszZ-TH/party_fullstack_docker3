from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.marital_status_type import MaritalStatusTypeCreate, MaritalStatusTypeUpdate, MaritalStatusTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_marital_status_type(marital_status_type: MaritalStatusTypeCreate) -> Optional[MaritalStatusTypeOut]:
    query = """
        SELECT id, description FROM maritalstatustype WHERE description = :description
    """
    existing = await database.fetch_one(query=query, values={"description": marital_status_type.description})
    if existing:
        logger.warning(f"Marital status type with description '{marital_status_type.description}' already exists")
        return None

    query = """
        INSERT INTO maritalstatustype (description)
        VALUES (:description)
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": marital_status_type.description})
        logger.info(f"Created marital status type: id={result['id']}, description={result['description']}")
        return MaritalStatusTypeOut(**result)
    except Exception as e:
        logger.error(f"Error creating marital status type: {str(e)}")
        raise

async def get_marital_status_type(marital_status_type_id: int) -> Optional[MaritalStatusTypeOut]:
    query = """
        SELECT id, description FROM maritalstatustype WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": marital_status_type_id})
    if not result:
        logger.warning(f"Marital status type not found: id={marital_status_type_id}")
        return None
    logger.info(f"Retrieved marital status type: id={result['id']}, description={result['description']}")
    return MaritalStatusTypeOut(**result)

async def get_all_marital_status_types() -> List[MaritalStatusTypeOut]:
    query = """
        SELECT id, description FROM maritalstatustype
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} marital status types")
    return [MaritalStatusTypeOut(**result) for result in results]

async def update_marital_status_type(marital_status_type_id: int, marital_status_type: MaritalStatusTypeUpdate) -> Optional[MaritalStatusTypeOut]:
    if marital_status_type.description:
        query = """
            SELECT id, description FROM maritalstatustype WHERE description = :description AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"description": marital_status_type.description, "id": marital_status_type_id})
        if existing:
            logger.warning(f"Marital status type with description '{marital_status_type.description}' already exists")
            return None

    query = """
        UPDATE maritalstatustype
        SET description = COALESCE(:description, description)
        WHERE id = :id
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": marital_status_type.description, "id": marital_status_type_id})
        if not result:
            logger.warning(f"Marital status type not found for update: id={marital_status_type_id}")
            return None
        logger.info(f"Updated marital status type: id={result['id']}, description={result['description']}")
        return MaritalStatusTypeOut(**result)
    except Exception as e:
        logger.error(f"Error updating marital status type: {str(e)}")
        raise

async def delete_marital_status_type(marital_status_type_id: int) -> bool:
    query = """
        DELETE FROM maritalstatustype WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": marital_status_type_id})
    if not result:
        logger.warning(f"Marital status type not found for deletion: id={marital_status_type_id}")
        return False
    logger.info(f"Deleted marital status type: id={marital_status_type_id}")
    return True