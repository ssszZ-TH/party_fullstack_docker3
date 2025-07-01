from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.role_type import RoleTypeCreate, RoleTypeUpdate, RoleTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_role_type(role_type: RoleTypeCreate) -> Optional[RoleTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO role_type (description)
                VALUES (:description)
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={"description": role_type.description})
            logger.info(f"Created role_type: id={result['id']}")
            return RoleTypeOut(**result)
        except Exception as e:
            logger.error(f"Error creating role_type: {str(e)}")
            raise

async def get_role_type(role_type_id: int) -> Optional[RoleTypeOut]:
    query = """
        SELECT id, description
        FROM role_type
        WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": role_type_id})
    if not result:
        logger.warning(f"Role_type not found: id={role_type_id}")
        return None
    logger.info(f"Retrieved role_type: id={result['id']}")
    return RoleTypeOut(**result)

async def get_all_role_types() -> List[RoleTypeOut]:
    query = """
        SELECT id, description
        FROM role_type
        ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} role_types")
    return [RoleTypeOut(**result) for result in results]

async def update_role_type(role_type_id: int, role_type: RoleTypeUpdate) -> Optional[RoleTypeOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE role_type
                SET description = COALESCE(:description, description)
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={
                "description": role_type.description,
                "id": role_type_id
            })
            if not result:
                logger.warning(f"Role_type not found for update: id={role_type_id}")
                return None
            logger.info(f"Updated role_type: id={role_type_id}")
            return RoleTypeOut(**result)
        except Exception as e:
            logger.error(f"Error updating role_type: {str(e)}")
            raise

async def delete_role_type(role_type_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM role_type
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": role_type_id})
            if not result:
                logger.warning(f"Role_type not found for deletion: id={role_type_id}")
                return False
            logger.info(f"Deleted role_type: id={role_type_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting role_type: {str(e)}")
            raise