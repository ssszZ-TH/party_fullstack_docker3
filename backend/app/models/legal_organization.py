from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.legal_organization import LegalOrganizationCreate, LegalOrganizationUpdate, LegalOrganizationOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_legal_organization(legal_organization: LegalOrganizationCreate) -> Optional[LegalOrganizationOut]:
    query_check = """
        SELECT id FROM legal_organization WHERE federal_tax_id_number = :federal_tax_id_number
    """
    existing = await database.fetch_one(query=query_check, values={"federal_tax_id_number": legal_organization.federal_tax_id_number})
    if existing:
        logger.warning(f"Legal organization with federal_tax_id_number '{legal_organization.federal_tax_id_number}' already exists")
        return None

    async with database.transaction():
        try:
            query = """
                INSERT INTO legal_organization (id, federal_tax_id_number)
                VALUES (:organization_id, :federal_tax_id_number)
                RETURNING id, federal_tax_id_number
            """
            result = await database.fetch_one(query=query, values={
                "organization_id": legal_organization.organization_id,
                "federal_tax_id_number": legal_organization.federal_tax_id_number
            })
            logger.info(f"Created legal organization: id={result['id']}")
            return LegalOrganizationOut(id=result['id'], federal_tax_id_number=result['federal_tax_id_number'], organization_id=legal_organization.organization_id)
        except Exception as e:
            logger.error(f"Error creating legal organization: {str(e)}")
            raise

async def get_legal_organization(legal_organization_id: int) -> Optional[LegalOrganizationOut]:
    query = """
        SELECT lo.id, lo.federal_tax_id_number, o.id as organization_id
        FROM legal_organization lo
        JOIN organization o ON lo.id = o.id
        WHERE lo.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": legal_organization_id})
    if not result:
        logger.warning(f"Legal organization not found: id={legal_organization_id}")
        return None
    logger.info(f"Retrieved legal organization: id={result['id']}")
    return LegalOrganizationOut(**result)

async def get_all_legal_organizations() -> List[LegalOrganizationOut]:
    query = """
        SELECT lo.id, lo.federal_tax_id_number, o.id as organization_id
        FROM legal_organization lo
        JOIN organization o ON lo.id = o.id
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} legal organizations")
    return [LegalOrganizationOut(**result) for result in results]

async def update_legal_organization(legal_organization_id: int, legal_organization: LegalOrganizationUpdate) -> Optional[LegalOrganizationOut]:
    if legal_organization.federal_tax_id_number:
        query_check = """
            SELECT id FROM legal_organization 
            WHERE federal_tax_id_number = :federal_tax_id_number AND id != :id
        """
        existing = await database.fetch_one(query=query_check, values={
            "federal_tax_id_number": legal_organization.federal_tax_id_number,
            "id": legal_organization_id
        })
        if existing:
            logger.warning(f"Legal organization with federal_tax_id_number '{legal_organization.federal_tax_id_number}' already exists")
            return None

    query = """
        UPDATE legal_organization
        SET federal_tax_id_number = COALESCE(:federal_tax_id_number, federal_tax_id_number)
        WHERE id = :id
        RETURNING id, federal_tax_id_number
    """
    try:
        result = await database.fetch_one(query=query, values={
            "federal_tax_id_number": legal_organization.federal_tax_id_number,
            "id": legal_organization_id
        })
        if not result:
            logger.warning(f"Legal organization not found for update: id={legal_organization_id}")
            return None
        logger.info(f"Updated legal organization: id={result['id']}")
        return LegalOrganizationOut(id=result['id'], federal_tax_id_number=result['federal_tax_id_number'], organization_id=legal_organization_id)
    except Exception as e:
        logger.error(f"Error updating legal organization: {str(e)}")
        raise

async def delete_legal_organization(legal_organization_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM legal_organization WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": legal_organization_id})
            if not result:
                logger.warning(f"Legal organization not found for deletion: id={legal_organization_id}")
                return False
            logger.info(f"Deleted legal organization: id={legal_organization_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting legal organization: {str(e)}")
            raise