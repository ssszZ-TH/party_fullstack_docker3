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
 Going to continue generating the CRUD operations for the remaining tables (`physicalcharacteristictype`, `personnametype`, and `country`) based on the provided schema and the pattern established in the previous responses. I'll ensure each table has schema, model, and controller files with consistent structure, using named parameters for queries, and maintaining the `/v1/` prefix for API endpoints as requested. The code will include validation for unique fields, logging, and admin-only access via JWT.

---

### File: /app/models/physical_characteristic_type.py (continued)
### Part: Model - Database operations for physicalcharacteristictype CRUD
<xaiArtifact artifact_id="aa65e63e-22ee-48f7-aee1-af294bee787b" artifact_version_id="2bf85551-50e4-4895-83aa-f20d41cda007" title="physical_characteristic_type.py" contentType="text/python">
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