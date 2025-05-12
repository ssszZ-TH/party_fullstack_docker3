from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.marital_status import MaritalStatusCreate, MaritalStatusUpdate, MaritalStatusOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_marital_status(marital_status: MaritalStatusCreate) -> Optional[MaritalStatusOut]:
    query = """
        SELECT id FROM maritalstatus 
        WHERE person_id = :person_id AND maritalstatustype_id = :maritalstatustype_id 
        AND fromdate = :fromdate 
        AND (thrudate = :thrudate OR (thrudate IS NULL AND :thrudate IS NULL))
    """
    existing = await database.fetch_one(query=query, values={
        "person_id": marital_status.person_id,
        "maritalstatustype_id": marital_status.maritalstatustype_id,
        "fromdate": marital_status.fromdate,
        "thrudate": marital_status.thrudate
    })
    if existing:
        logger.warning(f"Marital status already exists: person_id={marital_status.person_id}, type_id={marital_status.maritalstatustype_id}")
        return None

    query = """
        INSERT INTO maritalstatus (fromdate, thrudate, person_id, maritalstatustype_id)
        VALUES (:fromdate, :thrudate, :person_id, :maritalstatustype_id)
        RETURNING id, fromdate, thrudate, person_id, maritalstatustype_id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "fromdate": marital_status.fromdate,
            "thrudate": marital_status.thrudate,
            "person_id": marital_status.person_id,
            "maritalstatustype_id": marital_status.maritalstatustype_id
        })
        logger.info(f"Created marital status: id={result['id']}, person_id={result['person_id']}")
        return MaritalStatusOut(**result)
    except Exception as e:
        logger.error(f"Error creating marital status: {str(e)}")
        raise

async def get_marital_status(marital_status_id: int) -> Optional[MaritalStatusOut]:
    query = """
        SELECT id, fromdate, thrudate, person_id, maritalstatustype_id 
        FROM maritalstatus WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": marital_status_id})
    if not result:
        logger.warning(f"Marital status not found: id={marital_status_id}")
        return None
    logger.info(f"Retrieved marital status: id={result['id']}, person_id={result['person_id']}")
    return MaritalStatusOut(**result)

async def get_all_marital_statuses() -> List[MaritalStatusOut]:
    query = """
        SELECT id, fromdate, thrudate, person_id, maritalstatustype_id 
        FROM maritalstatus
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} marital statuses")
    return [MaritalStatusOut(**result) for result in results]

async def update_marital_status(marital_status_id: int, marital_status: MaritalStatusUpdate) -> Optional[MaritalStatusOut]:
    if any([marital_status.fromdate, marital_status.thrudate, marital_status.person_id, marital_status.maritalstatustype_id]):
        query = """
            SELECT id FROM maritalstatus 
            WHERE person_id = COALESCE(:person_id, person_id)
            AND maritalstatustype_id = COALESCE(:maritalstatustype_id, maritalstatustype_id)
            AND fromdate = COALESCE(:fromdate, fromdate)
            AND (thrudate = COALESCE(:thrudate, thrudate) OR (thrudate IS NULL AND :thrudate IS NULL))
            AND id != :id
        """
        existing = await database.fetch_one(query=query, values={
            "person_id": marital_status.person_id,
            "maritalstatustype_id": marital_status.maritalstatustype_id,
            "fromdate": marital_status.fromdate,
            "thrudate": marital_status.thrudate,
            "id": marital_status_id
        })
        if existing:
            logger.warning(f"Marital status already exists: person_id={marital_status.person_id}, type_id={marital_status.maritalstatustype_id}")
            return None

    query = """
        UPDATE maritalstatus
        SET fromdate = COALESCE(:fromdate, fromdate),
            thrudate = COALESCE(:thrudate, thrudate),
            person_id = COALESCE(:person_id, person_id),
            maritalstatustype_id = COALESCE(:maritalstatustype_id, maritalstatustype_id)
        WHERE id = :id
        RETURNING id, fromdate, thrudate, person_id, maritalstatustype_id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "fromdate": marital_status.fromdate,
            "thrudate": marital_status.thrudate,
            "person_id": marital_status.person_id,
            "maritalstatustype_id": marital_status.maritalstatustype_id,
            "id": marital_status_id
        })
        if not result:
            logger.warning(f"Marital status not found for update: id={marital_status_id}")
            return None
        logger.info(f"Updated marital status: id={result['id']}, person_id={result['person_id']}")
        return MaritalStatusOut(**result)
    except Exception as e:
        logger.error(f"Error updating marital status: {str(e)}")
        raise

async def delete_marital_status(marital_status_id: int) -> bool:
    query = """
        DELETE FROM maritalstatus WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": marital_status_id})
    if not result:
        logger.warning(f"Marital status not found for deletion: id={marital_status_id}")
        return False
    logger.info(f"Deleted marital status: id={marital_status_id}")
    return True