from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.party_relationship import PartyRelationshipCreate, PartyRelationshipUpdate, PartyRelationshipOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_party_relationship(party_relationship: PartyRelationshipCreate) -> Optional[PartyRelationshipOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO party_relationship (from_date, thru_date, comment, from_party_role_id, to_party_role_id, 
                                              party_relationship_type_id, priority_type_id, party_relationship_status_type_id)
                VALUES (:from_date, :thru_date, :comment, :from_party_role_id, :to_party_role_id, 
                        :party_relationship_type_id, :priority_type_id, :party_relationship_status_type_id)
                RETURNING id, from_date, thru_date, comment, from_party_role_id, to_party_role_id, 
                          party_relationship_type_id, priority_type_id, party_relationship_status_type_id
            """
            result = await database.fetch_one(query=query, values={
                "from_date": party_relationship.from_date,
                "thru_date": party_relationship.thru_date,
                "comment": party_relationship.comment,
                "from_party_role_id": party_relationship.from_party_role_id,
                "to_party_role_id": party_relationship.to_party_role_id,
                "party_relationship_type_id": party_relationship.party_relationship_type_id,
                "priority_type_id": party_relationship.priority_type_id,
                "party_relationship_status_type_id": party_relationship.party_relationship_status_type_id
            })
            new_id = result["id"]

            query_fetch = """
                SELECT pr.id, pr.from_date, pr.thru_date, pr.comment, pr.from_party_role_id, pr.to_party_role_id,
                       pr.party_relationship_type_id, pr.priority_type_id, pr.party_relationship_status_type_id,
                       prt.description AS party_relationship_type_description,
                       pt.description AS priority_type_description,
                       prst.description AS party_relationship_status_type_description
                FROM party_relationship pr
                JOIN party_relationship_type prt ON pr.party_relationship_type_id = prt.id
                JOIN priority_type pt ON pr.priority_type_id = pt.id
                JOIN party_relationship_status_type prst ON pr.party_relationship_status_type_id = prst.id
                WHERE pr.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": new_id})
            logger.info(f"Created party_relationship: id={new_id}")
            return PartyRelationshipOut(**result)
        except Exception as e:
            logger.error(f"Error creating party_relationship: {str(e)}")
            raise

async def get_party_relationship(party_relationship_id: int) -> Optional[PartyRelationshipOut]:
    query = """
        SELECT pr.id, pr.from_date, pr.thru_date, pr.comment, pr.from_party_role_id, pr.to_party_role_id,
               pr.party_relationship_type_id, pr.priority_type_id, pr.party_relationship_status_type_id,
               prt.description AS party_relationship_type_description,
               pt.description AS priority_type_description,
               prst.description AS party_relationship_status_type_description
        FROM party_relationship pr
        JOIN party_relationship_type prt ON pr.party_relationship_type_id = prt.id
        JOIN priority_type pt ON pr.priority_type_id = pt.id
        JOIN party_relationship_status_type prst ON pr.party_relationship_status_type_id = prst.id
        WHERE pr.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": party_relationship_id})
    if not result:
        logger.warning(f"Party_relationship not found: id={party_relationship_id}")
        return None
    logger.info(f"Retrieved party_relationship: id={result['id']}")
    return PartyRelationshipOut(**result)

async def get_all_party_relationships() -> List[PartyRelationshipOut]:
    query = """
        SELECT pr.id, pr.from_date, pr.thru_date, pr.comment, pr.from_party_role_id, pr.to_party_role_id,
               pr.party_relationship_type_id, pr.priority_type_id, pr.party_relationship_status_type_id,
               prt.description AS party_relationship_type_description,
               pt.description AS priority_type_description,
               prst.description AS party_relationship_status_type_description
        FROM party_relationship pr
        JOIN party_relationship_type prt ON pr.party_relationship_type_id = prt.id
        JOIN priority_type pt ON pr.priority_type_id = pt.id
        JOIN party_relationship_status_type prst ON pr.party_relationship_status_type_id = prst.id
        ORDER BY pr.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} party_relationships")
    return [PartyRelationshipOut(**result) for result in results]

async def get_party_relationships_by_from_party_role_id(from_party_role_id: int) -> List[PartyRelationshipOut]:
    query = """
        SELECT pr.id, pr.from_date, pr.thru_date, pr.comment, pr.from_party_role_id, pr.to_party_role_id,
               pr.party_relationship_type_id, pr.priority_type_id, pr.party_relationship_status_type_id,
               prt.description AS party_relationship_type_description,
               pt.description AS priority_type_description,
               prst.description AS party_relationship_status_type_description
        FROM party_relationship pr
        JOIN party_relationship_type prt ON pr.party_relationship_type_id = prt.id
        JOIN priority_type pt ON pr.priority_type_id = pt.id
        JOIN party_relationship_status_type prst ON pr.party_relationship_status_type_id = prst.id
        WHERE pr.from_party_role_id = :from_party_role_id
        ORDER BY pr.from_date DESC, pr.id DESC
    """
    results = await database.fetch_all(query=query, values={"from_party_role_id": from_party_role_id})
    logger.info(f"Retrieved {len(results)} party_relationships for from_party_role_id={from_party_role_id}")
    return [PartyRelationshipOut(**result) for result in results]

async def get_party_relationships_by_to_party_role_id(to_party_role_id: int) -> List[PartyRelationshipOut]:
    query = """
        SELECT pr.id, pr.from_date, pr.thru_date, pr.comment, pr.from_party_role_id, pr.to_party_role_id,
               pr.party_relationship_type_id, pr.priority_type_id, pr.party_relationship_status_type_id,
               prt.description AS party_relationship_type_description,
               pt.description AS priority_type_description,
               prst.description AS party_relationship_status_type_description
        FROM party_relationship pr
        JOIN party_relationship_type prt ON pr.party_relationship_type_id = prt.id
        JOIN priority_type pt ON pr.priority_type_id = pt.id
        JOIN party_relationship_status_type prst ON pr.party_relationship_status_type_id = prst.id
        WHERE pr.to_party_role_id = :to_party_role_id
        ORDER BY pr.from_date DESC, pr.id DESC
    """
    results = await database.fetch_all(query=query, values={"to_party_role_id": to_party_role_id})
    logger.info(f"Retrieved {len(results)} party_relationships for to_party_role_id={to_party_role_id}")
    return [PartyRelationshipOut(**result) for result in results]

async def update_party_relationship(party_relationship_id: int, party_relationship: PartyRelationshipUpdate) -> Optional[PartyRelationshipOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE party_relationship
                SET from_date = COALESCE(:from_date, from_date),
                    thru_date = COALESCE(:thru_date, thru_date),
                    comment = COALESCE(:comment, comment),
                    from_party_role_id = COALESCE(:from_party_role_id, from_party_role_id),
                    to_party_role_id = COALESCE(:to_party_role_id, to_party_role_id),
                    party_relationship_type_id = COALESCE(:party_relationship_type_id, party_relationship_type_id),
                    priority_type_id = COALESCE(:priority_type_id, priority_type_id),
                    party_relationship_status_type_id = COALESCE(:party_relationship_status_type_id, party_relationship_status_type_id)
                WHERE id = :id
                RETURNING id, from_date, thru_date, comment, from_party_role_id, to_party_role_id, 
                          party_relationship_type_id, priority_type_id, party_relationship_status_type_id
            """
            result = await database.fetch_one(query=query, values={
                "from_date": party_relationship.from_date,
                "thru_date": party_relationship.thru_date,
                "comment": party_relationship.comment,
                "from_party_role_id": party_relationship.from_party_role_id,
                "to_party_role_id": party_relationship.to_party_role_id,
                "party_relationship_type_id": party_relationship.party_relationship_type_id,
                "priority_type_id": party_relationship.priority_type_id,
                "party_relationship_status_type_id": party_relationship.party_relationship_status_type_id,
                "id": party_relationship_id
            })
            if not result:
                logger.warning(f"Party_relationship not found for update: id={party_relationship_id}")
                return None

            query_fetch = """
                SELECT pr.id, pr.from_date, pr.thru_date, pr.comment, pr.from_party_role_id, pr.to_party_role_id,
                       pr.party_relationship_type_id, pr.priority_type_id, pr.party_relationship_status_type_id,
                       prt.description AS party_relationship_type_description,
                       pt.description AS priority_type_description,
                       prst.description AS party_relationship_status_type_description
                FROM party_relationship pr
                JOIN party_relationship_type prt ON pr.party_relationship_type_id = prt.id
                JOIN priority_type pt ON pr.priority_type_id = pt.id
                JOIN party_relationship_status_type prst ON pr.party_relationship_status_type_id = prst.id
                WHERE pr.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": party_relationship_id})
            logger.info(f"Updated party_relationship: id={party_relationship_id}")
            return PartyRelationshipOut(**result)
        except Exception as e:
            logger.error(f"Error updating party_relationship: {str(e)}")
            raise

async def delete_party_relationship(party_relationship_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM party_relationship
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": party_relationship_id})
            if not result:
                logger.warning(f"Party_relationship not found for deletion: id={party_relationship_id}")
                return False
            logger.info(f"Deleted party_relationship: id={party_relationship_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting party_relationship: {str(e)}")
            raise