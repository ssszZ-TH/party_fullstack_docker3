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
                "name_en": legal_organization.name_en,
                "name_th": legal_organization.name_th
            })

            # 3. Insert into legal_organization
            query_legal = """
                INSERT INTO legal_organization (id, federal_tax_id_number)
                VALUES (:id, :federal_tax_id_number)
                RETURNING id, federal_tax_id_number
            """
            result = await database.fetch_one(query=query_legal, values={
                "id": party_id,
                "federal_tax_id_number": legal_organization.federal_tax_id_number
            })
            logger.info(f"Created legal organization: id={result['id']}")
            return LegalOrganizationOut(
                id=result['id'],
                name_en=legal_organization.name_en,
                name_th=legal_organization.name_th,
                federal_tax_id_number=result['federal_tax_id_number']
            )
        except Exception as e:
            logger.error(f"Error creating legal organization: {str(e)}")
            raise

async def get_legal_organization(legal_organization_id: int) -> Optional[LegalOrganizationOut]:
    query = """
        SELECT lo.id, o.name_en, o.name_th, lo.federal_tax_id_number
        FROM legal_organization lo
        JOIN organization o ON lo.id = o.id
        JOIN party p ON o.id = p.id
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
        SELECT lo.id, o.name_en, o.name_th, lo.federal_tax_id_number
        FROM legal_organization lo
        JOIN organization o ON lo.id = o.id
        JOIN party p ON o.id = p.id
        ORDER BY lo.id ASC
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

    async with database.transaction():
        try:
            # Update organization
            if legal_organization.name_en or legal_organization.name_th:
                query_organization = """
                    UPDATE organization
                    SET name_en = COALESCE(:name_en, name_en),
                        name_th = COALESCE(:name_th, name_th)
                    WHERE id = :id
                    RETURNING name_en, name_th
                """
                org_result = await database.fetch_one(query=query_organization, values={
                    "name_en": legal_organization.name_en,
                    "name_th": legal_organization.name_th,
                    "id": legal_organization_id
                })

            # Update legal_organization
            query_legal = """
                UPDATE legal_organization
                SET federal_tax_id_number = COALESCE(:federal_tax_id_number, federal_tax_id_number)
                WHERE id = :id
                RETURNING id, federal_tax_id_number
            """
            result = await database.fetch_one(query=query_legal, values={
                "federal_tax_id_number": legal_organization.federal_tax_id_number,
                "id": legal_organization_id
            })
            if not result:
                logger.warning(f"Legal organization not found for update: id={legal_organization_id}")
                return None

            # Fetch updated organization data
            query_fetch = """
                SELECT o.name_en, o.name_th
                FROM organization o
                WHERE o.id = :id
            """
            org_data = await database.fetch_one(query=query_fetch, values={"id": legal_organization_id})
            logger.info(f"Updated legal organization: id={result['id']}")
            return LegalOrganizationOut(
                id=result['id'],
                name_en=org_data['name_en'],
                name_th=org_data['name_th'],
                federal_tax_id_number=result['federal_tax_id_number']
            )
        except Exception as e:
            logger.error(f"Error updating legal organization: {str(e)}")
            raise

async def delete_legal_organization(legal_organization_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from legal_organization
            query_legal = """
                DELETE FROM legal_organization WHERE id = :id
                RETURNING id
            """
            legal_result = await database.fetch_one(query=query_legal, values={"id": legal_organization_id})
            if not legal_result:
                logger.warning(f"Legal organization not found for deletion: id={legal_organization_id}")
                return False

            # Delete from organization
            query_organization = """
                DELETE FROM organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={"id": legal_organization_id})

            # Delete from party
            query_party = """
                DELETE FROM party WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_party, values={"id": legal_organization_id})

            logger.info(f"Deleted legal organization: id={legal_organization_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting legal organization: {str(e)}")
            raise