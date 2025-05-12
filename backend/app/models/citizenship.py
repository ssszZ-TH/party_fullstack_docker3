from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.citizenship import CitizenshipCreate, CitizenshipUpdate, CitizenshipOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_citizenship(citizenship: CitizenshipCreate) -> Optional[CitizenshipOut]:
    query = """
        SELECT id FROM citizenship 
        WHERE person_id = :person_id AND country_id = :country_id 
        AND fromdate = :fromdate AND (thrudate = :thrudate OR (thrudate IS NULL AND :thrudate IS NULL))
    """
    existing = await database.fetch_one(query=query, values={
        "person_id": citizenship.person_id,
        "country_id": citizenship.country_id,
        "fromdate": citizenship.fromdate,
        "thrudate": citizenship.thrudate
    })
    if existing:
        logger.warning(f"Citizenship already exists for person_id={citizenship.person_id}, country_id={citizenship.country_id}")
        return None

    query = """
        INSERT INTO citizenship (fromdate, thrudate, person_id, country_id)
        VALUES (:fromdate, :thrudate, :person_id, :country_id)
        RETURNING id, fromdate, thrudate, person_id, country_id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "fromdate": citizenship.fromdate,
            "thrudate": citizenship.thrudate,
            "person_id": citizenship.person_id,
            "country_id": citizenship.country_id
        })
        logger.info(f"Created citizenship: id={result['id']}, person_id={result['person_id']}")
        return CitizenshipOut(**result)
    except Exception as e:
        logger.error(f"Error creating citizenship: {str(e)}")
        raise

async def get_citizenship(citizenship_id: int) -> Optional[CitizenshipOut]:
    query = """
        SELECT id, fromdate, thrudate, person_id, country_id 
        FROM citizenship WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": citizenship_id})
    if not result:
        logger.warning(f"Citizenship not found: id={citizenship_id}")
        return None
    logger.info(f"Retrieved citizenship: id={result['id']}, person_id={result['person_id']}")
    return CitizenshipOut(**result)

async def get_all_citizenships() -> List[CitizenshipOut]:
    query = """
        SELECT id, fromdate, thrudate, person_id, country_id 
        FROM citizenship
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} citizenships")
    return [CitizenshipOut(**result) for result in results]

async def update_citizenship(citizenship_id: int, citizenship: CitizenshipUpdate) -> Optional[CitizenshipOut]:
    if any([citizenship.fromdate, citizenship.thrudate, citizenship.person_id, citizenship.country_id]):
        query = """
            SELECT id FROM citizenship 
            WHERE person_id = COALESCE(:person_id, person_id) 
            AND country_id = COALESCE(:country_id, country_id)
            AND fromdate = COALESCE(:fromdate, fromdate)
            AND (thrudate = COALESCE(:thrudate, thrudate) OR (thrudate IS NULL AND :thrudate IS NULL))
            AND id != :id
        """
        existing = await database.fetch_one(query=query, values={
            "person_id": citizenship.person_id,
            "country_id": citizenship.country_id,
            "fromdate": citizenship.fromdate,
            "thrudate": citizenship.thrudate,
            "id": citizenship_id
        })
        if existing:
            logger.warning(f"Citizenship already exists for person_id={citizenship.person_id}, country_id={citizenship.country_id}")
            return None

    query = """
        UPDATE citizenship
        SET fromdate = COALESCE(:fromdate, fromdate),
            thrudate = COALESCE(:thrudate, thrudate),
            person_id = COALESCE(:person_id, person_id),
            country_id = COALESCE(:country_id, country_id)
        WHERE id = :id
        RETURNING id, fromdate, thrudate, person_id, country_id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "fromdate": citizenship.fromdate,
            "thrudate": citizenship.thrudate,
            "person_id": citizenship.person_id,
            "country_id": citizenship.country_id,
            "id": citizenship_id
        })
        if not result:
            logger.warning(f"Citizenship not found for update: id={citizenship_id}")
            return None
        logger.info(f"Updated citizenship: id={result['id']}, person_id={result['person_id']}")
        return CitizenshipOut(**result)
    except Exception as e:
        logger.error(f"Error updating citizenship: {str(e)}")
        raise

async def delete_citizenship(citizenship_id: int) -> bool:
    query = """
        SELECT id FROM passport WHERE citizenship_id = :id LIMIT 1
    """
    referenced = await database.fetch_one(query=query, values={"id": citizenship_id})
    if referenced:
        logger.warning(f"Cannot delete citizenship: id={citizenship_id}, referenced in passport")
        return False

    query = """
        DELETE FROM citizenship WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": citizenship_id})
    if not result:
        logger.warning(f"Citizenship not found for deletion: id={citizenship_id}")
        return False
    logger.info(f"Deleted citizenship: id={citizenship_id}")
    return True