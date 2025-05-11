from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.country import CountryCreate, CountryUpdate, CountryOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_country(country: CountryCreate) -> Optional[CountryOut]:
    query = """
        SELECT id, isocode, name_en, name_th FROM country WHERE isocode = :isocode
    """
    existing = await database.fetch_one(query=query, values={"isocode": country.isocode})
    if existing:
        logger.warning(f"Country with isocode '{country.isocode}' already exists")
        return None

    query = """
        INSERT INTO country (isocode, name_en, name_th)
        VALUES (:isocode, :name_en, :name_th)
        RETURNING id, isocode, name_en, name_th
    """
    try:
        result = await database.fetch_one(query=query, values={"isocode": country.isocode, "name_en": country.name_en, "name_th": country.name_th})
        logger.info(f"Created country: id={result['id']}, isocode={result['isocode']}")
        return CountryOut(**result)
    except Exception as e:
        logger.error(f"Error creating country: {str(e)}")
        raise

async def get_country(country_id: int) -> Optional[CountryOut]:
    query = """
        SELECT id, isocode, name_en, name_th FROM country WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": country_id})
    if not result:
        logger.warning(f"Country not found: id={country_id}")
        return None
    logger.info(f"Retrieved country: id={result['id']}, isocode={result['isocode']}")
    return CountryOut(**result)

async def get_all_countries() -> List[CountryOut]:
    query = """
        SELECT id, isocode, name_en, name_th FROM country
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} countries")
    return [CountryOut(**result) for result in results]

async def update_country(country_id: int, country: CountryUpdate) -> Optional[CountryOut]:
    if country.isocode:
        query = """
            SELECT id, isocode, name_en, name_th FROM country WHERE isocode = :isocode AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"isocode": country.isocode, "id": country_id})
        if existing:
            logger.warning(f"Country with isocode '{country.isocode}' already exists")
            return None

    query = """
        UPDATE country
        SET isocode = COALESCE(:isocode, isocode),
            name_en = COALESCE(:name_en, name_en),
            name_th = COALESCE(:name_th, name_th)
        WHERE id = :id
        RETURNING id, isocode, name_en, name_th
    """
    try:
        result = await database.fetch_one(query=query, values={"isocode": country.isocode, "name_en": country.name_en, "name_th": country.name_th, "id": country_id})
        if not result:
            logger.warning(f"Country not found for update: id={country_id}")
            return None
        logger.info(f"Updated country: id={result['id']}, isocode={result['isocode']}")
        return CountryOut(**result)
    except Exception as e:
        logger.error(f"Error updating country: {str(e)}")
        raise

async def delete_country(country_id: int) -> bool:
    query = """
        DELETE FROM country WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": country_id})
    if not result:
        logger.warning(f"Country not found for deletion: id={country_id}")
        return False
    logger.info(f"Deleted country: id={country_id}")
    return True