from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.communication_event import CommunicationEventCreate, CommunicationEventUpdate, CommunicationEventOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_communication_event(communication_event: CommunicationEventCreate) -> Optional[CommunicationEventOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO communication_event (datetime_start, datetime_end, note, contact_mechanism_type_id, 
                                               communication_event_status_type_id, party_relationship_id)
                VALUES (:datetime_start, :datetime_end, :note, :contact_mechanism_type_id, 
                        :communication_event_status_type_id, :party_relationship_id)
                RETURNING id, datetime_start, datetime_end, note, contact_mechanism_type_id, 
                          communication_event_status_type_id, party_relationship_id
            """
            result = await database.fetch_one(query=query, values={
                "datetime_start": communication_event.datetime_start,
                "datetime_end": communication_event.datetime_end,
                "note": communication_event.note,
                "contact_mechanism_type_id": communication_event.contact_mechanism_type_id,
                "communication_event_status_type_id": communication_event.communication_event_status_type_id,
                "party_relationship_id": communication_event.party_relationship_id
            })
            new_id = result["id"]

            query_fetch = """
                SELECT ce.id, ce.datetime_start, ce.datetime_end, ce.note, ce.contact_mechanism_type_id, 
                       ce.communication_event_status_type_id, ce.party_relationship_id,
                       cmt.description AS contact_mechanism_type_description,
                       cest.description AS communication_event_status_type_description,
                       pr.comment AS party_relationship_comment
                FROM communication_event ce
                JOIN contact_mechanism_type cmt ON ce.contact_mechanism_type_id = cmt.id
                JOIN communication_event_status_type cest ON ce.communication_event_status_type_id = cest.id
                JOIN party_relationship pr ON ce.party_relationship_id = pr.id
                WHERE ce.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": new_id})
            logger.info(f"Created communication_event: id={new_id}")
            return CommunicationEventOut(**result)
        except Exception as e:
            logger.error(f"Error creating communication_event: {str(e)}")
            raise

async def get_communication_event(communication_event_id: int) -> Optional[CommunicationEventOut]:
    query = """
        SELECT ce.id, ce.datetime_start, ce.datetime_end, ce.note, ce.contact_mechanism_type_id, 
               ce.communication_event_status_type_id, ce.party_relationship_id,
               cmt.description AS contact_mechanism_type_description,
               cest.description AS communication_event_status_type_description,
               pr.comment AS party_relationship_comment
        FROM communication_event ce
        JOIN contact_mechanism_type cmt ON ce.contact_mechanism_type_id = cmt.id
        JOIN communication_event_status_type cest ON ce.communication_event_status_type_id = cest.id
        JOIN party_relationship pr ON ce.party_relationship_id = pr.id
        WHERE ce.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": communication_event_id})
    if not result:
        logger.warning(f"Communication_event not found: id={communication_event_id}")
        return None
    logger.info(f"Retrieved communication_event: id={result['id']}")
    return CommunicationEventOut(**result)

async def get_all_communication_events() -> List[CommunicationEventOut]:
    query = """
        SELECT ce.id, ce.datetime_start, ce.datetime_end, ce.note, ce.contact_mechanism_type_id, 
               ce.communication_event_status_type_id, ce.party_relationship_id,
               cmt.description AS contact_mechanism_type_description,
               cest.description AS communication_event_status_type_description,
               pr.comment AS party_relationship_comment
        FROM communication_event ce
        JOIN contact_mechanism_type cmt ON ce.contact_mechanism_type_id = cmt.id
        JOIN communication_event_status_type cest ON ce.communication_event_status_type_id = cest.id
        JOIN party_relationship pr ON ce.party_relationship_id = pr.id
        ORDER BY ce.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} communication_events")
    return [CommunicationEventOut(**result) for result in results]

async def get_communication_events_by_party_relationship_id(party_relationship_id: int) -> List[CommunicationEventOut]:
    query = """
        SELECT ce.id, ce.datetime_start, ce.datetime_end, ce.note, ce.contact_mechanism_type_id, 
               ce.communication_event_status_type_id, ce.party_relationship_id,
               cmt.description AS contact_mechanism_type_description,
               cest.description AS communication_event_status_type_description,
               pr.comment AS party_relationship_comment
        FROM communication_event ce
        JOIN contact_mechanism_type cmt ON ce.contact_mechanism_type_id = cmt.id
        JOIN communication_event_status_type cest ON ce.communication_event_status_type_id = cest.id
        JOIN party_relationship pr ON ce.party_relationship_id = pr.id
        WHERE ce.party_relationship_id = :party_relationship_id
        ORDER BY ce.datetime_start DESC, ce.id DESC
    """
    results = await database.fetch_all(query=query, values={"party_relationship_id": party_relationship_id})
    logger.info(f"Retrieved {len(results)} communication_events for party_relationship_id={party_relationship_id}")
    return [CommunicationEventOut(**result) for result in results]

async def update_communication_event(communication_event_id: int, communication_event: CommunicationEventUpdate) -> Optional[CommunicationEventOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE communication_event
                SET datetime_start = COALESCE(:datetime_start, datetime_start),
                    datetime_end = COALESCE(:datetime_end, datetime_end),
                    note = COALESCE(:note, note),
                    contact_mechanism_type_id = COALESCE(:contact_mechanism_type_id, contact_mechanism_type_id),
                    communication_event_status_type_id = COALESCE(:communication_event_status_type_id, communication_event_status_type_id),
                    party_relationship_id = COALESCE(:party_relationship_id, party_relationship_id)
                WHERE id = :id
                RETURNING id, datetime_start, datetime_end, note, contact_mechanism_type_id, 
                          communication_event_status_type_id, party_relationship_id
            """
            result = await database.fetch_one(query=query, values={
                "datetime_start": communication_event.datetime_start,
                "datetime_end": communication_event.datetime_end,
                "note": communication_event.note,
                "contact_mechanism_type_id": communication_event.contact_mechanism_type_id,
                "communication_event_status_type_id": communication_event.communication_event_status_type_id,
                "party_relationship_id": communication_event.party_relationship_id,
                "id": communication_event_id
            })
            if not result:
                logger.warning(f"Communication_event not found for update: id={communication_event_id}")
                return None

            query_fetch = """
                SELECT ce.id, ce.datetime_start, ce.datetime_end, ce.note, ce.contact_mechanism_type_id, 
                       ce.communication_event_status_type_id, ce.party_relationship_id,
                       cmt.description AS contact_mechanism_type_description,
                       cest.description AS communication_event_status_type_description,
                       pr.comment AS party_relationship_comment
                FROM communication_event ce
                JOIN contact_mechanism_type cmt ON ce.contact_mechanism_type_id = cmt.id
                JOIN communication_event_status_type cest ON ce.communication_event_status_type_id = cest.id
                JOIN party_relationship pr ON ce.party_relationship_id = pr.id
                WHERE ce.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": communication_event_id})
            logger.info(f"Updated communication_event: id={communication_event_id}")
            return CommunicationEventOut(**result)
        except Exception as e:
            logger.error(f"Error updating communication_event: {str(e)}")
            raise

async def delete_communication_event(communication_event_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM communication_event
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": communication_event_id})
            if not result:
                logger.warning(f"Communication_event not found for deletion: id={communication_event_id}")
                return False
            logger.info(f"Deleted communication_event: id={communication_event_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting communication_event: {str(e)}")
            raise