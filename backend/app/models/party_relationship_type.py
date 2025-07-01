from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.party_relationship_type import PartyRelationshipTypeCreate, PartyRelationshipTypeUpdate, PartyRelationshipTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_party_relationship_type(party_relationship_type: PartyRelationshipTypeCreate) -> Optional[PartyRelationshipTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO party_relationship_type (description)
                VALUES (:description)
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={"description": party_relationship_type.description})
            logger.info(f"Created party_relationship_type: id={result['id']}")
            return PartyRelationshipTypeOut(**result)
        except Exception as e:
            logger.error(f"Error creating party_relationship_type: {str(e)}")
            raise

async def get_party_relationship_type(party_relationship_type_id: int) -> Optional[PartyRelationshipTypeOut]:
    query = """
        SELECT id, description
        FROM party_relationship_type
        WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": party_relationship_type_id})
    if not result:
        logger.warning(f"Party_relationship_type not found: id={party_relationship_type_id}")
        return None
    logger.info(f"Retrieved party_relationship_type: id={result['id']}")
    return PartyRelationshipTypeOut(**result)

async def get_all_party_relationship_types() -> List[PartyRelationshipTypeOut]:
    query = """
        SELECT id, description
        FROM party_relationship_type
        ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} party_relationship_types")
    return [PartyRelationshipTypeOut(**result) for result in results]

async def update_party_relationship_type(party_relationship_type_id: int, party_relationship_type: PartyRelationshipTypeUpdate) -> Optional[PartyRelationshipTypeOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE party_relationship_type
                SET description = COALESCE(:description, description)
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={
                "description": party_relationship_type.description,
                "id": party_relationship_type_id
            })
            if not result:
                logger.warning(f"Party_relationship_type not found for update: id={party_relationship_type_id}")
                return None
            logger.info(f"Updated party_relationship_type: id={party_relationship_type_id}")
            return PartyRelationshipTypeOut(**result)
        except Exception as e:
            logger.error(f"Error updating party_relationship_type: {str(e)}")
            raise

async def delete_party_relationship_type(party_relationship_type_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM party_relationship_type
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": party_relationship_type_id})
            if not result:
                logger.warning(f"Party_relationship_type not found for deletion: id={party_relationship_type_id}")
                return False
            logger.info(f"Deleted party_relationship_type: id={party_relationship_type_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting party_relationship_type: {str(e)}")
            raise