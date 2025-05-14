from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.informal_organization import InformalOrganizationCreate, InformalOrganizationUpdate, InformalOrganizationOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_informal_organization(informal_organization: InformalOrganizationCreate) -> Optional[InformalOrganizationOut]:
    async with database.transaction():
        try:
            # 1. Insert into party
            query_party = """
                INSERT INTO party (id)
                VALUES (DEFAULT)
                RETURNING id
            """
            party_result = await database.fetch_one(query=query_party)
            party_id = party_result["id"]

            # 2. Insert into organization
            query_organization = """
                INSERT INTO organization (id, name_en, name_th)
                VALUES (:id, :name_en, :name_th)
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={
                "id": party_id,
                "name_en": informal_organization.name_en,
                "name_th": informal_organization.name_th
            })

            # 3. Insert into informal_organization
            query_informal = """
                INSERT INTO informal_organization (id)
                VALUES (:id)
                RETURNING id
            """
            result = await database.fetch_one(query=query_informal, values={"id": party_id})
            logger.info(f"Created informal organization: id={result['id']}")
            return InformalOrganizationOut(
                id=result['id'],
                name_en=informal_organization.name_en,
                name_th=informal_organization.name_th
            )
        except Exception as e:
            logger.error(f"Error creating informal organization: {str(e)}")
            raise

async def get_informal_organization(informal_organization_id: int) -> Optional[InformalOrganizationOut]:
    query = """
        SELECT io.id, o.name_en, o.name_th
        FROM informal_organization io
        JOIN organization o ON io.id = o.id
        JOIN party p ON o.id = p.id
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
        SELECT io.id, o.name_en, o.name_th
        FROM informal_organization io
        JOIN organization o ON io.id = o.id
        JOIN party p ON o.id = p.id
        ORDER BY io.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} informal organizations")
    return [InformalOrganizationOut(**result) for result in results]

async def update_informal_organization(informal_organization_id: int, informal_organization: InformalOrganizationUpdate) -> Optional[InformalOrganizationOut]:
    async with database.transaction():
        try:
            # Update organization
            query_organization = """
                UPDATE organization
                SET name_en = COALESCE(:name_en, name_en),
                    name_th = COALESCE(:name_th, name_th)
                WHERE id = :id
                RETURNING id, name_en, name_th
            """
            result = await database.fetch_one(query=query_organization, values={
                "name_en": informal_organization.name_en,
                "name_th": informal_organization.name_th,
                "id": informal_organization_id
            })
            if not result:
                logger.warning(f"Informal organization not found for update: id={informal_organization_id}")
                return None
            logger.info(f"Updated informal organization: id={result['id']}")
            return InformalOrganizationOut(**result)
        except Exception as e:
            logger.error(f"Error updating informal organization: {str(e)}")
            raise

async def delete_informal_organization(informal_organization_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from informal_organization
            query_informal = """
                DELETE FROM informal_organization WHERE id = :id
                RETURNING id
            """
            informal_result = await database.fetch_one(query=query_informal, values={"id": informal_organization_id})
            if not informal_result:
                logger.warning(f"Informal organization not found for deletion: id={informal_organization_id}")
                return False

            # Delete from organization
            query_organization = """
                DELETE FROM organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={"id": informal_organization_id})

            # Delete from party
            query_party = """
                DELETE FROM party WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_party, values={"id": informal_organization_id})

            logger.info(f"Deleted informal organization: id={informal_organization_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting informal organization: {str(e)}")
            raise