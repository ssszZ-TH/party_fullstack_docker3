from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.other_informal_organization import OtherInformalOrganizationCreate, OtherInformalOrganizationUpdate, OtherInformalOrganizationOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_other_informal_organization(other_informal_organization: OtherInformalOrganizationCreate) -> Optional[OtherInformalOrganizationOut]:
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
                "name_en": other_informal_organization.name_en,
                "name_th": other_informal_organization.name_th
            })

            # 3. Insert into informal_organization
            query_informal = """
                INSERT INTO informal_organization (id)
                VALUES (:id)
                RETURNING id
            """
            await database.fetch_one(query=query_informal, values={"id": party_id})

            # 4. Insert into other_informal_organization
            query_other = """
                INSERT INTO other_informal_organization (id)
                VALUES (:id)
                RETURNING id
            """
            result = await database.fetch_one(query=query_other, values={"id": party_id})
            logger.info(f"สร้าง other informal organization: id={result['id']}")
            return OtherInformalOrganizationOut(
                id=result['id'],
                name_en=other_informal_organization.name_en,
                name_th=other_informal_organization.name_th
            )
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการสร้าง other informal organization: {str(e)}")
            raise

async def get_other_informal_organization(other_informal_organization_id: int) -> Optional[OtherInformalOrganizationOut]:
    query = """
        SELECT oio.id, o.name_en, o.name_th
        FROM other_informal_organization oio
        JOIN informal_organization io ON oio.id = io.id
        JOIN organization o ON io.id = o.id
        JOIN party p ON o.id = p.id
        WHERE oio.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": other_informal_organization_id})
    if not result:
        logger.warning(f"ไม่พบ other informal organization: id={other_informal_organization_id}")
        return None
    logger.info(f"ดึงข้อมูล other informal organization: id={result['id']}")
    return OtherInformalOrganizationOut(**result)

async def get_all_other_informal_organizations() -> List[OtherInformalOrganizationOut]:
    query = """
        SELECT oio.id, o.name_en, o.name_th
        FROM other_informal_organization oio
        JOIN informal_organization io ON oio.id = io.id
        JOIN organization o ON io.id = o.id
        JOIN party p ON o.id = p.id
        ORDER BY oio.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"ดึงข้อมูล {len(results)} other informal organizations")
    return [OtherInformalOrganizationOut(**result) for result in results]

async def update_other_informal_organization(other_informal_organization_id: int, other_informal_organization: OtherInformalOrganizationUpdate) -> Optional[OtherInformalOrganizationOut]:
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
                "name_en": other_informal_organization.name_en,
                "name_th": other_informal_organization.name_th,
                "id": other_informal_organization_id
            })
            if not result:
                logger.warning(f"ไม่พบ other informal organization สำหรับอัปเดต: id={other_informal_organization_id}")
                return None
            logger.info(f"อัปเดต other informal organization: id={result['id']}")
            return OtherInformalOrganizationOut(**result)
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการอัปเดต other informal organization: {str(e)}")
            raise

async def delete_other_informal_organization(other_informal_organization_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from other_informal_organization
            query_other = """
                DELETE FROM other_informal_organization WHERE id = :id
                RETURNING id
            """
            other_result = await database.fetch_one(query=query_other, values={"id": other_informal_organization_id})
            if not other_result:
                logger.warning(f"ไม่พบ other informal organization สำหรับลบ: id={other_informal_organization_id}")
                return False

            # Delete from informal_organization
            query_informal = """
                DELETE FROM informal_organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_informal, values={"id": other_informal_organization_id})

            # Delete from organization
            query_organization = """
                DELETE FROM organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={"id": other_informal_organization_id})

            # Delete from party
            query_party = """
                DELETE FROM party WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_party, values={"id": other_informal_organization_id})

            logger.info(f"ลบ other informal organization: id={other_informal_organization_id}")
            return True
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการลบ other informal organization: {str(e)}")
            raise