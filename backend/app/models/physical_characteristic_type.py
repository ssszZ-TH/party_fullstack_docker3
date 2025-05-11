from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.physical_characteristic_type import PhysicalCharacteristicTypeCreate, PhysicalCharacteristicTypeUpdate, PhysicalCharacteristicTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_physical_characteristic_type(physical_characteristic_type: PhysicalCharacteristicTypeCreate) -> Optional[PhysicalCharacteristicTypeOut]:
    query = """
        SELECT id, description FROM physicalcharacteristictype WHERE description = :description
    """
    existing = await database.fetch_one(query=query, values={"description": physical_characteristic_type.description})
    if existing:
        logger.warning(f"Physical characteristic type with description '{physical_characteristic_type.description}' already exists")
        return None

    query = """
        INSERT INTO physicalcharacteristictype (description)
        VALUES (:description)
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": physical_characteristic_type.description})
        logger.info(f"Created physical characteristic type: id={result['id']}, description={result['description']}")
        return PhysicalCharacteristicTypeOut(**result)
    except Exception as e:
        logger.error(f"Error creating physical characteristic type: {str(e)}")
        raise

async def get_physical_characteristic_type(physical_characteristic_type_id: int) -> Optional[PhysicalCharacteristicTypeOut]:
    query = """
        SELECT id, description FROM physicalcharacteristictype WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": physical_characteristic_type_id})
    if not result:
        logger.warning(f"Physical characteristic type not found: id={physical_characteristic_type_id}")
        return None
    logger.info(f"Retrieved physical characteristic type: id={result['id']}, description={result['description']}")
    return PhysicalCharacteristicTypeOut(**result)

async def get_all_physical_characteristic_types() -> List[PhysicalCharacteristicTypeOut]:
    query = """
        SELECT id, description FROM physicalcharacteristictype
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} physical characteristic types")
    return [PhysicalCharacteristicTypeOut(**result) for result in results]

async def update_physical_characteristic_type(physical_characteristic_type_id: int, physical_characteristic_type: PhysicalCharacteristicTypeUpdate) -> Optional[PhysicalCharacteristicTypeOut]:
    if physical_characteristic_type.description:
        query = """
            SELECT id, description FROM physicalcharacteristictype WHERE description = :description AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"description": physical_characteristic_type.description, "id": physical_characteristic_type_id})
        if existing:
            logger.warning(f"Physical characteristic type with description '{physical_characteristic_type.description}' already exists")
            return None

    query = """
        UPDATE physicalcharacteristictype
        SET description = COALESCE(:description, description)
        WHERE id = :id
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": physical_characteristic_type.description, "id": physical_characteristic_type_id})
        if not result:
            logger.warning(f"Physical characteristic type not found for update: id={physical_characteristic_type_id}")
            return None
        logger.info(f"Updated physical characteristic type: id={result['id']}, description={result['description']}")
        return PhysicalCharacteristicTypeOut(**result)
    except Exception as e:
        logger.error(f"Error updating physical characteristic type: {str(e)}")
        raise

async def delete_physical_characteristic_type(physical_characteristic_type_id: int) -> bool:
    # Check if the type is referenced in physicalcharacteristic table
    query = """
        SELECT id FROM physicalcharacteristic WHERE physicalcharacteristictype_id = :id LIMIT 1
    """
    referenced = await database.fetch_one(query=query, values={"id": physical_characteristic_type_id})
    if referenced:
        logger.warning(f"Cannot delete physical characteristic type: id={physical_characteristic_type_id}, referenced in physicalcharacteristic")
        return False

    query = """
        DELETE FROM physicalcharacteristictype WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": physical_characteristic_type_id})
    if not result:
        logger.warning(f"Physical characteristic type not found for deletion: id={physical_characteristic_type_id}")
        return False
    logger.info(f"Deleted physical characteristic type: id={physical_characteristic_type_id}")
    return True