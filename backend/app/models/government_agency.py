from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.government_agency import GovernmentAgencyCreate, GovernmentAgencyUpdate, GovernmentAgencyOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_government_agency(government_agency: GovernmentAgencyCreate) -> Optional[GovernmentAgencyOut]:
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
                "name_en": government_agency.name_en,
                "name_th": government_agency.name_th
            })

            # 3. Insert into legal_organization
            query_legal = """
                INSERT INTO legal_organization (id, federal_tax_id_number)
                VALUES (:id, :federal_tax_id_number)
                RETURNING id
            """
            await database.fetch_one(query=query_legal, values={
                "id": party_id,
                "federal_tax_id_number": government_agency.federal_tax_id_number
            })

            # 4. Insert into government_agency
            query_government = """
                INSERT INTO government_agency (id)
                VALUES (:id)
                RETURNING id
            """
            result = await database.fetch_one(query=query_government, values={"id": party_id})
            logger.info(f"สร้าง government agency: id={result['id']}")
            return GovernmentAgencyOut(
                id=result['id'],
                name_en=government_agency.name_en,
                name_th=government_agency.name_th,
                federal_tax_id_number=government_agency.federal_tax_id_number
            )
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการสร้าง government agency: {str(e)}")
            raise

async def get_government_agency(government_agency_id: int) -> Optional[GovernmentAgencyOut]:
    query = """
        SELECT ga.id, o.name_en, o.name_th, lo.federal_tax_id_number
        FROM government_agency ga
        JOIN legal_organization lo ON ga.id = lo.id
        JOIN organization o ON lo.id = o.id
        JOIN party p ON o.id = p.id
        WHERE ga.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": government_agency_id})
    if not result:
        logger.warning(f"ไม่พบ government agency: id={government_agency_id}")
        return None
    logger.info(f"ดึงข้อมูล government agency: id={result['id']}")
    return GovernmentAgencyOut(**result)

async def get_all_government_agencies() -> List[GovernmentAgencyOut]:
    query = """
        SELECT ga.id, o.name_en, o.name_th, lo.federal_tax_id_number
        FROM government_agency ga
        JOIN legal_organization lo ON ga.id = lo.id
        JOIN organization o ON lo.id = o.id
        JOIN party p ON o.id = p.id
        ORDER BY ga.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"ดึงข้อมูล {len(results)} government agencies")
    return [GovernmentAgencyOut(**result) for result in results]

async def update_government_agency(government_agency_id: int, government_agency: GovernmentAgencyUpdate) -> Optional[GovernmentAgencyOut]:
    async with database.transaction():
        try:
            # Update organization
            query_organization = """
                UPDATE organization
                SET name_en = COALESCE(:name_en, name_en),
                    name_th = COALESCE(:name_th, name_th)
                WHERE id = :id
                RETURNING id
            """
            org_result = await database.fetch_one(query=query_organization, values={
                "name_en": government_agency.name_en,
                "name_th": government_agency.name_th,
                "id": government_agency_id
            })
            if not org_result:
                logger.warning(f"ไม่พบ government agency สำหรับอัปเดต: id={government_agency_id}")
                return None

            # Update legal_organization
            query_legal = """
                UPDATE legal_organization
                SET federal_tax_id_number = COALESCE(:federal_tax_id_number, federal_tax_id_number)
                WHERE id = :id
                RETURNING id, federal_tax_id_number
            """
            legal_result = await database.fetch_one(query=query_legal, values={
                "federal_tax_id_number": government_agency.federal_tax_id_number,
                "id": government_agency_id
            })

            # Fetch updated data
            query_fetch = """
                SELECT ga.id, o.name_en, o.name_th, lo.federal_tax_id_number
                FROM government_agency ga
                JOIN legal_organization lo ON ga.id = lo.id
                JOIN organization o ON lo.id = o.id
                WHERE ga.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": government_agency_id})
            logger.info(f"อัปเดต government agency: id={result['id']}")
            return GovernmentAgencyOut(**result)
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการอัปเดต government agency: {str(e)}")
            raise

async def delete_government_agency(government_agency_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from government_agency
            query_government = """
                DELETE FROM government_agency WHERE id = :id
                RETURNING id
            """
            government_result = await database.fetch_one(query=query_government, values={"id": government_agency_id})
            if not government_result:
                logger.warning(f"ไม่พบ government agency สำหรับลบ: id={government_agency_id}")
                return False

            # Delete from legal_organization
            query_legal = """
                DELETE FROM legal_organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_legal, values={"id": government_agency_id})

            # Delete from organization
            query_organization = """
                DELETE FROM organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={"id": government_agency_id})

            # Delete from party
            query_party = """
                DELETE FROM party WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_party, values={"id": government_agency_id})

            logger.info(f"ลบ government agency: id={government_agency_id}")
            return True
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการลบ government agency: {str(e)}")
            raise