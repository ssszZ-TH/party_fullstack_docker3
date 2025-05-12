from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.person_name import PersonNameCreate, PersonNameUpdate, PersonNameOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_person_name(person_name: PersonNameCreate) -> Optional[PersonNameOut]:
    query = """
        SELECT id FROM personname 
        WHERE person_id = :person_id AND personnametype_id = :personnametype_id 
        AND name = :name AND fromdate = :fromdate 
        AND (thrudate = :thrudate OR (thrudate IS NULL AND :thrudate IS NULL))
    """
    existing = await database.fetch_one(query=query, values={
        "person_id": person_name.person_id,
        "personnametype_id": person_name.personnametype_id,
        "name": person_name.name,
        "fromdate": person_name.fromdate,
        "thrudate": person_name.thrudate
    })
    if existing:
        logger.warning(f"Person name already exists: person_id={person_name.person_id}, name={person_name.name}")
        return None

    query = """
        INSERT INTO personname (fromdate, thrudate, person_id, personnametype_id, name)
        VALUES (:fromdate, :thrudate, :person_id, :personnametype_id, :name)
        RETURNING id, fromdate, thrudate, person_id, personnametype_id, name
    """
    try:
        result = await database.fetch_one(query=query, values={
            "fromdate": person_name.fromdate,
            "thrudate": person_name.thrudate,
            "person_id": person_name.person_id,
            "personnametype_id": person_name.personnametype_id,
            "name": person_name.name
        })
        logger.info(f"Created person name: id={result['id']}, name={result['name']}")
        return PersonNameOut(**result)
    except Exception as e:
        logger.error(f"Error creating person name: {str(e)}")
        raise

async def get_person_name(person_name_id: int) -> Optional[PersonNameOut]:
    query = """
        SELECT id, fromdate, thrudate, person_id, personnametype_id, name 
        FROM personname WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": person_name_id})
    if not result:
        logger.warning(f"Person name not found: id={person_name_id}")
        return None
    logger.info(f"Retrieved person name: id={result['id']}, name={result['name']}")
    return PersonNameOut(**result)

async def get_all_person_names() -> List[PersonNameOut]:
    query = """
        SELECT id, fromdate, thrudate, person_id, personnametype_id, name 
        FROM personname
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} person names")
    return [PersonNameOut(**result) for result in results]

async def update_person_name(person_name_id: int, person_name: PersonNameUpdate) -> Optional[PersonNameOut]:
    if any([person_name.fromdate, person_name.thrudate, person_name.person_id, person_name.personnametype_id, person_name.name]):
        query = """
            SELECT id FROM personname 
            WHERE person_id = COALESCE(:person_id, person_id)
            AND personnametype_id = COALESCE(:personnametype_id, personnametype_id)
            AND name = COALESCE(:name, name)
            AND fromdate = COALESCE(:fromdate, fromdate)
            AND (thrudate = COALESCE(:thrudate, thrudate) OR (thrudate IS NULL AND :thrudate IS NULL))
            AND id != :id
        """
        existing = await database.fetch_one(query=query, values={
            "person_id": person_name.person_id,
            "personnametype_id": person_name.personnametype_id,
            "name": person_name.name,
            "fromdate": person_name.fromdate,
            "thrudate": person_name.thrudate,
            "id": person_name_id
        })
        if existing:
            logger.warning(f"Person name already exists: person_id={person_name.person_id}, name={person_name.name}")
            return None

    query = """
        UPDATE personname
        SET fromdate = COALESCE(:fromdate, fromdate),
            thrudate = COALESCE(:thrudate, thrudate),
            person_id = COALESCE(:person_id, person_id),
            personnametype_id = COALESCE(:personnametype_id, personnametype_id),
            name = COALESCE(:name, name)
        WHERE id = :id
        RETURNING id, fromdate, thrudate, person_id, personnametype_id, name
    """
    try:
        result = await database.fetch_one(query=query, values={
            "fromdate": person_name.fromdate,
            "thrudate": person_name.thrudate,
            "person_id": person_name.person_id,
            "personnametype_id": person_name.personnametype_id,
            "name": person_name.name,
            "id": person_name_id
        })
        if not result:
            logger.warning(f"Person name not found for update: id={person_name_id}")
            return None
        logger.info(f"Updated person name: id={result['id']}, name={result['name']}")
        return PersonNameOut(**result)
    except Exception as e:
        logger.error(f"Error updating person name: {str(e)}")
        raise

async def delete_person_name(person_name_id: int) -> bool:
    query = """
        DELETE FROM personname WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": person_name_id})
    if not result:
        logger.warning(f"Person name not found for deletion: id={person_name_id}")
        return False
    logger.info(f"Deleted person name: id={person_name_id}")
    return True