from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.passport import PassportCreate, PassportUpdate, PassportOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_passport(passport: PassportCreate) -> Optional[PassportOut]:
    query = """
        SELECT id FROM passport 
        WHERE passportnumber = :passportnumber AND citizenship_id = :citizenship_id
    """
    existing = await database.fetch_one(query=query, values={
        "passportnumber": passport.passportnumber,
        "citizenship_id": passport.citizenship_id
    })
    if existing:
        logger.warning(f"Passport already exists: passportnumber={passport.passportnumber}, citizenship_id={passport.citizenship_id}")
        return None

    query = """
        INSERT INTO passport (passportnumber, fromdate, thrudate, citizenship_id)
        VALUES (:passportnumber, :fromdate, :thrudate, :citizenship_id)
        RETURNING id, passportnumber, fromdate, thrudate, citizenship_id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "passportnumber": passport.passportnumber,
            "fromdate": passport.fromdate,
            "thrudate": passport.thrudate,
            "citizenship_id": passport.citizenship_id
        })
        logger.info(f"Created passport: id={result['id']}, passportnumber={result['passportnumber']}")
        return PassportOut(**result)
    except Exception as e:
        logger.error(f"Error creating passport: {str(e)}")
        raise

async def get_passport(passport_id: int) -> Optional[PassportOut]:
    query = """
        SELECT id, passportnumber, fromdate, thrudate, citizenship_id 
        FROM passport WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": passport_id})
    if not result:
        logger.warning(f"Passport not found: id={passport_id}")
        return None
    logger.info(f"Retrieved passport: id={result['id']}, passportnumber={result['passportnumber']}")
    return PassportOut(**result)

async def get_all_passports() -> List[PassportOut]:
    query = """
        SELECT id, passportnumber, fromdate, thrudate, citizenship_id 
        FROM passport
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} passports")
    return [PassportOut(**result) for result in results]

async def get_passports_by_citizenship(citizenship_id: int) -> List[PassportOut]:
    query = """
        SELECT id, passportnumber, fromdate, thrudate, citizenship_id 
        FROM passport 
        WHERE citizenship_id = :citizenship_id
    """
    results = await database.fetch_all(query=query, values={"citizenship_id": citizenship_id})
    logger.info(f"Retrieved {len(results)} passports for citizenship_id={citizenship_id}")
    return [PassportOut(**result) for result in results]

async def update_passport(passport_id: int, passport: PassportUpdate) -> Optional[PassportOut]:
    if passport.passportnumber or passport.citizenship_id:
        query = """
            SELECT id FROM passport 
            WHERE passportnumber = COALESCE(:passportnumber, passportnumber) 
            AND citizenship_id = COALESCE(:citizenship_id, citizenship_id)
            AND id != :id
        """
        existing = await database.fetch_one(query=query, values={
            "passportnumber": passport.passportnumber,
            "citizenship_id": passport.citizenship_id,
            "id": passport_id
        })
        if existing:
            logger.warning(f"Passport already exists: passportnumber={passport.passportnumber}, citizenship_id={passport.citizenship_id}")
            return None

    query = """
        UPDATE passport
        SET passportnumber = COALESCE(:passportnumber, passportnumber),
            fromdate = COALESCE(:fromdate, fromdate),
            thrudate = COALESCE(:thrudate, thrudate),
            citizenship_id = COALESCE(:citizenship_id, citizenship_id)
        WHERE id = :id
        RETURNING id, passportnumber, fromdate, thrudate, citizenship_id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "passportnumber": passport.passportnumber,
            "fromdate": passport.fromdate,
            "thrudate": passport.thrudate,
            "citizenship_id": passport.citizenship_id,
            "id": passport_id
        })
        if not result:
            logger.warning(f"Passport not found for update: id={passport_id}")
            return None
        logger.info(f"Updated passport: id={result['id']}, passportnumber={result['passportnumber']}")
        return PassportOut(**result)
    except Exception as e:
        logger.error(f"Error updating passport: {str(e)}")
        raise

async def delete_passport(passport_id: int) -> bool:
    query = """
        DELETE FROM passport WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": passport_id})
    if not result:
        logger.warning(f"Passport not found for deletion: id={passport_id}")
        return False
    logger.info(f"Deleted passport: id={passport_id}")
    return True