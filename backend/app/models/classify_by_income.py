from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.classify_by_income import ClassifyByIncomeCreate, ClassifyByIncomeUpdate, ClassifyByIncomeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_classify_by_income(classify_by_income: ClassifyByIncomeCreate) -> Optional[ClassifyByIncomeOut]:
    async with database.transaction():
        try:
            # 1. Insert into party_classification
            query_party_cl = """
                INSERT INTO party_classification (fromdate, thrudate, party_id, party_type_id)
                VALUES (:fromdate, :thrudate, :party_id, :party_type_id)
                RETURNING id
            """
            party_cl_result = await database.fetch_one(query=query_party_cl, values={
                "fromdate": classify_by_income.fromdate,
                "thrudate": classify_by_income.thrudate,
                "party_id": classify_by_income.party_id,
                "party_type_id": classify_by_income.party_type_id
            })
            new_id = party_cl_result["id"]

            # 2. Insert into person_classification
            query_person_cl = """
                INSERT INTO person_classification (id)
                VALUES (:id)
            """
            await database.execute(query=query_person_cl, values={"id": new_id})

            # 3. Insert into classify_by_income
            query_income = """
                INSERT INTO classify_by_income (id, income_range_id)
                VALUES (:id, :income_range_id)
                RETURNING id
            """
            await database.execute(query=query_income, values={
                "id": new_id,
                "income_range_id": classify_by_income.income_range_id
            })

            # Fetch the complete data
            query_fetch = """
                SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
                       ci.income_range_id, ir.description
                FROM classify_by_income ci
                JOIN person_classification pcn ON ci.id = pcn.id
                JOIN party_classification pc ON ci.id = pc.id
                JOIN income_range ir ON ci.income_range_id = ir.id
                WHERE ci.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": new_id})
            logger.info(f"Created classify_by_income: id={new_id}")
            return ClassifyByIncomeOut(**result)
        except Exception as e:
            logger.error(f"Error creating classify_by_income: {str(e)}")
            raise

async def get_classify_by_income(classify_by_income_id: int) -> Optional[ClassifyByIncomeOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               ci.income_range_id, ir.description
        FROM classify_by_income ci
        JOIN person_classification pcn ON ci.id = pcn.id
        JOIN party_classification pc ON ci.id = pc.id
        JOIN income_range ir ON ci.income_range_id = ir.id
        WHERE ci.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": classify_by_income_id})
    if not result:
        logger.warning(f"Classify_by_income not found: id={classify_by_income_id}")
        return None
    logger.info(f"Retrieved classify_by_income: id={result['id']}")
    return ClassifyByIncomeOut(**result)

async def get_all_classify_by_incomes() -> List[ClassifyByIncomeOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               ci.income_range_id, ir.description
        FROM classify_by_income ci
        JOIN person_classification pcn ON ci.id = pcn.id
        JOIN party_classification pc ON ci.id = pc.id
        JOIN income_range ir ON ci.income_range_id = ir.id
        ORDER BY pc.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} classify_by_incomes")
    return [ClassifyByIncomeOut(**result) for result in results]

async def update_classify_by_income(classify_by_income_id: int, classify_by_income: ClassifyByIncomeUpdate) -> Optional[ClassifyByIncomeOut]:
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
                "fromdate": classify_by_income.fromdate,
                "thrudate": classify_by_income.thrudate,
                "party_id": classify_by_income.party_id,
                "party_type_id": classify_by_income.party_type_id,
                "id": classify_by_income_id
            })

            # Update classify_by_income
            query_income = """
                UPDATE classify_by_income
                SET income_range_id = COALESCE(:income_range_id, income_range_id)
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query_income, values={
                "income_range_id": classify_by_income.income_range_id,
                "id": classify_by_income_id
            })
            if not result:
                logger.warning(f"Classify_by_income not found for update: id={classify_by_income_id}")
                return None

            # Fetch updated data
            query_fetch = """
                SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
                       ci.income_range_id, ir.description
                FROM classify_by_income ci
                JOIN person_classification pcn ON ci.id = pcn.id
                JOIN party_classification pc ON ci.id = pc.id
                JOIN income_range ir ON ci.income_range_id = ir.id
                WHERE ci.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": classify_by_income_id})
            logger.info(f"Updated classify_by_income: id={classify_by_income_id}")
            return ClassifyByIncomeOut(**result)
        except Exception as e:
            logger.error(f"Error updating classify_by_income: {str(e)}")
            raise

async def delete_classify_by_income(classify_by_income_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from classify_by_income
            query_income = """
                DELETE FROM classify_by_income WHERE id = :id
                RETURNING id
            """
            income_result = await database.fetch_one(query=query_income, values={"id": classify_by_income_id})
            if not income_result:
                logger.warning(f"Classify_by_income not found for deletion: id={classify_by_income_id}")
                return False

            # Delete from person_classification
            query_person_cl = """
                DELETE FROM person_classification WHERE id = :id
            """
            await database.execute(query=query_person_cl, values={"id": classify_by_income_id})

            # Delete from party_classification
            query_party_cl = """
                DELETE FROM party_classification WHERE id = :id
            """
            await database.execute(query=query_party_cl, values={"id": classify_by_income_id})

            logger.info(f"Deleted classify_by_income: id={classify_by_income_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting classify_by_income: {str(e)}")
            raise