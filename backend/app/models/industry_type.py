from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.industry_type import IndustryTypeCreate, IndustryTypeUpdate, IndustryTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_industry_type(industry_type: IndustryTypeCreate) -> Optional[IndustryTypeOut]:
    query = """
        SELECT id, naics_code, description FROM industry_type WHERE naics_code = :naics_code
    """
    existing = await database.fetch_one(query=query, values={"naics_code": industry_type.naics_code})
    if existing:
        logger.warning(f"Industry type with naics_code '{industry_type.naics_code}' already exists")
        return None

    query = """
        INSERT INTO industry_type (naics_code, description)
        VALUES (:naics_code, :description)
        RETURNING id, naics_code, description
    """
    try:
        result = await database.fetch_one(query=query, values={"naics_code": industry_type.naics_code, "description": industry_type.description})
        logger.info(f"Created industry type: id={result['id']}, naics_code={result['naics_code']}")
        return IndustryTypeOut(**result)
    except Exception as e:
        logger.error(f"Error creating industry type: {str(e)}")
        raise

async def get_industry_type(industry_type_id: int) -> Optional[IndustryTypeOut]:
    query = """
        SELECT id, naics_code, description FROM industry_type WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": industry_type_id})
    if not result:
        logger.warning(f"Industry type not found: id={industry_type_id}")
        return None
    logger.info(f"Retrieved industry type: id={result['id']}, naics_code={result['naics_code']}")
    return IndustryTypeOut(**result)

async def get_all_industry_types() -> List[IndustryTypeOut]:
    query = """
        SELECT id, naics_code, description FROM industry_type
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} industry types")
    return [IndustryTypeOut(**result) for result in results]

async def update_industry_type(industry_type_id: int, industry_type: IndustryTypeUpdate) -> Optional[IndustryTypeOut]:
    if industry_type.naics_code:
        query = """
            SELECT id, naics_code, description FROM industry_type WHERE naics_code = :naics_code AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"naics_code": industry_type.naics_code, "id": industry_type_id})
        if existing:
            logger.warning(f"Industry type with naics_code '{industry_type.naics_code}' already exists")
            return None

    query = """
        UPDATE industry_type
        SET naics_code = COALESCE(:naics_code, naics_code),
            description = COALESCE(:description, description)
        WHERE id = :id
        RETURNING id, naics_code, description
    """
    try:
        result = await database.fetch_one(query=query, values={"naics_code": industry_type.naics_code, "description": industry_type.description, "id": industry_type_id})
        if not result:
            logger.warning(f"Industry type not found for update: id={industry_type_id}")
            return None
        logger.info(f"Updated industry type: id={result['id']}, naics_code={result['naics_code']}")
        return IndustryTypeOut(**result)
    except Exception as e:
        logger.error(f"Error updating industry type: {str(e)}")
        raise

async def delete_industry_type(industry_type_id: int) -> bool:
    query = """
        DELETE FROM industry_type WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": industry_type_id})
    if not result:
        logger.warning(f"Industry type not found for deletion: id={industry_type_id}")
        return False
    logger.info(f"Deleted industry type: id={industry_type_id}")
    return True