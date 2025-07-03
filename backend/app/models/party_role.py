from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.party_role import PartyRoleCreate, PartyRoleUpdate, PartyRoleOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_party_role(party_role: PartyRoleCreate) -> Optional[PartyRoleOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO party_role (party_id, role_type_id, fromdate, thrudate)
                VALUES (:party_id, :role_type_id, :fromdate, :thrudate)
                RETURNING id, party_id, role_type_id, fromdate, thrudate
            """
            result = await database.fetch_one(query=query, values={
                "party_id": party_role.party_id,
                "role_type_id": party_role.role_type_id,
                "fromdate": party_role.fromdate,
                "thrudate": party_role.thrudate
            })
            new_id = result["id"]

            query_fetch = """
                SELECT pr.id, pr.party_id, pr.role_type_id, pr.fromdate, pr.thrudate,
                       CASE 
                           WHEN p.id IS NOT NULL THEN 'person'
                           WHEN o.id IS NOT NULL THEN 'organization'
                       END AS type,
                       o.name_en, o.name_th, p.personal_id_number, p.comment,
                       rt.description AS role_type_description
                FROM party_role pr
                LEFT JOIN person p ON pr.party_id = p.id
                LEFT JOIN organization o ON pr.party_id = o.id
                LEFT JOIN role_type rt ON pr.role_type_id = rt.id
                WHERE pr.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": new_id})
            logger.info(f"Created party_role: id={new_id}")
            return PartyRoleOut(**result)
        except Exception as e:
            logger.error(f"Error creating party_role: {str(e)}")
            raise

async def get_party_role(party_role_id: int) -> Optional[PartyRoleOut]:
    query = """
        SELECT pr.id, pr.party_id, pr.role_type_id, pr.fromdate, pr.thrudate,
               CASE 
                   WHEN p.id IS NOT NULL THEN 'person'
                   WHEN o.id IS NOT NULL THEN 'organization'
               END AS type,
               o.name_en, o.name_th, p.personal_id_number, p.comment,
               rt.description AS role_type_description
        FROM party_role pr
        LEFT JOIN person p ON pr.party_id = p.id
        LEFT JOIN organization o ON pr.party_id = o.id
        LEFT JOIN role_type rt ON pr.role_type_id = rt.id
        WHERE pr.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": party_role_id})
    if not result:
        logger.warning(f"Party_role not found: id={party_role_id}")
        return None
    logger.info(f"Retrieved party_role: id={result['id']}")
    return PartyRoleOut(**result)

async def get_all_party_roles() -> List[PartyRoleOut]:
    query = """
        SELECT pr.id, pr.party_id, pr.role_type_id, pr.fromdate, pr.thrudate,
               CASE 
                   WHEN p.id IS NOT NULL THEN 'person'
                   WHEN o.id IS NOT NULL THEN 'organization'
               END AS type,
               o.name_en, o.name_th, p.personal_id_number, p.comment,
               rt.description AS role_type_description
        FROM party_role pr
        LEFT JOIN person p ON pr.party_id = p.id
        LEFT JOIN organization o ON pr.party_id = o.id
        LEFT JOIN role_type rt ON pr.role_type_id = rt.id
        ORDER BY pr.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} party_roles")
    return [PartyRoleOut(**result) for result in results]

async def get_party_roles_by_party_id(party_id: int) -> List[PartyRoleOut]:
    query = """
        SELECT pr.id, pr.party_id, pr.role_type_id, pr.fromdate, pr.thrudate,
               CASE 
                   WHEN p.id IS NOT NULL THEN 'person'
                   WHEN o.id IS NOT NULL THEN 'organization'
               END AS type,
               o.name_en, o.name_th, p.personal_id_number, p.comment,
               rt.description AS role_type_description
        FROM party_role pr
        LEFT JOIN person p ON pr.party_id = p.id
        LEFT JOIN organization o ON pr.party_id = o.id
        LEFT JOIN role_type rt ON pr.role_type_id = rt.id
        WHERE pr.party_id = :party_id
        ORDER BY pr.fromdate DESC, pr.id DESC
    """
    results = await database.fetch_all(query=query, values={"party_id": party_id})
    logger.info(f"Retrieved {len(results)} party_roles for party_id={party_id}")
    return [PartyRoleOut(**result) for result in results]

async def update_party_role(party_role_id: int, party_role: PartyRoleUpdate) -> Optional[PartyRoleOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE party_role
                SET party_id = COALESCE(:party_id, party_id),
                    role_type_id = COALESCE(:role_type_id, role_type_id),
                    fromdate = COALESCE(:fromdate, fromdate),
                    thrudate = COALESCE(:thrudate, thrudate)
                WHERE id = :id
                RETURNING id, party_id, role_type_id, fromdate, thrudate
            """
            result = await database.fetch_one(query=query, values={
                "party_id": party_role.party_id,
                "role_type_id": party_role.role_type_id,
                "fromdate": party_role.fromdate,
                "thrudate": party_role.thrudate,
                "id": party_role_id
            })
            if not result:
                logger.warning(f"Party_role not found for update: id={party_role_id}")
                return None

            query_fetch = """
                SELECT pr.id, pr.party_id, pr.role_type_id, pr.fromdate, pr.thrudate,
                       CASE 
                           WHEN p.id IS NOT NULL THEN 'person'
                           WHEN o.id IS NOT NULL THEN 'organization'
                       END AS type,
                       o.name_en, o.name_th, p.personal_id_number, p.comment,
                       rt.description AS role_type_description
                FROM party_role pr
                LEFT JOIN person p ON pr.party_id = p.id
                LEFT JOIN organization o ON pr.party_id = o.id
                LEFT JOIN role_type rt ON pr.role_type_id = rt.id
                WHERE pr.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": party_role_id})
            logger.info(f"Updated party_role: id={party_role_id}")
            return PartyRoleOut(**result)
        except Exception as e:
            logger.error(f"Error updating party_role: {str(e)}")
            raise

async def delete_party_role(party_role_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM party_role
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": party_role_id})
            if not result:
                logger.warning(f"Party_role not found for deletion: id={party_role_id}")
                return False
            logger.info(f"Deleted party_role: id={party_role_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting party_role: {str(e)}")
            raise