from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.party_type import PartyTypeCreate, PartyTypeUpdate, PartyTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_party_type(party_type: PartyTypeCreate) -> Optional[PartyTypeOut]:
    query = """
        SELECT id, description FROM party_type WHERE description = :description
    """
    existing = await database.fetch_one(query=query, values={"description": party_type.description})
    if existing:
        logger.warning(f"Party type with description '{party_type.description}' already exists")
        return None

    query = """
        INSERT INTO party_type (description)
        VALUES (:description)
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": party_type.description})
        logger.info(f"Created party type: id={result['id']}, description={result['description']}")
        return PartyTypeOut(**result)
    except Exception as e:
        logger.error(f"Error creating party type: {str(e)}")
        raise

async def get_party_type(party_type_id: int) -> Optional[PartyTypeOut]:
    query = """
        SELECT id, description FROM party_type WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": party_type_id})
    if not result:
        logger.warning(f"Party type not found: id={party_type_id}")
        return None
    logger.info(f"Retrieved party type: id={result['id']}, description={result['description']}")
    return PartyTypeOut(**result)

async def get_all_party_types() -> List[PartyTypeOut]:
    query = """
        SELECT id, description FROM party_type
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} party types")
    return [PartyTypeOut(**result) for result in results]

async def update_party_type(party_type_id: int, party_type: PartyTypeUpdate) -> Optional[PartyTypeOut]:
    if party_type.description:
        query = """
            SELECT id, description FROM party_type WHERE description = :description AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"description": party_type.description, "id": party_type_id})
        if existing:
            logger.warning(f"Party type with description '{party_type.description}' already exists")
            return None

    query = """
        UPDATE party_type
        SET description = COALESCE(:description, description)
        WHERE id = :id
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": party_type.description, "id": party_type_id})
        if not result:
            logger.warning(f"Party type not found for update: id={party_type_id}")
            return None
        logger.info(f"Updated party type: id={result['id']}, description={result['description']}")
        return PartyTypeOut(**result)
    except Exception as e:
        logger.error(f"Error updating party type: {str(e)}")
        raise

async def delete_party_type(party_type_id: int) -> bool:
    query = """
        SELECT id FROM party_classification WHERE party_type_id = :id LIMIT 1
    """
    referenced = await database.fetch_one(query=query, values={"id": party_type_id})
    if referenced:
        logger.warning(f"Cannot delete party type: id={party_type_id}, referenced in party_classification")
        return False

    query = """
        DELETE FROM party_type WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": party_type_id})
    if not result:
        logger.warning(f"Party type not found for deletion: id={party_type_id}")
        return False
    logger.info(f"Deleted party type: id={party_type_id}")
    return True