from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.person_name_type import PersonNameTypeCreate, PersonNameTypeUpdate, PersonNameTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_person_name_type(person_name_type: PersonNameTypeCreate) -> Optional[PersonNameTypeOut]:
    query = """
        SELECT id, description FROM personnametype WHERE description = :description
    """
    existing = await database.fetch_one(query=query, values={"description": person_name_type.description})
    if existing:
        logger.warning(f"Person name type with description '{person_name_type.description}' already exists")
        return None

    query = """
        INSERT INTO personnametype (description)
        VALUES (:description)
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": person_name_type.description})
        logger.info(f"Created person name type: id={result['id']}, description={result['description']}")
        return PersonNameTypeOut(**result)
    except Exception as e:
        logger.error(f"Error creating person name type: {str(e)}")
        raise

async def get_person_name_type(person_name_type_id: int) -> Optional[PersonNameTypeOut]:
    query = """
        SELECT id, description FROM personnametype WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": person_name_type_id})
    if not result:
        logger.warning(f"Person name type not found: id={person_name_type_id}")
        return None
    logger.info(f"Retrieved person name type: id={result['id']}, description={result['description']}")
    return PersonNameTypeOut(**result)

async def get_all_person_name_types() -> List[PersonNameTypeOut]:
    query = """
        SELECT id, description FROM personnametype
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} person name types")
    return [PersonNameTypeOut(**result) for result in results]

async def update_person_name_type(person_name_type_id: int, person_name_type: PersonNameTypeUpdate) -> Optional[PersonNameTypeOut]:
    if person_name_type.description:
        query = """
            SELECT id, description FROM personnametype WHERE description = :description AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"description": person_name_type.description, "id": person_name_type_id})
        if existing:
            logger.warning(f"Person name type with description '{person_name_type.description}' already exists")
            return None

    query = """
        UPDATE personnametype
        SET description = COALESCE(:description, description)
        WHERE id = :id
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": person_name_type.description, "id": person_name_type_id})
        if not result:
            logger.warning(f"Person name type not found for update: id={person_name_type_id}")
            return None
        logger.info(f"Updated person name type: id={result['id']}, description={result['description']}")
        return PersonNameTypeOut(**result)
    except Exception as e:
        logger.error(f"Error updating person name type: {str(e)}")
        raise

async def delete_person_name_type(person_name_type_id: int) -> bool:
    query = """
        DELETE FROM personnametype WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": person_name_type_id})
    if not result:
        logger.warning(f"Person name type not found for deletion: id={person_name_type_id}")
        return False
    logger.info(f"Deleted person name type: id={person_name_type_id}")
    return True