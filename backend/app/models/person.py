from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.person import PersonCreate, PersonUpdate, PersonOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_person(person: PersonCreate) -> Optional[PersonOut]:
    async with database.transaction():
        try:
            query_party = """
                INSERT INTO party (id)
                VALUES (DEFAULT)
                RETURNING id
            """
            party_result = await database.fetch_one(query=query_party)
            new_id = party_result["id"]

            query_person = """
                INSERT INTO person (
                    id, personal_id_number, birthdate, mothermaidenname, 
                    totalyearworkexperience, comment, gender_type_id
                )
                VALUES (
                    :id, :personal_id_number, :birthdate, :mothermaidenname, 
                    :totalyearworkexperience, :comment, :gender_type_id
                )
                RETURNING id
            """
            await database.fetch_one(query=query_person, values={
                "id": new_id,
                "personal_id_number": person.personal_id_number,
                "birthdate": person.birthdate,
                "mothermaidenname": person.mothermaidenname,
                "totalyearworkexperience": person.totalyearworkexperience,
                "comment": person.comment,
                "gender_type_id": person.gender_type_id
            })
            return await get_person(new_id)
        except Exception as e:
            logger.error(f"Error creating person: {str(e)}")
            raise

async def get_person(person_id: int) -> Optional[PersonOut]:
    query = """
        SELECT 
            p.id, 
            p.personal_id_number, 
            p.birthdate, 
            p.mothermaidenname, 
            p.totalyearworkexperience, 
            p.comment, 
            p.gender_type_id,
            gt.description AS gender_description,
            pn1.id AS fname_id,
            pn1.name AS fname,
            pn1.fromdate AS fname_fromdate,
            pn1.thrudate AS fname_thrudate,
            pn1.personnametype_id AS fname_personnametype_id,
            pnt1.description AS fname_personnametype_description,
            pn2.id AS mname_id,
            pn2.name AS mname,
            pn2.fromdate AS mname_fromdate,
            pn2.thrudate AS mname_thrudate,
            pn2.personnametype_id AS mname_personnametype_id,
            pnt2.description AS mname_personnametype_description,
            pn3.id AS lname_id,
            pn3.name AS lname,
            pn3.fromdate AS lname_fromdate,
            pn3.thrudate AS lname_thrudate,
            pn3.personnametype_id AS lname_personnametype_id,
            pnt3.description AS lname_personnametype_description,
            ms.id AS marital_status_id,
            ms.fromdate AS marital_status_fromdate,
            ms.thrudate AS marital_status_thrudate,
            ms.maritalstatustype_id AS marital_status_type_id,
            mst.description AS marital_status_type_description,
            pc1.id AS height_id,
            pc1.val AS height_val,
            pc1.fromdate AS height_fromdate,
            pc1.thrudate AS height_thrudate,
            pc1.physicalcharacteristictype_id AS height_type_id,
            pct1.description AS height_type_description,
            pc2.id AS weight_id,
            pc2.val AS weight_val,
            pc2.fromdate AS weight_fromdate,
            pc2.thrudate AS weight_thrudate,
            pc2.physicalcharacteristictype_id AS weight_type_id,
            pct2.description AS weight_type_description,
            c.id AS citizenship_id,
            c.fromdate AS citizenship_fromdate,
            c.thrudate AS citizenship_thrudate,
            c.country_id AS country_id,
            co.isocode AS country_isocode,
            co.name_en AS country_name_en,
            co.name_th AS country_name_th
        FROM person p
        LEFT JOIN gender_type gt ON p.gender_type_id = gt.id
        LEFT JOIN personname pn1 ON pn1.person_id = p.id 
            AND pn1.personnametype_id = (SELECT id FROM personnametype WHERE description = 'FirstName')
        LEFT JOIN personnametype pnt1 ON pn1.personnametype_id = pnt1.id
        LEFT JOIN personname pn2 ON pn2.person_id = p.id 
            AND pn2.personnametype_id = (SELECT id FROM personnametype WHERE description = 'MiddleName')
        LEFT JOIN personnametype pnt2 ON pn2.personnametype_id = pnt2.id
        LEFT JOIN personname pn3 ON pn3.person_id = p.id 
            AND pn3.personnametype_id = (SELECT id FROM personnametype WHERE description = 'LastName')
        LEFT JOIN personnametype pnt3 ON pn3.personnametype_id = pnt3.id
        LEFT JOIN maritalstatus ms ON ms.person_id = p.id
        LEFT JOIN maritalstatustype mst ON ms.maritalstatustype_id = mst.id
        LEFT JOIN physicalcharacteristic pc1 ON pc1.person_id = p.id 
            AND pc1.physicalcharacteristictype_id = (SELECT id FROM physicalcharacteristictype WHERE description = 'Height')
        LEFT JOIN physicalcharacteristictype pct1 ON pc1.physicalcharacteristictype_id = pct1.id
        LEFT JOIN physicalcharacteristic pc2 ON pc2.person_id = p.id 
            AND pc2.physicalcharacteristictype_id = (SELECT id FROM physicalcharacteristictype WHERE description = 'Weight')
        LEFT JOIN physicalcharacteristictype pct2 ON pc2.physicalcharacteristictype_id = pct2.id
        LEFT JOIN (
            SELECT c.* 
            FROM citizenship c
            ORDER BY c.fromdate DESC LIMIT 1
        ) c ON c.person_id = p.id
        LEFT JOIN country co ON c.country_id = co.id
        WHERE p.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": person_id})
    if not result:
        logger.warning(f"Person not found: id={person_id}")
        return None
    logger.info(f"Fetched person: id={result['id']}")
    return PersonOut(**result)

async def get_all_persons() -> List[PersonOut]:
    query = """
        SELECT 
            p.id, 
            p.personal_id_number, 
            p.birthdate, 
            p.mothermaidenname, 
            p.totalyearworkexperience, 
            p.comment, 
            p.gender_type_id,
            gt.description AS gender_description,
            pn1.id AS fname_id,
            pn1.name AS fname,
            pn1.fromdate AS fname_fromdate,
            pn1.thrudate AS fname_thrudate,
            pn1.personnametype_id AS fname_personnametype_id,
            pnt1.description AS fname_personnametype_description,
            pn2.id AS mname_id,
            pn2.name AS mname,
            pn2.fromdate AS mname_fromdate,
            pn2.thrudate AS mname_thrudate,
            pn2.personnametype_id AS mname_personnametype_id,
            pnt2.description AS mname_personnametype_description,
            pn3.id AS lname_id,
            pn3.name AS lname,
            pn3.fromdate AS lname_fromdate,
            pn3.thrudate AS lname_thrudate,
            pn3.personnametype_id AS lname_personnametype_id,
            pnt3.description AS lname_personnametype_description,
            ms.id AS marital_status_id,
            ms.fromdate AS marital_status_fromdate,
            ms.thrudate AS marital_status_thrudate,
            ms.maritalstatustype_id AS marital_status_type_id,
            mst.description AS marital_status_type_description,
            pc1.id AS height_id,
            pc1.val AS height_val,
            pc1.fromdate AS height_fromdate,
            pc1.thrudate AS height_thrudate,
            pc1.physicalcharacteristictype_id AS height_type_id,
            pct1.description AS height_type_description,
            pc2.id AS weight_id,
            pc2.val AS weight_val,
            pc2.fromdate AS weight_fromdate,
            pc2.thrudate AS weight_thrudate,
            pc2.physicalcharacteristictype_id AS weight_type_id,
            pct2.description AS weight_type_description,
            c.id AS citizenship_id,
            c.fromdate AS citizenship_fromdate,
            c.thrudate AS citizenship_thrudate,
            c.country_id AS country_id,
            co.isocode AS country_isocode,
            co.name_en AS country_name_en,
            co.name_th AS country_name_th
        FROM person p
        LEFT JOIN gender_type gt ON p.gender_type_id = gt.id
        LEFT JOIN personname pn1 ON pn1.person_id = p.id 
            AND pn1.personnametype_id = (SELECT id FROM personnametype WHERE description = 'FirstName')
        LEFT JOIN personnametype pnt1 ON pn1.personnametype_id = pnt1.id
        LEFT JOIN personname pn2 ON pn2.person_id = p.id 
            AND pn2.personnametype_id = (SELECT id FROM personnametype WHERE description = 'MiddleName')
        LEFT JOIN personnametype pnt2 ON pn2.personnametype_id = pnt2.id
        LEFT JOIN personname pn3 ON pn3.person_id = p.id 
            AND pn3.personnametype_id = (SELECT id FROM personnametype WHERE description = 'LastName')
        LEFT JOIN personnametype pnt3 ON pn3.personnametype_id = pnt3.id
        LEFT JOIN maritalstatus ms ON ms.person_id = p.id
        LEFT JOIN maritalstatustype mst ON ms.maritalstatustype_id = mst.id
        LEFT JOIN physicalcharacteristic pc1 ON pc1.person_id = p.id 
            AND pc1.physicalcharacteristictype_id = (SELECT id FROM physicalcharacteristictype WHERE description = 'Height')
        LEFT JOIN physicalcharacteristictype pct1 ON pc1.physicalcharacteristictype_id = pct1.id
        LEFT JOIN physicalcharacteristic pc2 ON pc2.person_id = p.id 
            AND pc2.physicalcharacteristictype_id = (SELECT id FROM physicalcharacteristictype WHERE description = 'Weight')
        LEFT JOIN physicalcharacteristictype pct2 ON pc2.physicalcharacteristictype_id = pct2.id
        LEFT JOIN (
            SELECT c.* 
            FROM citizenship c
            ORDER BY c.fromdate DESC LIMIT 1
        ) c ON c.person_id = p.id
        LEFT JOIN country co ON c.country_id = co.id
        ORDER BY p.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Fetched {len(results)} persons")
    return [PersonOut(**result) for result in results]

async def update_person(person_id: int, person: PersonUpdate) -> Optional[PersonOut]:
    query = """
        UPDATE person
        SET personal_id_number = COALESCE(:personal_id_number, personal_id_number),
            birthdate = COALESCE(:birthdate, birthdate),
            mothermaidenname = COALESCE(:mothermaidenname, mothermaidenname),
            totalyearworkexperience = COALESCE(:totalyearworkexperience, totalyearworkexperience),
            comment = COALESCE(:comment, comment),
            gender_type_id = COALESCE(:gender_type_id, gender_type_id)
        WHERE id = :id
        RETURNING id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "personal_id_number": person.personal_id_number,
            "birthdate": person.birthdate,
            "mothermaidenname": person.mothermaidenname,
            "totalyearworkexperience": person.totalyearworkexperience,
            "comment": person.comment,
            "gender_type_id": person.gender_type_id,
            "id": person_id
        })
        if not result:
            logger.warning(f"Person not found for update: id={person_id}")
            return None
        return await get_person(person_id)
    except Exception as e:
        logger.error(f"Error updating person: {str(e)}")
        raise

async def delete_person(person_id: int) -> bool:
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
            query_person = """
                DELETE FROM person WHERE id = :id
                RETURNING id
            """
            person_result = await database.fetch_one(query=query_person, values={"id": person_id})
            if not person_result:
                logger.warning(f"Person not found for deletion: id={person_id}")
                return False

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