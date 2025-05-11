from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.ethnicity import EthnicityCreate, EthnicityUpdate, EthnicityOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_ethnicity(ethnicity: EthnicityCreate) -> Optional[EthnicityOut]:
    query = """
        SELECT id, name_en, name_th FROM ethnicity WHERE name_en = :name_en
    """
    existing = await database.fetch_one(query=query, values={"name_en": ethnicity.name_en})
    if existing:
        logger.warning(f"Ethnicity with name_en '{ethnicity.name_en}' already exists")
        return None

    query = """
        INSERT INTO ethnicity (name_en, name_th)
        VALUES (:name_en, :name_th)
        RETURNING id, name_en, name_th
    """
    try:
        result = await database.fetch_one(query=query, values={"name_en": ethnicity.name_en, "name_th": ethnicity.name_th})
        logger.info(f"Created ethnicity: id={result['id']}, name_en={result['name_en']}")
        return EthnicityOut(**result)
    except Exception as e:
        logger.error(f"Error creating ethnicity: {str(e)}")
        raise

async def get_ethnicity(ethnicity_id: int) -> Optional[EthnicityOut]:
    query = """
        SELECT id, name_en, name_th FROM ethnicity WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": ethnicity_id})
    if not result:
        logger.warning(f"Ethnicity not found: id={ethnicity_id}")
        return None
    logger.info(f"Retrieved ethnicity: id={result['id']}, name_en={result['name_en']}")
    return EthnicityOut(**result)

async def get_all_ethnicities() -> List[EthnicityOut]:
    query = """
        SELECT id, name_en, name_th FROM ethnicity
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} ethnicities")
    return [EthnicityOut(**result) for result in results]

async def update_ethnicity(ethnicity_id: int, ethnicity: EthnicityUpdate) -> Optional[EthnicityOut]:
    if ethnicity.name_en:
        query = """
            SELECT id, name_en, name_th FROM ethnicity WHERE name_en = :name_en AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"name_en": ethnicity.name_en, "id": ethnicity_id})
        if existing:
            logger.warning(f"Ethnicity with name_en '{ethnicity.name_en}' already exists")
            return None

    query = """
        UPDATE ethnicity
        SET name_en = COALESCE(:name_en, name_en),
            name_th = COALESCE(:name_th, name_th)
        WHERE id = :id
        RETURNING id, name_en, name_th
    """
    try:
        result = await database.fetch_one(query=query, values={"name_en": ethnicity.name_en, "name_th": ethnicity.name_th, "id": ethnicity_id})
        if not result:
            logger.warning(f"Ethnicity not found for update: id={ethnicity_id}")
            return None
        logger.info(f"Updated ethnicity: id={result['id']}, name_en={result['name_en']}")
        return EthnicityOut(**result)
    except Exception as e:
        logger.error(f"Error updating ethnicity: {str(e)}")
        raise

async def delete_ethnicity(ethnicity_id: int) -> bool:
    query = """
        DELETE FROM ethnicity WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": ethnicity_id})
    if not result:
        logger.warning(f"Ethnicity not found for deletion: id={ethnicity_id}")
        return False
    logger.info(f"Deleted ethnicity: id={ethnicity_id}")
    return True