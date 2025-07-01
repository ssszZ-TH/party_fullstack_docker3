from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.communication_event_purpose_type import CommunicationEventPurposeTypeCreate, CommunicationEventPurposeTypeUpdate, CommunicationEventPurposeTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_communication_event_purpose_type(communication_event_purpose_type: CommunicationEventPurposeTypeCreate) -> Optional[CommunicationEventPurposeTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO communication_event_purpose_type (description)
                VALUES (:description)
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={"description": communication_event_purpose_type.description})
            logger.info(f"Created communication_event_purpose_type: id={result['id']}")
            return CommunicationEventPurposeTypeOut(**result)
        except Exception as e:
            logger.error(f"Error creating communication_event_purpose_type: {str(e)}")
            raise

async def get_communication_event_purpose_type(communication_event_purpose_type_id: int) -> Optional[CommunicationEventPurposeTypeOut]:
    query = """
        SELECT id, description
        FROM communication_event_purpose_type
        WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": communication_event_purpose_type_id})
    if not result:
        logger.warning(f"Communication_event_purpose_type not found: id={communication_event_purpose_type_id}")
        return None
    logger.info(f"Retrieved communication_event_purpose_type: id={result['id']}")
    return CommunicationEventPurposeTypeOut(**result)

async def get_all_communication_event_purpose_types() -> List[CommunicationEventPurposeTypeOut]:
    query = """
        SELECT id, description
        FROM communication_event_purpose_type
        ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} communication_event_purpose_types")
    return [CommunicationEventPurposeTypeOut(**result) for result in results]

async def update_communication_event_purpose_type(communication_event_purpose_type_id: int, communication_event_purpose_type: CommunicationEventPurposeTypeUpdate) -> Optional[CommunicationEventPurposeTypeOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE communication_event_purpose_type
                SET description = COALESCE(:description, description)
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={
                "description": communication_event_purpose_type.description,
                "id": communication_event_purpose_type_id
            })
            if not result:
                logger.warning(f"Communication_event_purpose_type not found for update: id={communication_event_purpose_type_id}")
                return None
            logger.info(f"Updated communication_event_purpose_type: id={communication_event_purpose_type_id}")
            return CommunicationEventPurposeTypeOut(**result)
        except Exception as e:
            logger.error(f"Error updating communication_event_purpose_type: {str(e)}")
            raise

async def delete_communication_event_purpose_type(communication_event_purpose_type_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM communication_event_purpose_type
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": communication_event_purpose_type_id})
            if not result:
                logger.warning(f"Communication_event_purpose_type not found for deletion: id={communication_event_purpose_type_id}")
                return False
            logger.info(f"Deleted communication_event_purpose_type: id={communication_event_purpose_type_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting communication_event_purpose_type: {str(e)}")
            raise