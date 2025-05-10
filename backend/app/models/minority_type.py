from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.minority_type import MinorityTypeCreate, MinorityTypeUpdate, MinorityTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_minority_type(minority_type: MinorityTypeCreate) -> Optional[MinorityTypeOut]:
    query = """
        SELECT id, name_en, name_th FROM minority_type WHERE name_en = :name_en
    """
    existing = await database.fetch_one(query=query, values={"name_en": minority_type.name_en})
    if existing:
        logger.warning(f"Minority type with name_en '{minority_type.name_en}' already exists")
        return None

    query = """
        INSERT INTO minority_type (name_en, name_th)
        VALUES (:name_en, :name_th)
        RETURNING id, name_en, name_th
    """
    try:
        result = await database.fetch_one(query=query, values={"name_en": minority_type.name_en, "name_th": minority_type.name_th})
        logger.info(f"Created minority type: id={result['id']}, name_en={result['name_en']}")
        return MinorityTypeOut(**result)
    except Exception as e:
        logger.error(f"Error creating minority type: {str(e)}")
        raise

async def get_minority_type(minority_type_id: int) -> Optional[MinorityTypeOut]:
    query = """
        SELECT id, name_en, name_th FROM minority_type WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": minority_type_id})
    if not result:
        logger.warning(f"Minority type not found: id={minority_type_id}")
        return None
    logger.info(f"Retrieved minority type: id={result['id']}, name_en={result['name_en']}")
    return MinorityTypeOut(**result)

async def get_all_minority_types() -> List[MinorityTypeOut]:
    query = """
        SELECT id, name_en, name_th FROM minority_type
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} minority types")
    return [MinorityTypeOut(**result) for result in results]

async def update_minority_type(minority_type_id: int, minority_type: MinorityTypeUpdate) -> Optional[MinorityTypeOut]:
    if minority_type.name_en:
        query = """
            SELECT id, name_en, name_th FROM minority_type WHERE name_en = :name_en AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"name_en": minority_type.name_en, "id": minority_type_id})
        if existing:
            logger.warning(f"Minority type with name_en '{minority_type.name_en}' already exists")
            return None

    query = """
        UPDATE minority_type
        SET name_en = COALESCE(:name_en, name_en),
            name_th = COALESCE(:name_th, name_th)
        WHERE id = :id
        RETURNING id, name_en, name_th
    """
    try:
        result = await database.fetch_one(query=query, values={"name_en": minority_type.name_en, "name_th": minority_type.name_th, "id": minority_type_id})
        if not result:
            logger.warning(f"Minority type not found for update: id={minority_type_id}")
            return None
        logger.info(f"Updated minority type: id={result['id']}, name_en={result['name_en']}")
        return MinorityTypeOut(**result)
    except Exception as e:
        logger.error(f"Error updating minority type: {str(e)}")
        raise

async def delete_minority_type(minority_type_id: int) -> bool:
    query = """
        DELETE FROM minority_type WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": minority_type_id})
    if not result:
        logger.warning(f"Minority type not found for deletion: id={minority_type_id}")
        return False
    logger.info(f"Deleted minority type: id={minority_type_id}")
    return True