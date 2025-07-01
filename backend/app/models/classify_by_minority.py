from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.classify_by_minority import ClassifyByMinorityCreate, ClassifyByMinorityUpdate, ClassifyByMinorityOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_classify_by_minority(classify_by_minority: ClassifyByMinorityCreate) -> Optional[ClassifyByMinorityOut]:
    async with database.transaction():
        try:
            query_party_cl = """
                INSERT INTO party_classification (fromdate, thrudate, party_id, party_type_id)
                VALUES (:fromdate, :thrudate, :party_id, :party_type_id)
                RETURNING id
            """
            party_cl_result = await database.fetch_one(query=query_party_cl, values={
                "fromdate": classify_by_minority.fromdate,
                "thrudate": classify_by_minority.thrudate,
                "party_id": classify_by_minority.party_id,
                "party_type_id": classify_by_minority.party_type_id
            })
            new_id = party_cl_result["id"]

            query_org_cl = """
                INSERT INTO organization_classification (id)
                VALUES (:id)
            """
            await database.execute(query=query_org_cl, values={"id": new_id})

            query_minority = """
                INSERT INTO classify_by_minority (id, minority_type_id)
                VALUES (:id, :minority_type_id)
                RETURNING id
            """
            await database.execute(query=query_minority, values={
                "id": new_id,
                "minority_type_id": classify_by_minority.minority_type_id
            })

            query_fetch = """
                SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
                       cm.minority_type_id, mt.name_en, mt.name_th
                FROM classify_by_minority cm
                JOIN organization_classification oc ON cm.id = oc.id
                JOIN party_classification pc ON cm.id = pc.id
                JOIN minority_type mt ON cm.minority_type_id = mt.id
                WHERE cm.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": new_id})
            logger.info(f"Created classify_by_minority: id={new_id}")
            return ClassifyByMinorityOut(**result)
        except Exception as e:
            logger.error(f"Error creating classify_by_minority: {str(e)}")
            raise

async def get_classify_by_minority(classify_by_minority_id: int) -> Optional[ClassifyByMinorityOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               cm.minority_type_id, mt.name_en, mt.name_th
        FROM classify_by_minority cm
        JOIN organization_classification oc ON cm.id = oc.id
        JOIN party_classification pc ON cm.id = pc.id
        JOIN minority_type mt ON cm.minority_type_id = mt.id
        WHERE cm.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": classify_by_minority_id})
    if not result:
        logger.warning(f"Classify_by_minority not found: id={classify_by_minority_id}")
        return None
    logger.info(f"Retrieved classify_by_minority: id={result['id']}")
    return ClassifyByMinorityOut(**result)

async def get_all_classify_by_minorities() -> List[ClassifyByMinorityOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               cm.minority_type_id, mt.name_en, mt.name_th
        FROM classify_by_minority cm
        JOIN organization_classification oc ON cm.id = oc.id
        JOIN party_classification pc ON cm.id = pc.id
        JOIN minority_type mt ON cm.minority_type_id = mt.id
        ORDER BY pc.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} classify_by_minorities")
    return [ClassifyByMinorityOut(**result) for result in results]

async def get_classify_by_minorities_by_organization(organization_id: int) -> List[ClassifyByMinorityOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               cm.minority_type_id, mt.name_en, mt.name_th
        FROM classify_by_minority cm
        JOIN organization_classification oc ON cm.id = oc.id
        JOIN party_classification pc ON cm.id = pc.id
        JOIN minority_type mt ON cm.minority_type_id = mt.id
        WHERE pc.party_id = :organization_id
        ORDER BY pc.fromdate DESC, pc.id DESC
    """
    results = await database.fetch_all(query=query, values={"organization_id": organization_id})
    logger.info(f"Retrieved {len(results)} classify_by_minorities for organization_id={organization_id}")
    return [ClassifyByMinorityOut(**result) for result in results]

async def update_classify_by_minority(classify_by_minority_id: int, classify_by_minority: ClassifyByMinorityUpdate) -> Optional[ClassifyByMinorityOut]:
    async with database.transaction():
        try:
            query_party_cl = """
                UPDATE party_classification
                SET fromdate = COALESCE(:fromdate, fromdate),
                    thrudate = COALESCE(:thrudate, thrudate),
                    party_id = COALESCE(:party_id, party_id),
                    party_type_id = COALESCE(:party_type_id, party_type_id)
                WHERE id = :id
            """
            await database.execute(query=query_party_cl, values={
                "fromdate": classify_by_minority.fromdate,
                "thrudate": classify_by_minority.thrudate,
                "party_id": classify_by_minority.party_id,
                "party_type_id": classify_by_minority.party_type_id,
                "id": classify_by_minority_id
            })

            query_minority = """
                UPDATE classify_by_minority
                SET minority_type_id = COALESCE(:minority_type_id, minority_type_id)
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query_minority, values={
                "minority_type_id": classify_by_minority.minority_type_id,
                "id": classify_by_minority_id
            })
            if not result:
                logger.warning(f"Classify_by_minority not found for update: id={classify_by_minority_id}")
                return None

            query_fetch = """
                SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
                       cm.minority_type_id, mt.name_en, mt.name_th
                FROM classify_by_minority cm
                JOIN organization_classification oc ON cm.id = oc.id
                JOIN party_classification pc ON cm.id = pc.id
                JOIN minority_type mt ON cm.minority_type_id = mt.id
                WHERE cm.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": classify_by_minority_id})
            logger.info(f"Updated classify_by_minority: id={classify_by_minority_id}")
            return ClassifyByMinorityOut(**result)
        except Exception as e:
            logger.error(f"Error updating classify_by_minority: {str(e)}")
            raise

async def delete_classify_by_minority(classify_by_minority_id: int) -> bool:
    async with database.transaction():
        try:
            query_minority = """
                DELETE FROM classify_by_minority WHERE id = :id
                RETURNING id
            """
            minority_result = await database.fetch_one(query=query_minority, values={"id": classify_by_minority_id})
            if not minority_result:
                logger.warning(f"Classify_by_minority not found for deletion: id={classify_by_minority_id}")
                return False

            query_org_cl = """
                DELETE FROM organization_classification WHERE id = :id
            """
            await database.execute(query=query_org_cl, values={"id": classify_by_minority_id})

            query_party_cl = """
                DELETE FROM party_classification WHERE id = :id
            """
            await database.execute(query=query_party_cl, values={"id": classify_by_minority_id})

            logger.info(f"Deleted classify_by_minority: id={classify_by_minority_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting classify_by_minority: {str(e)}")
            raise