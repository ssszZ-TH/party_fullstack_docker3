from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.informal_organization import InformalOrganizationCreate, InformalOrganizationUpdate, InformalOrganizationOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_informal_organization(informal_organization: InformalOrganizationCreate) -> Optional[InformalOrganizationOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO informal_organization (id)
                VALUES (:organization_id)
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={
                "organization_id": informal_organization.organization_id
            })
            logger.info(f"Created informal organization: id={result['id']}")
            return InformalOrganizationOut(id=result['id'], organization_id=informal_organization.organization_id)
        except Exception as e:
            logger.error(f"Error creating informal organization: {str(e)}")
            raise

async def get_informal_organization(informal_organization_id: int) -> Optional[InformalOrganizationOut]:
    query = """
        SELECT io.id, o.id as organization_id
        FROM informal_organization io
        JOIN organization o ON io.id = o.id
        WHERE io.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": informal_organization_id})
    if not result:
        logger.warning(f"Informal organization not found: id={informal_organization_id}")
        return None
    logger.info(f"Retrieved informal organization: id={result['id']}")
    return InformalOrganizationOut(**result)

async def get_all_informal_organizations() -> List[InformalOrganizationOut]:
    query = """
        SELECT io.id, o.id as organization_id
        FROM informal_organization io
        JOIN organization o ON io.id = o.id
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} informal organizations")
    return [InformalOrganizationOut(**result) for result in results]

async def update_informal_organization(informal_organization_id: int, informal_organization: InformalOrganizationUpdate) -> Optional[InformalOrganizationOut]:
    query = """
        SELECT id, id as organization_id
        FROM informal_organization
        WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": informal_organization_id})
    if not result:
        logger.warning(f"Informal organization not found for update: id={informal_organization_id}")
        return None
    logger.info(f"Updated informal organization: id={result['id']}")
    return InformalOrganizationOut(**result)

async def delete_informal_organization(informal_organization_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM informal_organization WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": informal_organization_id})
            if not result:
                logger.warning(f"Informal organization not found for deletion: id={informal_organization_id}")
                return False
            logger.info(f"Deleted informal organization: id={informal_organization_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting informal organization: {str(e)}")
            raise