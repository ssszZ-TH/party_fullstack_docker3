from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.physical_characteristic import PhysicalCharacteristicCreate, PhysicalCharacteristicUpdate, PhysicalCharacteristicOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_physical_characteristic(physical_characteristic: PhysicalCharacteristicCreate) -> Optional[PhysicalCharacteristicOut]:
    query = """
        SELECT id FROM physicalcharacteristic 
        WHERE person_id = :person_id AND physicalcharacteristictype_id = :physicalcharacteristictype_id 
        AND val = :val AND fromdate = :fromdate 
        AND (thrudate = :thrudate OR (thrudate IS NULL AND :thrudate IS NULL))
    """
    existing = await database.fetch_one(query=query, values={
        "person_id": physical_characteristic.person_id,
        "physicalcharacteristictype_id": physical_characteristic.physicalcharacteristictype_id,
        "val": physical_characteristic.val,
        "fromdate": physical_characteristic.fromdate,
        "thrudate": physical_characteristic.thrudate
    })
    if existing:
        logger.warning(f"Physical characteristic already exists: person_id={physical_characteristic.person_id}, type_id={physical_characteristic.physicalcharacteristictype_id}")
        return None

    query = """
        INSERT INTO physicalcharacteristic (fromdate, thrudate, val, person_id, physicalcharacteristictype_id)
        VALUES (:fromdate, :thrudate, :val, :person_id, :physicalcharacteristictype_id)
        RETURNING id, fromdate, thrudate, val, person_id, physicalcharacteristictype_id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "fromdate": physical_characteristic.fromdate,
            "thrudate": physical_characteristic.thrudate,
            "val": physical_characteristic.val,
            "person_id": physical_characteristic.person_id,
            "physicalcharacteristictype_id": physical_characteristic.physicalcharacteristictype_id
        })
        logger.info(f"Created physical characteristic: id={result['id']}, person_id={result['person_id']}")
        return PhysicalCharacteristicOut(**result)
    except Exception as e:
        logger.error(f"Error creating physical characteristic: {str(e)}")
        raise

async def get_physical_characteristic(physical_characteristic_id: int) -> Optional[PhysicalCharacteristicOut]:
    query = """
        SELECT id, fromdate, thrudate, val, person_id, physicalcharacteristictype_id 
        FROM physicalcharacteristic WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": physical_characteristic_id})
    if not result:
        logger.warning(f"Physical characteristic not found: id={physical_characteristic_id}")
        return None
    logger.info(f"Retrieved physical characteristic: id={result['id']}, person_id={result['person_id']}")
    return PhysicalCharacteristicOut(**result)

async def get_all_physical_characteristics() -> List[PhysicalCharacteristicOut]:
    query = """
        SELECT id, fromdate, thrudate, val, person_id, physicalcharacteristictype_id 
        FROM physicalcharacteristic
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} physical characteristics")
    return [PhysicalCharacteristicOut(**result) for result in results]

async def update_physical_characteristic(physical_characteristic_id: int, physical_characteristic: PhysicalCharacteristicUpdate) -> Optional[PhysicalCharacteristicOut]:
    if any([physical_characteristic.fromdate, physical_characteristic.thrudate, physical_characteristic.val, physical_characteristic.person_id, physical_characteristic.physicalcharacteristictype_id]):
        query = """
            SELECT id FROM physicalcharacteristic 
            WHERE person_id = COALESCE(:person_id, person_id)
            AND physicalcharacteristictype_id = COALESCE(:physicalcharacteristictype_id, physicalcharacteristictype_id)
            AND val = COALESCE(:val, val)
            AND fromdate = COALESCE(:fromdate, fromdate)
            AND (thrudate = COALESCE(:thrudate, thrudate) OR (thrudate IS NULL AND :thrudate IS NULL))
            AND id != :id
        """
        existing = await database.fetch_one(query=query, values={
            "person_id": physical_characteristic.person_id,
            "physicalcharacteristictype_id": physical_characteristic.physicalcharacteristictype_id,
            "val": physical_characteristic.val,
            "fromdate": physical_characteristic.fromdate,
            "thrudate": physical_characteristic.thrudate,
            "id": physical_characteristic_id
        })
        if existing:
            logger.warning(f"Physical characteristic already exists: person_id={physical_characteristic.person_id}, type_id={physical_characteristic.physicalcharacteristictype_id}")
            return None

    query = """
        UPDATE physicalcharacteristic
        SET fromdate = COALESCE(:fromdate, fromdate),
            thrudate = COALESCE(:thrudate, thrudate),
            val = COALESCE(:val, val),
            person_id = COALESCE(:person_id, person_id),
            physicalcharacteristictype_id = COALESCE(:physicalcharacteristictype_id, physicalcharacteristictype_id)
        WHERE id = :id
        RETURNING id, fromdate, thrudate, val, person_id, physicalcharacteristictype_id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "fromdate": physical_characteristic.fromdate,
            "thrudate": physical_characteristic.thrudate,
            "val": physical_characteristic.val,
            "person_id": physical_characteristic.person_id,
            "physicalcharacteristictype_id": physical_characteristic.physicalcharacteristictype_id,
            "id": physical_characteristic_id
        })
        if not result:
            logger.warning(f"Physical characteristic not found for update: id={physical_characteristic_id}")
            return None
        logger.info(f"Updated physical characteristic: id={result['id']}, person_id={result['person_id']}")
        return PhysicalCharacteristicOut(**result)
    except Exception as e:
        logger.error(f"Error updating physical characteristic: {str(e)}")
        raise

async def delete_physical_characteristic(physical_characteristic_id: int) -> bool:
    query = """
        DELETE FROM physicalcharacteristic WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": physical_characteristic_id})
    if not result:
        logger.warning(f"Physical characteristic not found for deletion: id={physical_characteristic_id}")
        return False
    logger.info(f"Deleted physical characteristic: id={physical_characteristic_id}")
    return True