from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.party_relationship_status_type import PartyRelationshipStatusTypeCreate, PartyRelationshipStatusTypeUpdate, PartyRelationshipStatusTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_party_relationship_status_type(party_relationship_status_type: PartyRelationshipStatusTypeCreate) -> Optional[PartyRelationshipStatusTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO party_relationship_status_type (description)
                VALUES (:description)
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={"description": party_relationship_status_type.description})
            logger.info(f"Created party_relationship_status_type: id={result['id']}")
            return PartyRelationshipStatusTypeOut(**result)
        except Exception as e:
            logger.error(f"Error creating party_relationship_status_type: {str(e)}")
            raise

async def get_party_relationship_status_type(party_relationship_status_type_id: int) -> Optional[PartyRelationshipStatusTypeOut]:
    query = """
        SELECT id, description
        FROM party_relationship_status_type
        WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": party_relationship_status_type_id})
    if not result:
        logger.warning(f"Party_relationship_status_type not found: id={party_relationship_status_type_id}")
        return None
    logger.info(f"Retrieved party_relationship_status_type: id={result['id']}")
    return PartyRelationshipStatusTypeOut(**result)

async def get_all_party_relationship_status_types() -> List[PartyRelationshipStatusTypeOut]:
    query = """
        SELECT id, description
        FROM party_relationship_status_type
        ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} party_relationship_status_types")
    return [PartyRelationshipStatusTypeOut(**result) for result in results]

async def update_party_relationship_status_type(party_relationship_status_type_id: int, party_relationship_status_type: PartyRelationshipStatusTypeUpdate) -> Optional[PartyRelationshipStatusTypeOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE party_relationship_status_type
                SET description = COALESCE(:description, description)
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={
                "description": party_relationship_status_type.description,
                "id": party_relationship_status_type_id
            })
            if not result:
                logger.warning(f"Party_relationship_status_type not found for update: id={party_relationship_status_type_id}")
                return None
            logger.info(f"Updated party_relationship_status_type: id={party_relationship_status_type_id}")
            return PartyRelationshipStatusTypeOut(**result)
        except Exception as e:
            logger.error(f"Error updating party_relationship_status_type: {str(e)}")
            raise

async def delete_party_relationship_status_type(party_relationship_status_type_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM party_relationship_status_type
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": party_relationship_status_type_id})
            if not result:
                logger.warning(f"Party_relationship_status_type not found for deletion: id={party_relationship_status_type_id}")
                return False
            logger.info(f"Deleted party_relationship_status_type: id={party_relationship_status_type_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting party_relationship_status_type: {str(e)}")
            raise