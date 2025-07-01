from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.contact_mechanism_type import ContactMechanismTypeCreate, ContactMechanismTypeUpdate, ContactMechanismTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_contact_mechanism_type(contact_mechanism_type: ContactMechanismTypeCreate) -> Optional[ContactMechanismTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO contact_mechanism_type (description)
                VALUES (:description)
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={"description": contact_mechanism_type.description})
            logger.info(f"Created contact_mechanism_type: id={result['id']}")
            return ContactMechanismTypeOut(**result)
        except Exception as e:
            logger.error(f"Error creating contact_mechanism_type: {str(e)}")
            raise

async def get_contact_mechanism_type(contact_mechanism_type_id: int) -> Optional[ContactMechanismTypeOut]:
    query = """
        SELECT id, description
        FROM contact_mechanism_type
        WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": contact_mechanism_type_id})
    if not result:
        logger.warning(f"Contact_mechanism_type not found: id={contact_mechanism_type_id}")
        return None
    logger.info(f"Retrieved contact_mechanism_type: id={result['id']}")
    return ContactMechanismTypeOut(**result)

async def get_all_contact_mechanism_types() -> List[ContactMechanismTypeOut]:
    query = """
        SELECT id, description
        FROM contact_mechanism_type
        ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} contact_mechanism_types")
    return [ContactMechanismTypeOut(**result) for result in results]

async def update_contact_mechanism_type(contact_mechanism_type_id: int, contact_mechanism_type: ContactMechanismTypeUpdate) -> Optional[ContactMechanismTypeOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE contact_mechanism_type
                SET description = COALESCE(:description, description)
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={
                "description": contact_mechanism_type.description,
                "id": contact_mechanism_type_id
            })
            if not result:
                logger.warning(f"Contact_mechanism_type not found for update: id={contact_mechanism_type_id}")
                return None
            logger.info(f"Updated contact_mechanism_type: id={contact_mechanism_type_id}")
            return ContactMechanismTypeOut(**result)
        except Exception as e:
            logger.error(f"Error updating contact_mechanism_type: {str(e)}")
            raise

async def delete_contact_mechanism_type(contact_mechanism_type_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM contact_mechanism_type
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": contact_mechanism_type_id})
            if not result:
                logger.warning(f"Contact_mechanism_type not found for deletion: id={contact_mechanism_type_id}")
                return False
            logger.info(f"Deleted contact_mechanism_type: id={contact_mechanism_type_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting contact_mechanism_type: {str(e)}")
            raise