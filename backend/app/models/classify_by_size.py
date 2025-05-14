from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.classify_by_size import ClassifyBySizeCreate, ClassifyBySizeUpdate, ClassifyBySizeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_classify_by_size(classify_by_size: ClassifyBySizeCreate) -> Optional[ClassifyBySizeOut]:
    async with database.transaction():
        try:
            # 1. Insert into party_classification
            query_party_cl = """
                INSERT INTO party_classification (fromdate, thrudate, party_id, party_type_id)
                VALUES (:fromdate, :thrudate, :party_id, :party_type_id)
                RETURNING id
            """
            party_cl_result = await database.fetch_one(query=query_party_cl, values={
                "fromdate": classify_by_size.fromdate,
                "thrudate": classify_by_size.thrudate,
                "party_id": classify_by_size.party_id,
                "party_type_id": classify_by_size.party_type_id
            })
            new_id = party_cl_result["id"]

            # 2. Insert into organization_classification
            query_org_cl = """
                INSERT INTO organization_classification (id)
                VALUES (:id)
            """
            await database.execute(query=query_org_cl, values={"id": new_id})

            # 3. Insert into classify_by_size
            query_size = """
                INSERT INTO classify_by_size (id, employee_count_range_id)
                VALUES (:id, :employee_count_range_id)
                RETURNING id
            """
            await database.execute(query=query_size, values={
                "id": new_id,
                "employee_count_range_id": classify_by_size.employee_count_range_id
            })

            # Fetch the complete data
            query_fetch = """
                SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
                       cs.employee_count_range_id, ecr.description
                FROM classify_by_size cs
                JOIN organization_classification oc ON cs.id = oc.id
                JOIN party_classification pc ON cs.id = pc.id
                JOIN employee_count_range ecr ON cs.employee_count_range_id = ecr.id
                WHERE cs.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": new_id})
            logger.info(f"Created classify_by_size: id={new_id}")
            return ClassifyBySizeOut(**result)
        except Exception as e:
            logger.error(f"Error creating classify_by_size: {str(e)}")
            raise

async def get_classify_by_size(classify_by_size_id: int) -> Optional[ClassifyBySizeOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               cs.employee_count_range_id, ecr.description
        FROM classify_by_size cs
        JOIN organization_classification oc ON cs.id = oc.id
        JOIN party_classification pc ON cs.id = pc.id
        JOIN employee_count_range ecr ON cs.employee_count_range_id = ecr.id
        WHERE cs.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": classify_by_size_id})
    if not result:
        logger.warning(f"Classify_by_size not found: id={classify_by_size_id}")
        return None
    logger.info(f"Retrieved classify_by_size: id={result['id']}")
    return ClassifyBySizeOut(**result)

async def get_all_classify_by_sizes() -> List[ClassifyBySizeOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               cs.employee_count_range_id, ecr.description
        FROM classify_by_size cs
        JOIN organization_classification oc ON cs.id = oc.id
        JOIN party_classification pc ON cs.id = pc.id
        JOIN employee_count_range ecr ON cs.employee_count_range_id = ecr.id
        ORDER BY pc.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} classify_by_sizes")
    return [ClassifyBySizeOut(**result) for result in results]

async def update_classify_by_size(classify_by_size_id: int, classify_by_size: ClassifyBySizeUpdate) -> Optional[ClassifyBySizeOut]:
    async with database.transaction():
        try:
            # Update party_classification
            query_party_cl = """
                UPDATE party_classification
                SET fromdate = COALESCE(:fromdate, fromdate),
                    thrudate = COALESCE(:thrudate, thrudate),
                    party_id = COALESCE(:party_id, party_id),
                    party_type_id = COALESCE(:party_type_id, party_type_id)
                WHERE id = :id
            """
            await database.execute(query=query_party_cl, values={
                "fromdate": classify_by_size.fromdate,
                "thrudate": classify_by_size.thrudate,
                "party_id": classify_by_size.party_id,
                "party_type_id": classify_by_size.party_type_id,
                "id": classify_by_size_id
            })

            # Update classify_by_size
            query_size = """
                UPDATE classify_by_size
                SET employee_count_range_id = COALESCE(:employee_count_range_id, employee_count_range_id)
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query_size, values={
                "employee_count_range_id": classify_by_size.employee_count_range_id,
                "id": classify_by_size_id
            })
            if not result:
                logger.warning(f"Classify_by_size not found for update: id={classify_by_size_id}")
                return None

            # Fetch updated data
            query_fetch = """
                SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
                       cs.employee_count_range_id, ecr.description
                FROM classify_by_size cs
                JOIN organization_classification oc ON cs.id = oc.id
                JOIN party_classification pc ON cs.id = pc.id
                JOIN employee_count_range ecr ON cs.employee_count_range_id = ecr.id
                WHERE cs.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": classify_by_size_id})
            logger.info(f"Updated classify_by_size: id={classify_by_size_id}")
            return ClassifyBySizeOut(**result)
        except Exception as e:
            logger.error(f"Error updating classify_by_size: {str(e)}")
            raise

async def delete_classify_by_size(classify_by_size_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from classify_by_size
            query_size = """
                DELETE FROM classify_by_size WHERE id = :id
                RETURNING id
            """
            size_result = await database.fetch_one(query=query_size, values={"id": classify_by_size_id})
            if not size_result:
                logger.warning(f"Classify_by_size not found for deletion: id={classify_by_size_id}")
                return False

            # Delete from organization_classification
            query_org_cl = """
                DELETE FROM organization_classification WHERE id = :id
            """
            await database.execute(query=query_org_cl, values={"id": classify_by_size_id})

            # Delete from party_classification
            query_party_cl = """
                DELETE FROM party_classification WHERE id = :id
            """
            await database.execute(query=query_party_cl, values={"id": classify_by_size_id})

            logger.info(f"Deleted classify_by_size: id={classify_by_size_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting classify_by_size: {str(e)}")
            raise