from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.corporation import CorporationCreate, CorporationUpdate, CorporationOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_corporation(corporation: CorporationCreate) -> Optional[CorporationOut]:
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
                "name_en": corporation.name_en,
                "name_th": corporation.name_th
            })

            # 3. Insert into legal_organization
            query_legal = """
                INSERT INTO legal_organization (id, federal_tax_id_number)
                VALUES (:id, :federal_tax_id_number)
                RETURNING id
            """
            await database.fetch_one(query=query_legal, values={
                "id": party_id,
                "federal_tax_id_number": corporation.federal_tax_id_number
            })

            # 4. Insert into corporation
            query_corporation = """
                INSERT INTO corporation (id)
                VALUES (:id)
                RETURNING id
            """
            result = await database.fetch_one(query=query_corporation, values={"id": party_id})
            logger.info(f"สร้าง corporation: id={result['id']}")
            return CorporationOut(
                id=result['id'],
                name_en=corporation.name_en,
                name_th=corporation.name_th,
                federal_tax_id_number=corporation.federal_tax_id_number
            )
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการสร้าง corporation: {str(e)}")
            raise

async def get_corporation(corporation_id: int) -> Optional[CorporationOut]:
    query = """
        SELECT c.id, o.name_en, o.name_th, lo.federal_tax_id_number
        FROM corporation c
        JOIN legal_organization lo ON c.id = lo.id
        JOIN organization o ON lo.id = o.id
        JOIN party p ON o.id = p.id
        WHERE c.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": corporation_id})
    if not result:
        logger.warning(f"ไม่พบ corporation: id={corporation_id}")
        return None
    logger.info(f"ดึงข้อมูล corporation: id={result['id']}")
    return CorporationOut(**result)

async def get_all_corporations() -> List[CorporationOut]:
    query = """
        SELECT c.id, o.name_en, o.name_th, lo.federal_tax_id_number
        FROM corporation c
        JOIN legal_organization lo ON c.id = lo.id
        JOIN organization o ON lo.id = o.id
        JOIN party p ON o.id = p.id
        ORDER BY c.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"ดึงข้อมูล {len(results)} corporations")
    return [CorporationOut(**result) for result in results]

async def update_corporation(corporation_id: int, corporation: CorporationUpdate) -> Optional[CorporationOut]:
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
                "name_en": corporation.name_en,
                "name_th": corporation.name_th,
                "id": corporation_id
            })
            if not org_result:
                logger.warning(f"ไม่พบ corporation สำหรับอัปเดต: id={corporation_id}")
                return None

            # Update legal_organization
            query_legal = """
                UPDATE legal_organization
                SET federal_tax_id_number = COALESCE(:federal_tax_id_number, federal_tax_id_number)
                WHERE id = :id
                RETURNING id, federal_tax_id_number
            """
            legal_result = await database.fetch_one(query=query_legal, values={
                "federal_tax_id_number": corporation.federal_tax_id_number,
                "id": corporation_id
            })

            # Fetch updated data
            query_fetch = """
                SELECT c.id, o.name_en, o.name_th, lo.federal_tax_id_number
                FROM corporation c
                JOIN legal_organization lo ON c.id = lo.id
                JOIN organization o ON lo.id = o.id
                WHERE c.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": corporation_id})
            logger.info(f"อัปเดต corporation: id={result['id']}")
            return CorporationOut(**result)
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการอัปเดต corporation: {str(e)}")
            raise

async def delete_corporation(corporation_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from corporation
            query_corporation = """
                DELETE FROM corporation WHERE id = :id
                RETURNING id
            """
            corporation_result = await database.fetch_one(query=query_corporation, values={"id": corporation_id})
            if not corporation_result:
                logger.warning(f"ไม่พบ corporation สำหรับลบ: id={corporation_id}")
                return False

            # Delete from legal_organization
            query_legal = """
                DELETE FROM legal_organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_legal, values={"id": corporation_id})

            # Delete from organization
            query_organization = """
                DELETE FROM organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={"id": corporation_id})

            # Delete from party
            query_party = """
                DELETE FROM party WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_party, values={"id": corporation_id})

            logger.info(f"ลบ corporation: id={corporation_id}")
            return True
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการลบ corporation: {str(e)}")
            raise