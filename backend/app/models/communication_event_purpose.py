from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.communication_event_purpose import CommunicationEventPurposeCreate, CommunicationEventPurposeUpdate, CommunicationEventPurposeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_communication_event_purpose(communication_event_purpose: CommunicationEventPurposeCreate) -> Optional[CommunicationEventPurposeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO communication_event_purpose (communication_event_id, communication_event_purpose_type_id)
                VALUES (:communication_event_id, :communication_event_purpose_type_id)
                RETURNING id, communication_event_id, communication_event_purpose_type_id
            """
            result = await database.fetch_one(query=query, values={
                "communication_event_id": communication_event_purpose.communication_event_id,
                "communication_event_purpose_type_id": communication_event_purpose.communication_event_purpose_type_id
            })
            new_id = result["id"]

            query_fetch = """
                SELECT cep.id, cep.communication_event_id, cep.communication_event_purpose_type_id,
                       ce.note AS communication_event_note,
                       cept.description AS communication_event_purpose_type_description
                FROM communication_event_purpose cep
                JOIN communication_event ce ON cep.communication_event_id = ce.id
                JOIN communication_event_purpose_type cept ON cep.communication_event_purpose_type_id = cept.id
                WHERE cep.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": new_id})
            logger.info(f"Created communication_event_purpose: id={new_id}")
            return CommunicationEventPurposeOut(**result)
        except Exception as e:
            logger.error(f"Error creating communication_event_purpose: {str(e)}")
            raise

async def get_communication_event_purpose(communication_event_purpose_id: int) -> Optional[CommunicationEventPurposeOut]:
    query = """
        SELECT cep.id, cep.communication_event_id, cep.communication_event_purpose_type_id,
               ce.note AS communication_event_note,
               cept.description AS communication_event_purpose_type_description
        FROM communication_event_purpose cep
        JOIN communication_event ce ON cep.communication_event_id = ce.id
        JOIN communication_event_purpose_type cept ON cep.communication_event_purpose_type_id = cept.id
        WHERE cep.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": communication_event_purpose_id})
    if not result:
        logger.warning(f"Communication_event_purpose not found: id={communication_event_purpose_id}")
        return None
    logger.info(f"Retrieved communication_event_purpose: id={result['id']}")
    return CommunicationEventPurposeOut(**result)

async def get_all_communication_event_purposes() -> List[CommunicationEventPurposeOut]:
    query = """
        SELECT cep.id, cep.communication_event_id, cep.communication_event_purpose_type_id,
               ce.note AS communication_event_note,
               cept.description AS communication_event_purpose_type_description
        FROM communication_event_purpose cep
        JOIN communication_event ce ON cep.communication_event_id = ce.id
        JOIN communication_event_purpose_type cept ON cep.communication_event_purpose_type_id = cept.id
        ORDER BY cep.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} communication_event_purposes")
    return [CommunicationEventPurposeOut(**result) for result in results]

async def get_communication_event_purposes_by_communication_event_id(communication_event_id: int) -> List[CommunicationEventPurposeOut]:
    query = """
        SELECT cep.id, cep.communication_event_id, cep.communication_event_purpose_type_id,
               ce.note AS communication_event_note,
               cept.description AS communication_event_purpose_type_description
        FROM communication_event_purpose cep
        JOIN communication_event ce ON cep.communication_event_id = ce.id
        JOIN communication_event_purpose_type cept ON cep.communication_event_purpose_type_id = cept.id
        WHERE cep.communication_event_id = :communication_event_id
        ORDER BY cep.id DESC
    """
    results = await database.fetch_all(query=query, values={"communication_event_id": communication_event_id})
    logger.info(f"Retrieved {len(results)} communication_event_purposes for communication_event_id={communication_event_id}")
    return [CommunicationEventPurposeOut(**result) for result in results]

async def update_communication_event_purpose(communication_event_purpose_id: int, communication_event_purpose: CommunicationEventPurposeUpdate) -> Optional[CommunicationEventPurposeOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE communication_event_purpose
                SET communication_event_id = COALESCE(:communication_event_id, communication_event_id),
                    communication_event_purpose_type_id = COALESCE(:communication_event_purpose_type_id, communication_event_purpose_type_id)
                WHERE id = :id
                RETURNING id, communication_event_id, communication_event_purpose_type_id
            """
            result = await database.fetch_one(query=query, values={
                "communication_event_id": communication_event_purpose.communication_event_id,
                "communication_event_purpose_type_id": communication_event_purpose.communication_event_purpose_type_id,
                "id": communication_event_purpose_id
            })
            if not result:
                logger.warning(f"Communication_event_purpose not found for update: id={communication_event_purpose_id}")
                return None

            query_fetch = """
                SELECT cep.id, cep.communication_event_id, cep.communication_event_purpose_type_id,
                       ce.note AS communication_event_note,
                       cept.description AS communication_event_purpose_type_description
                FROM communication_event_purpose cep
                JOIN communication_event ce ON cep.communication_event_id = ce.id
                JOIN communication_event_purpose_type cept ON cep.communication_event_purpose_type_id = cept.id
                WHERE cep.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": communication_event_purpose_id})
            logger.info(f"Updated communication_event_purpose: id={communication_event_purpose_id}")
            return CommunicationEventPurposeOut(**result)
        except Exception as e:
            logger.error(f"Error updating communication_event_purpose: {str(e)}")
            raise

async def delete_communication_event_purpose(communication_event_purpose_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM communication_event_purpose
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": communication_event_purpose_id})
            if not result:
                logger.warning(f"Communication_event_purpose not found for deletion: id={communication_event_purpose_id}")
                return False
            logger.info(f"Deleted communication_event_purpose: id={communication_event_purpose_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting communication_event_purpose: {str(e)}")
            raise