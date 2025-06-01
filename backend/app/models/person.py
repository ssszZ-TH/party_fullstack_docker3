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
            p.id, p.personal_id_number, p.birthdate, p.mothermaidenname, 
            p.totalyearworkexperience, p.comment, p.gender_type_id,
            gt.description AS gender_description,
            (SELECT jsonb_build_object(
                'id', pn1.id,
                'name', pn1.name,
                'fromdate', pn1.fromdate,
                'thrudate', pn1.thrudate,
                'personnametype_id', pn1.personnametype_id,
                'personnametype_description', pnt1.description
            ) FROM personname pn1
            JOIN personnametype pnt1 ON pn1.personnametype_id = pnt1.id
            WHERE pn1.person_id = p.id AND pnt1.description = 'FirstName'
            AND (pn1.thrudate IS NULL OR pn1.thrudate > CURRENT_DATE)
            ORDER BY pn1.fromdate DESC LIMIT 1) AS firstname,
            (SELECT jsonb_build_object(
                'id', pn2.id,
                'name', pn2.name,
                'fromdate', pn2.fromdate,
                'thrudate', pn2.thrudate,
                'personnametype_id', pn2.personnametype_id,
                'personnametype_description', pnt2.description
            ) FROM personname pn2
            JOIN personnametype pnt2 ON pn2.personnametype_id = pnt2.id
            WHERE pn2.person_id = p.id AND pnt2.description = 'MiddleName'
            AND (pn2.thrudate IS NULL OR pn2.thrudate > CURRENT_DATE)
            ORDER BY pn2.fromdate DESC LIMIT 1) AS middlename,
            (SELECT jsonb_build_object(
                'id', pn3.id,
                'name', pn3.name,
                'fromdate', pn3.fromdate,
                'thrudate', pn3.thrudate,
                'personnametype_id', pn3.personnametype_id,
                'personnametype_description', pnt3.description
            ) FROM personname pn3
            JOIN personnametype pnt3 ON pn3.personnametype_id = pnt3.id
            WHERE pn3.person_id = p.id AND pnt3.description = 'LastName'
            AND (pn3.thrudate IS NULL OR pn3.thrudate > CURRENT_DATE)
            ORDER BY pn3.fromdate DESC LIMIT 1) AS lastname,
            (SELECT jsonb_build_object(
                'id', ms.id,
                'fromdate', ms.fromdate,
                'thrudate', ms.thrudate,
                'maritalstatustype_id', ms.maritalstatustype_id,
                'maritalstatustype_description', mst.description
            ) FROM maritalstatus ms
            JOIN maritalstatustype mst ON ms.maritalstatustype_id = mst.id
            WHERE ms.person_id = p.id
            AND (ms.thrudate IS NULL OR ms.thrudate > CURRENT_DATE)
            ORDER BY ms.fromdate DESC LIMIT 1) AS marital_status,
            (SELECT jsonb_build_object(
                'id', pc1.id,
                'val', pc1.val,
                'fromdate', pc1.fromdate,
                'thrudate', pc1.thrudate,
                'physicalcharacteristictype_id', pc1.physicalcharacteristictype_id,
                'physicalcharacteristictype_description', pct1.description
            ) FROM physicalcharacteristic pc1
            JOIN physicalcharacteristictype pct1 ON pc1.physicalcharacteristictype_id = pct1.id
            WHERE pc1.person_id = p.id AND pct1.description = 'Height'
            AND (pc1.thrudate IS NULL OR pc1.thrudate > CURRENT_DATE)
            ORDER BY pc1.fromdate DESC LIMIT 1) AS height,
            (SELECT jsonb_build_object(
                'id', pc2.id,
                'val', pc2.val,
                'fromdate', pc2.fromdate,
                'thrudate', pc2.thrudate,
                'physicalcharacteristictype_id', pc2.physicalcharacteristictype_id,
                'physicalcharacteristictype_description', pct2.description
            ) FROM physicalcharacteristic pc2
            JOIN physicalcharacteristictype pct2 ON pc2.physicalcharacteristictype_id = pct2.id
            WHERE pc2.person_id = p.id AND pct2.description = 'Weight'
            AND (pc2.thrudate IS NULL OR pc2.thrudate > CURRENT_DATE)
            ORDER BY pc2.fromdate DESC LIMIT 1) AS weight,
            (SELECT jsonb_build_object(
                'id', c.id,
                'fromdate', c.fromdate,
                'thrudate', c.thrudate,
                'country_id', c.country_id,
                'country_isocode', co.isocode,
                'country_name_en', co.name_en,
                'country_name_th', co.name_th
            ) FROM citizenship c
            JOIN country co ON c.country_id = co.id
            WHERE c.person_id = p.id
            AND (c.thrudate IS NULL OR c.thrudate > CURRENT_DATE)
            ORDER BY c.fromdate DESC LIMIT 1) AS citizenship
        FROM person p
        LEFT JOIN gender_type gt ON p.gender_type_id = gt.id
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
            p.id, p.personal_id_number, p.birthdate, p.mothermaidenname, 
            p.totalyearworkexperience, p.comment, p.gender_type_id,
            gt.description AS gender_description,
            (SELECT jsonb_build_object(
                'id', pn1.id,
                'name', pn1.name,
                'fromdate', pn1.fromdate,
                'thrudate', pn1.thrudate,
                'personnametype_id', pn1.personnametype_id,
                'personnametype_description', pnt1.description
            ) FROM personname pn1
            JOIN personnametype pnt1 ON pn1.personnametype_id = pnt1.id
            WHERE pn1.person_id = p.id AND pnt1.description = 'FirstName'
            AND (pn1.thrudate IS NULL OR pn1.thrudate > CURRENT_DATE)
            ORDER BY pn1.fromdate DESC LIMIT 1) AS firstname,
            (SELECT jsonb_build_object(
                'id', pn2.id,
                'name', pn2.name,
                'fromdate', pn2.fromdate,
                'thrudate', pn2.thrudate,
                'personnametype_id', pn2.personnametype_id,
                'personnametype_description', pnt2.description
            ) FROM personname pn2
            JOIN personnametype pnt2 ON pn2.personnametype_id = pnt2.id
            WHERE pn2.person_id = p.id AND pnt2.description = 'MiddleName'
            AND (pn2.thrudate IS NULL OR pn2.thrudate > CURRENT_DATE)
            ORDER BY pn2.fromdate DESC LIMIT 1) AS middlename,
            (SELECT jsonb_build_object(
                'id', pn3.id,
                'name', pn3.name,
                'fromdate', pn3.fromdate,
                'thrudate', pn3.thrudate,
                'personnametype_id', pn3.personnametype_id,
                'personnametype_description', pnt3.description
            ) FROM personname pn3
            JOIN personnametype pnt3 ON pn3.personnametype_id = pnt3.id
            WHERE pn3.person_id = p.id AND pnt3.description = 'LastName'
            AND (pn3.thrudate IS NULL OR pn3.thrudate > CURRENT_DATE)
            ORDER BY pn3.fromdate DESC LIMIT 1) AS lastname,
            (SELECT jsonb_build_object(
                'id', ms.id,
                'fromdate', ms.fromdate,
                'thrudate', ms.thrudate,
                'maritalstatustype_id', ms.maritalstatustype_id,
                'maritalstatustype_description', mst.description
            ) FROM maritalstatus ms
            JOIN maritalstatustype mst ON ms.maritalstatustype_id = mst.id
            WHERE ms.person_id = p.id
            AND (ms.thrudate IS NULL OR ms.thrudate > CURRENT_DATE)
            ORDER BY ms.fromdate DESC LIMIT 1) AS marital_status,
            (SELECT jsonb_build_object(
                'id', pc1.id,
                'val', pc1.val,
                'fromdate', pc1.fromdate,
                'thrudate', pc1.thrudate,
                'physicalcharacteristictype_id', pc1.physicalcharacteristictype_id,
                'physicalcharacteristictype_description', pct1.description
            ) FROM physicalcharacteristic pc1
            JOIN physicalcharacteristictype pct1 ON pc1.physicalcharacteristictype_id = pct1.id
            WHERE pc1.person_id = p.id AND pct1.description = 'Height'
            AND (pc1.thrudate IS NULL OR pc1.thrudate > CURRENT_DATE)
            ORDER BY pc1.fromdate DESC LIMIT 1) AS height,
            (SELECT jsonb_build_object(
                'id', pc2.id,
                'val', pc2.val,
                'fromdate', pc2.fromdate,
                'thrudate', pc2.thrudate,
                'physicalcharacteristictype_id', pc2.physicalcharacteristictype_id,
                'physicalcharacteristictype_description', pct2.description
            ) FROM physicalcharacteristic pc2
            JOIN physicalcharacteristictype pct2 ON pc2.physicalcharacteristictype_id = pct2.id
            WHERE pc2.person_id = p.id AND pct2.description = 'Weight'
            AND (pc2.thrudate IS NULL OR pc2.thrudate > CURRENT_DATE)
            ORDER BY pc2.fromdate DESC LIMIT 1) AS weight,
            (SELECT jsonb_build_object(
                'id', c.id,
                'fromdate', c.fromdate,
                'thrudate', c.thrudate,
                'country_id', c.country_id,
                'country_isocode', co.isocode,
                'country_name_en', co.name_en,
                'country_name_th', co.name_th
            ) FROM citizenship c
            JOIN country co ON c.country_id = co.id
            WHERE c.person_id = p.id
            AND (c.thrudate IS NULL OR c.thrudate > CURRENT_DATE)
            ORDER BY c.fromdate DESC LIMIT 1) AS citizenship
        FROM person p
        LEFT JOIN gender_type gt ON p.gender_type_id = gt.id
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