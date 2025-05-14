from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.classify_by_eeoc import ClassifyByEeocCreate, ClassifyByEeocUpdate, ClassifyByEeocOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_classify_by_eeoc(classify_by_eeoc: ClassifyByEeocCreate) -> Optional[ClassifyByEeocOut]:
    async with database.transaction():
        try:
            # 1. Insert into party_classification
            query_party_cl = """
                INSERT INTO party_classification (fromdate, thrudate, party_id, party_type_id)
                VALUES (:fromdate, :thrudate, :party_id, :party_type_id)
                RETURNING id
            """
            party_cl_result = await database.fetch_one(query=query_party_cl, values={
                "fromdate": classify_by_eeoc.fromdate,
                "thrudate": classify_by_eeoc.thrudate,
                "party_id": classify_by_eeoc.party_id,
                "party_type_id": classify_by_eeoc.party_type_id
            })
            new_id = party_cl_result["id"]

            # 2. Insert into person_classification
            query_person_cl = """
                INSERT INTO person_classification (id)
                VALUES (:id)
            """
            await database.execute(query=query_person_cl, values={"id": new_id})

            # 3. Insert into classify_by_eeoc
            query_eeoc = """
                INSERT INTO classify_by_eeoc (id, ethnicity_id)
                VALUES (:id, :ethnicity_id)
                RETURNING id
            """
            await database.execute(query=query_eeoc, values={
                "id": new_id,
                "ethnicity_id": classify_by_eeoc.ethnicity_id
            })

            # Fetch the complete data
            query_fetch = """
                SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
                       ce.ethnicity_id, e.name_en, e.name_th
                FROM classify_by_eeoc ce
                JOIN person_classification pcn ON ce.id = pcn.id
                JOIN party_classification pc ON ce.id = pc.id
                JOIN ethnicity e ON ce.ethnicity_id = e.id
                WHERE ce.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": new_id})
            logger.info(f"Created classify_by_eeoc: id={new_id}")
            return ClassifyByEeocOut(**result)
        except Exception as e:
            logger.error(f"Error creating classify_by_eeoc: {str(e)}")
            raise

async def get_classify_by_eeoc(classify_by_eeoc_id: int) -> Optional[ClassifyByEeocOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               ce.ethnicity_id, e.name_en, e.name_th
        FROM classify_by_eeoc ce
        JOIN person_classification pcn ON ce.id = pcn.id
        JOIN party_classification pc ON ce.id = pc.id
        JOIN ethnicity e ON ce.ethnicity_id = e.id
        WHERE ce.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": classify_by_eeoc_id})
    if not result:
        logger.warning(f"Classify_by_eeoc not found: id={classify_by_eeoc_id}")
        return None
    logger.info(f"Retrieved classify_by_eeoc: id={result['id']}")
    return ClassifyByEeocOut(**result)

async def get_all_classify_by_eeocs() -> List[ClassifyByEeocOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               ce.ethnicity_id, e.name_en, e.name_th
        FROM classify_by_eeoc ce
        JOIN person_classification pcn ON ce.id = pcn.id
        JOIN party_classification pc ON ce.id = pc.id
        JOIN ethnicity e ON ce.ethnicity_id = e.id
        ORDER BY pc.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} classify_by_eeocs")
    return [ClassifyByEeocOut(**result) for result in results]

async def update_classify_by_eeoc(classify_by_eeoc_id: int, classify_by_eeoc: ClassifyByEeocUpdate) -> Optional[ClassifyByEeocOut]:
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
                "fromdate": classify_by_eeoc.fromdate,
                "thrudate": classify_by_eeoc.thrudate,
                "party_id": classify_by_eeoc.party_id,
                "party_type_id": classify_by_eeoc.party_type_id,
                "id": classify_by_eeoc_id
            })

            # Update classify_by_eeoc
            query_eeoc = """
                UPDATE classify_by_eeoc
                SET ethnicity_id = COALESCE(:ethnicity_id, ethnicity_id)
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query_eeoc, values={
                "ethnicity_id": classify_by_eeoc.ethnicity_id,
                "id": classify_by_eeoc_id
            })
            if not result:
                logger.warning(f"Classify_by_eeoc not found for update: id={classify_by_eeoc_id}")
                return None

            # Fetch updated data
            query_fetch = """
                SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
                       ce.ethnicity_id, e.name_en, e.name_th
                FROM classify_by_eeoc ce
                JOIN person_classification pcn ON ce.id = pcn.id
                JOIN party_classification pc ON ce.id = pc.id
                JOIN ethnicity e ON ce.ethnicity_id = e.id
                WHERE ce.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": classify_by_eeoc_id})
            logger.info(f"Updated classify_by_eeoc: id={classify_by_eeoc_id}")
            return ClassifyByEeocOut(**result)
        except Exception as e:
            logger.error(f"Error updating classify_by_eeoc: {str(e)}")
            raise

async def delete_classify_by_eeoc(classify_by_eeoc_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from classify_by_eeoc
            query_eeoc = """
                DELETE FROM classify_by_eeoc WHERE id = :id
                RETURNING id
            """
            eeoc_result = await database.fetch_one(query=query_eeoc, values={"id": classify_by_eeoc_id})
            if not eeoc_result:
                logger.warning(f"Classify_by_eeoc not found for deletion: id={classify_by_eeoc_id}")
                return False

            # Delete from person_classification
            query_person_cl = """
                DELETE FROM person_classification WHERE id = :id
            """
            await database.execute(query=query_person_cl, values={"id": classify_by_eeoc_id})

            # Delete from party_classification
            query_party_cl = """
                DELETE FROM party_classification WHERE id = :id
            """
            await database.execute(query=query_party_cl, values={"id": classify_by_eeoc_id})

            logger.info(f"Deleted classify_by_eeoc: id={classify_by_eeoc_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting classify_by_eeoc: {str(e)}")
            raise