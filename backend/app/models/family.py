from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.family import FamilyCreate, FamilyUpdate, FamilyOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_family(family: FamilyCreate) -> Optional[FamilyOut]:
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
                "name_en": family.name_en,
                "name_th": family.name_th
            })

            # 3. Insert into informal_organization
            query_informal = """
                INSERT INTO informal_organization (id)
                VALUES (:id)
                RETURNING id
            """
            await database.fetch_one(query=query_informal, values={"id": party_id})

            # 4. Insert into family
            query_family = """
                INSERT INTO family (id)
                VALUES (:id)
                RETURNING id
            """
            result = await database.fetch_one(query=query_family, values={"id": party_id})
            logger.info(f"สร้าง family: id={result['id']}")
            return FamilyOut(
                id=result['id'],
                name_en=family.name_en,
                name_th=family.name_th
            )
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการสร้าง family: {str(e)}")
            raise

async def get_family(family_id: int) -> Optional[FamilyOut]:
    query = """
        SELECT f.id, o.name_en, o.name_th
        FROM family f
        JOIN informal_organization io ON f.id = io.id
        JOIN organization o ON io.id = o.id
        JOIN party p ON o.id = p.id
        WHERE f.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": family_id})
    if not result:
        logger.warning(f"ไม่พบ family: id={family_id}")
        return None
    logger.info(f"ดึงข้อมูล family: id={result['id']}")
    return FamilyOut(**result)

async def get_all_families() -> List[FamilyOut]:
    query = """
        SELECT f.id, o.name_en, o.name_th
        FROM family f
        JOIN informal_organization io ON f.id = io.id
        JOIN organization o ON io.id = o.id
        JOIN party p ON o.id = p.id
        ORDER BY f.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"ดึงข้อมูล {len(results)} families")
    return [FamilyOut(**result) for result in results]

async def update_family(family_id: int, family: FamilyUpdate) -> Optional[FamilyOut]:
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
                "name_en": family.name_en,
                "name_th": family.name_th,
                "id": family_id
            })
            if not result:
                logger.warning(f"ไม่พบ family สำหรับอัปเดต: id={family_id}")
                return None
            logger.info(f"อัปเดต family: id={result['id']}")
            return FamilyOut(**result)
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการอัปเดต family: {str(e)}")
            raise

async def delete_family(family_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from family
            query_family = """
                DELETE FROM family WHERE id = :id
                RETURNING id
            """
            family_result = await database.fetch_one(query=query_family, values={"id": family_id})
            if not family_result:
                logger.warning(f"ไม่พบ family สำหรับลบ: id={family_id}")
                return False

            # Delete from informal_organization
            query_informal = """
                DELETE FROM informal_organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_informal, values={"id": family_id})

            # Delete from organization
            query_organization = """
                DELETE FROM organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={"id": family_id})

            # Delete from party
            query_party = """
                DELETE FROM party WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_party, values={"id": family_id})

            logger.info(f"ลบ family: id={family_id}")
            return True
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการลบ family: {str(e)}")
            raise