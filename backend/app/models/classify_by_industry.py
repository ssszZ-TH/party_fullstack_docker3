from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.classify_by_industry import ClassifyByIndustryCreate, ClassifyByIndustryUpdate, ClassifyByIndustryOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_classify_by_industry(classify_by_industry: ClassifyByIndustryCreate) -> Optional[ClassifyByIndustryOut]:
    async with database.transaction():
        try:
            # 1. Insert into party_classification
            query_party_cl = """
                INSERT INTO party_classification (fromdate, thrudate, party_id, party_type_id)
                VALUES (:fromdate, :thrudate, :party_id, :party_type_id)
                RETURNING id
            """
            party_cl_result = await database.fetch_one(query=query_party_cl, values={
                "fromdate": classify_by_industry.fromdate,
                "thrudate": classify_by_industry.thrudate,
                "party_id": classify_by_industry.party_id,
                "party_type_id": classify_by_industry.party_type_id
            })
            new_id = party_cl_result["id"]

            # 2. Insert into organization_classification
            query_org_cl = """
                INSERT INTO organization_classification (id)
                VALUES (:id)
            """
            await database.execute(query=query_org_cl, values={"id": new_id})

            # 3. Insert into classify_by_industry
            query_industry = """
                INSERT INTO classify_by_industry (id, industry_type_id)
                VALUES (:id, :industry_type_id)
                RETURNING id
            """
            await database.execute(query=query_industry, values={
                "id": new_id,
                "industry_type_id": classify_by_industry.industry_type_id
            })

            # Fetch the complete data
            query_fetch = """
                SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
                       ci.industry_type_id, it.naics_code, it.description
                FROM classify_by_industry ci
                JOIN organization_classification oc ON ci.id = oc.id
                JOIN party_classification pc ON ci.id = pc.id
                JOIN industry_type it ON ci.industry_type_id = it.id
                WHERE ci.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": new_id})
            logger.info(f"Created classify_by_industry: id={new_id}")
            return ClassifyByIndustryOut(**result)
        except Exception as e:
            logger.error(f"Error creating classify_by_industry: {str(e)}")
            raise

async def get_classify_by_industry(classify_by_industry_id: int) -> Optional[ClassifyByIndustryOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               ci.industry_type_id, it.naics_code, it.description
        FROM classify_by_industry ci
        JOIN organization_classification oc ON ci.id = oc.id
        JOIN party_classification pc ON ci.id = pc.id
        JOIN industry_type it ON ci.industry_type_id = it.id
        WHERE ci.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": classify_by_industry_id})
    if not result:
        logger.warning(f"Classify_by_industry not found: id={classify_by_industry_id}")
        return None
    logger.info(f"Retrieved classify_by_industry: id={result['id']}")
    return ClassifyByIndustryOut(**result)

async def get_all_classify_by_industries() -> List[ClassifyByIndustryOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               ci.industry_type_id, it.naics_code, it.description
        FROM classify_by_industry ci
        JOIN organization_classification oc ON ci.id = oc.id
        JOIN party_classification pc ON ci.id = pc.id
        JOIN industry_type it ON ci.industry_type_id = it.id
        ORDER BY pc.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} classify_by_industries")
    return [ClassifyByIndustryOut(**result) for result in results]

async def update_classify_by_industry(classify_by_industry_id: int, classify_by_industry: ClassifyByIndustryUpdate) -> Optional[ClassifyByIndustryOut]:
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
                "fromdate": classify_by_industry.fromdate,
                "thrudate": classify_by_industry.thrudate,
                "party_id": classify_by_industry.party_id,
                "party_type_id": classify_by_industry.party_type_id,
                "id": classify_by_industry_id
            })

            # Update classify_by_industry
            query_industry = """
                UPDATE classify_by_industry
                SET industry_type_id = COALESCE(:industry_type_id, industry_type_id)
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query_industry, values={
                "industry_type_id": classify_by_industry.industry_type_id,
                "id": classify_by_industry_id
            })
            if not result:
                logger.warning(f"Classify_by_industry not found for update: id={classify_by_industry_id}")
                return None

            # Fetch updated data
            query_fetch = """
                SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
                       ci.industry_type_id, it.naics_code, it.description
                FROM classify_by_industry ci
                JOIN organization_classification oc ON ci.id = oc.id
                JOIN party_classification pc ON ci.id = pc.id
                JOIN industry_type it ON ci.industry_type_id = it.id
                WHERE ci.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": classify_by_industry_id})
            logger.info(f"Updated classify_by_industry: id={classify_by_industry_id}")
            return ClassifyByIndustryOut(**result)
        except Exception as e:
            logger.error(f"Error updating classify_by_industry: {str(e)}")
            raise

async def delete_classify_by_industry(classify_by_industry_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from classify_by_industry
            query_industry = """
                DELETE FROM classify_by_industry WHERE id = :id
                RETURNING id
            """
            industry_result = await database.fetch_one(query=query_industry, values={"id": classify_by_industry_id})
            if not industry_result:
                logger.warning(f"Classify_by_industry not found for deletion: id={classify_by_industry_id}")
                return False

            # Delete from organization_classification
            query_org_cl = """
                DELETE FROM organization_classification WHERE id = :id
            """
            await database.execute(query=query_org_cl, values={"id": classify_by_industry_id})

            # Delete from party_classification
            query_party_cl = """
                DELETE FROM party_classification WHERE id = :id
            """
            await database.execute(query=query_party_cl, values={"id": classify_by_industry_id})

            logger.info(f"Deleted classify_by_industry: id={classify_by_industry_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting classify_by_industry: {str(e)}")
            raise