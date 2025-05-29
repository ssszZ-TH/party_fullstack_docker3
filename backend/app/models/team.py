from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.team import TeamCreate, TeamUpdate, TeamOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_team(team: TeamCreate) -> Optional[TeamOut]:
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
                "name_en": team.name_en,
                "name_th": team.name_th
            })

            # 3. Insert into informal_organization
            query_informal = """
                INSERT INTO informal_organization (id)
                VALUES (:id)
                RETURNING id
            """
            await database.fetch_one(query=query_informal, values={"id": party_id})

            # 4. Insert into team
            query_team = """
                INSERT INTO team (id)
                VALUES (:id)
                RETURNING id
            """
            result = await database.fetch_one(query=query_team, values={"id": party_id})
            logger.info(f"สร้าง team: id={result['id']}")
            return TeamOut(
                id=result['id'],
                name_en=team.name_en,
                name_th=team.name_th
            )
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการสร้าง team: {str(e)}")
            raise

async def get_team(team_id: int) -> Optional[TeamOut]:
    query = """
        SELECT t.id, o.name_en, o.name_th
        FROM team t
        JOIN informal_organization io ON t.id = io.id
        JOIN organization o ON io.id = o.id
        JOIN party p ON o.id = p.id
        WHERE t.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": team_id})
    if not result:
        logger.warning(f"ไม่พบ team: id={team_id}")
        return None
    logger.info(f"ดึงข้อมูล team: id={result['id']}")
    return TeamOut(**result)

async def get_all_teams() -> List[TeamOut]:
    query = """
        SELECT t.id, o.name_en, o.name_th
        FROM team t
        JOIN informal_organization io ON t.id = io.id
        JOIN organization o ON io.id = o.id
        JOIN party p ON o.id = p.id
        ORDER BY t.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"ดึงข้อมูล {len(results)} teams")
    return [TeamOut(**result) for result in results]

async def update_team(team_id: int, team: TeamUpdate) -> Optional[TeamOut]:
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
                "name_en": team.name_en,
                "name_th": team.name_th,
                "id": team_id
            })
            if not result:
                logger.warning(f"ไม่พบ team สำหรับอัปเดต: id={team_id}")
                return None
            logger.info(f"อัปเดต team: id={result['id']}")
            return TeamOut(**result)
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการอัปเดต team: {str(e)}")
            raise

async def delete_team(team_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from team
            query_team = """
                DELETE FROM team WHERE id = :id
                RETURNING id
            """
            team_result = await database.fetch_one(query=query_team, values={"id": team_id})
            if not team_result:
                logger.warning(f"ไม่พบ team สำหรับลบ: id={team_id}")
                return False

            # Delete from informal_organization
            query_informal = """
                DELETE FROM informal_organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_informal, values={"id": team_id})

            # Delete from organization
            query_organization = """
                DELETE FROM organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={"id": team_id})

            # Delete from party
            query_party = """
                DELETE FROM party WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_party, values={"id": team_id})

            logger.info(f"ลบ team: id={team_id}")
            return True
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการลบ team: {str(e)}")
            raise