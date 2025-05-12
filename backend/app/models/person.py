from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.person import PersonCreate, PersonUpdate, PersonOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_person(person: PersonCreate) -> Optional[PersonOut]:
    async with database.transaction():
        try:
            # 1. Insert into party and get id
            query_party = """
                INSERT INTO party (id)
                VALUES (DEFAULT)
                RETURNING id
            """
            party_result = await database.fetch_one(query=query_party)
            new_id = party_result["id"]

            # 2. Insert into person with the new id
            query_person = """
                INSERT INTO person (
                    id, socialsecuritynumber, birthdate, mothermaidenname, 
                    totalyearworkexperience, comment
                )
                VALUES (
                    :id, :socialsecuritynumber, :birthdate, :mothermaidenname, 
                    :totalyearworkexperience, :comment
                )
                RETURNING id, socialsecuritynumber, birthdate, mothermaidenname, 
                          totalyearworkexperience, comment
            """
            result = await database.fetch_one(query=query_person, values={
                "id": new_id,
                "socialsecuritynumber": person.socialsecuritynumber,
                "birthdate": person.birthdate,
                "mothermaidenname": person.mothermaidenname,
                "totalyearworkexperience": person.totalyearworkexperience,
                "comment": person.comment
            })
            logger.info(f"Created person: id={result['id']}")
            return PersonOut(**result)
        except Exception as e:
            logger.error(f"Error creating person: {str(e)}")
            raise

async def get_person(person_id: int) -> Optional[PersonOut]:
    query = """
        SELECT id, socialsecuritynumber, birthdate, mothermaidenname, 
               totalyearworkexperience, comment
        FROM person WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": person_id})
    if not result:
        logger.warning(f"Person not found: id={person_id}")
        return None
    logger.info(f"Retrieved person: id={result['id']}")
    return PersonOut(**result)

async def get_all_persons() -> List[PersonOut]:
    query = """
        SELECT id, socialsecuritynumber, birthdate, mothermaidenname, 
               totalyearworkexperience, comment
        FROM person ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} persons")
    return [PersonOut(**result) for result in results]

async def update_person(person_id: int, person: PersonUpdate) -> Optional[PersonOut]:
    query = """
        UPDATE person
        SET socialsecuritynumber = COALESCE(:socialsecuritynumber, socialsecuritynumber),
            birthdate = COALESCE(:birthdate, birthdate),
            mothermaidenname = COALESCE(:mothermaidenname, mothermaidenname),
            totalyearworkexperience = COALESCE(:totalyearworkexperience, totalyearworkexperience),
            comment = COALESCE(:comment, comment)
        WHERE id = :id
        RETURNING id, socialsecuritynumber, birthdate, mothermaidenname, 
                  totalyearworkexperience, comment
    """
    try:
        result = await database.fetch_one(query=query, values={
            "socialsecuritynumber": person.socialsecuritynumber,
            "birthdate": person.birthdate,
            "mothermaidenname": person.mothermaidenname,
            "totalyearworkexperience": person.totalyearworkexperience,
            "comment": person.comment,
            "id": person_id
        })
        if not result:
            logger.warning(f"Person not found for update: id={person_id}")
            return None
        logger.info(f"Updated person: id={result['id']}")
        return PersonOut(**result)
    except Exception as e:
        logger.error(f"Error updating person: {str(e)}")
        raise

async def delete_person(person_id: int) -> bool:
    # Check if person is referenced in related tables
    query_check = """
        SELECT id FROM citizenship WHERE person_id = :id
        UNION
        SELECT id FROM personname WHERE person_id = :id
        UNION
        SELECT id FROM physicalcharacteristic WHERE person_id = :id
        UNION
        SELECT id FROM maritalstatus WHERE person_id = :id
        LIMIT 1
    """
    referenced = await database.fetch_one(query=query_check, values={"id": person_id})
    if referenced:
        logger.warning(f"Cannot delete person: id={person_id}, referenced in related tables")
        return False

    async with database.transaction():
        try:
            # Delete from person
            query_person = """
                DELETE FROM person WHERE id = :id
                RETURNING id
            """
            person_result = await database.fetch_one(query=query_person, values={"id": person_id})
            if not person_result:
                logger.warning(f"Person not found for deletion: id={person_id}")
                return False

            # Delete from party
            query_party = """
                DELETE FROM party WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_party, values={"id": person_id})

            logger.info(f"Deleted person: id={person_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting person: {str(e)}")
            raise