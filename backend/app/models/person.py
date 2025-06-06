from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.person import PersonCreate, PersonUpdate, PersonOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_person(person: PersonCreate) -> Optional[PersonOut]:
    async with database.transaction():
        try:
            # Insert into party
            query_party = """
                INSERT INTO party (id)
                VALUES (DEFAULT)
                RETURNING id
            """
            party_result = await database.fetch_one(query=query_party)
            new_id = party_result["id"]

            # Insert into person
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

            # Insert into personname for fname, mname, lname, nickname
            if person.fname:
                query_fname = """
                    INSERT INTO personname (person_id, name, personnametype_id, fromdate)
                    VALUES (:person_id, :name, (SELECT id FROM personnametype WHERE description = 'FirstName'), CURRENT_DATE)
                """
                await database.execute(query_fname, values={"person_id": new_id, "name": person.fname})

            if person.mname:
                query_mname = """
                    INSERT INTO personname (person_id, name, personnametype_id, fromdate)
                    VALUES (:person_id, :name, (SELECT id FROM personnametype WHERE description = 'MiddleName'), CURRENT_DATE)
                """
                await database.execute(query_mname, values={"person_id": new_id, "name": person.mname})

            if person.lname:
                query_lname = """
                    INSERT INTO personname (person_id, name, personnametype_id, fromdate)
                    VALUES (:person_id, :name, (SELECT id FROM personnametype WHERE description = 'LastName'), CURRENT_DATE)
                """
                await database.execute(query_lname, values={"person_id": new_id, "name": person.lname})

            if person.nickname:
                query_nickname = """
                    INSERT INTO personname (person_id, name, personnametype_id, fromdate)
                    VALUES (:person_id, :name, (SELECT id FROM personnametype WHERE description = 'Nickname'), CURRENT_DATE)
                """
                await database.execute(query_nickname, values={"person_id": new_id, "name": person.nickname})

            # Insert into maritalstatus
            if person.marital_status_type_id:
                query_marital = """
                    INSERT INTO maritalstatus (person_id, maritalstatustype_id, fromdate)
                    VALUES (:person_id, :maritalstatustype_id, CURRENT_DATE)
                """
                await database.execute(query_marital, values={
                    "person_id": new_id,
                    "maritalstatustype_id": person.marital_status_type_id
                })

            # Insert into physicalcharacteristic for height
            if person.height_val:
                query_height = """
                    INSERT INTO physicalcharacteristic (person_id, val, physicalcharacteristictype_id, fromdate)
                    VALUES (:person_id, :val, (SELECT id FROM physicalcharacteristictype WHERE description = 'Height'), CURRENT_DATE)
                """
                await database.execute(query_height, values={"person_id": new_id, "val": person.height_val})

            # Insert into physicalcharacteristic for weight
            if person.weight_val:
                query_weight = """
                    INSERT INTO physicalcharacteristic (person_id, val, physicalcharacteristictype_id, fromdate)
                    VALUES (:person_id, :val, (SELECT id FROM physicalcharacteristictype WHERE description = 'Weight'), CURRENT_DATE)
                """
                await database.execute(query_weight, values={"person_id": new_id, "val": person.weight_val})

            # Insert into citizenship
            if person.country_id:
                query_citizenship = """
                    INSERT INTO citizenship (person_id, country_id, fromdate)
                    VALUES (:person_id, :country_id, CURRENT_DATE)
                """
                await database.execute(query_citizenship, values={"person_id": new_id, "country_id": person.country_id})

            return await get_person(new_id)
        except Exception as e:
            logger.error(f"Error creating person: {str(e)}")
            raise

async def get_person(person_id: int) -> Optional[PersonOut]:
    query = """
        WITH ranked_names AS (
            SELECT 
                pn.*, 
                ROW_NUMBER() OVER (PARTITION BY pn.person_id, pn.personnametype_id ORDER BY pn.fromdate DESC) AS rn
            FROM personname pn
        ),
        ranked_marital AS (
            SELECT 
                ms.*, 
                ROW_NUMBER() OVER (PARTITION BY ms.person_id ORDER BY ms.fromdate DESC, ms.id DESC) AS rn
            FROM maritalstatus ms
        ),
        ranked_physical AS (
            SELECT 
                pc.*, 
                ROW_NUMBER() OVER (PARTITION BY pc.person_id, pc.physicalcharacteristictype_id ORDER BY pc.fromdate DESC) AS rn
            FROM physicalcharacteristic pc
        ),
        ranked_citizenship AS (
            SELECT 
                c.*, 
                ROW_NUMBER() OVER (PARTITION BY c.person_id ORDER BY c.fromdate DESC) AS rn
            FROM citizenship c
        )
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
            pn4.id AS nickname_id,
            pn4.name AS nickname,
            pn4.fromdate AS nickname_fromdate,
            pn4.thrudate AS nickname_thrudate,
            pn4.personnametype_id AS nickname_personnametype_id,
            pnt4.description AS nickname_personnametype_description,
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
        LEFT JOIN ranked_names pn1 
            ON pn1.person_id = p.id 
            AND pn1.rn = 1 
            AND pn1.personnametype_id = (SELECT id FROM personnametype WHERE description = 'FirstName')
        LEFT JOIN personnametype pnt1 ON pn1.personnametype_id = pnt1.id
        LEFT JOIN ranked_names pn2 
            ON pn2.person_id = p.id 
            AND pn2.rn = 1 
            AND pn2.personnametype_id = (SELECT id FROM personnametype WHERE description = 'MiddleName')
        LEFT JOIN personnametype pnt2 ON pn2.personnametype_id = pnt2.id
        LEFT JOIN ranked_names pn3 
            ON pn3.person_id = p.id 
            AND pn3.rn = 1 
            AND pn3.personnametype_id = (SELECT id FROM personnametype WHERE description = 'LastName')
        LEFT JOIN personnametype pnt3 ON pn3.personnametype_id = pnt3.id
        LEFT JOIN ranked_names pn4 
            ON pn4.person_id = p.id 
            AND pn4.rn = 1 
            AND pn4.personnametype_id = (SELECT id FROM personnametype WHERE description = 'Nickname')
        LEFT JOIN personnametype pnt4 ON pn4.personnametype_id = pnt4.id
        LEFT JOIN ranked_marital ms 
            ON ms.person_id = p.id 
            AND ms.rn = 1
        LEFT JOIN maritalstatustype mst ON ms.maritalstatustype_id = mst.id
        LEFT JOIN ranked_physical pc1 
            ON pc1.person_id = p.id 
            AND pc1.rn = 1 
            AND pc1.physicalcharacteristictype_id = (SELECT id FROM physicalcharacteristictype WHERE description = 'Height')
        LEFT JOIN physicalcharacteristictype pct1 ON pc1.physicalcharacteristictype_id = pct1.id
        LEFT JOIN ranked_physical pc2 
            ON pc2.person_id = p.id 
            AND pc2.rn = 1 
            AND pc2.physicalcharacteristictype_id = (SELECT id FROM physicalcharacteristictype WHERE description = 'Weight')
        LEFT JOIN physicalcharacteristictype pct2 ON pc2.physicalcharacteristictype_id = pct2.id
        LEFT JOIN ranked_citizenship c 
            ON c.person_id = p.id 
            AND c.rn = 1
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
        WITH ranked_names AS (
            SELECT 
                pn.*, 
                ROW_NUMBER() OVER (PARTITION BY pn.person_id, pn.personnametype_id ORDER BY pn.fromdate DESC) AS rn
            FROM personname pn
        ),
        ranked_marital AS (
            SELECT 
                ms.*, 
                ROW_NUMBER() OVER (PARTITION BY ms.person_id ORDER BY ms.fromdate DESC, ms.id DESC) AS rn
            FROM maritalstatus ms
        ),
        ranked_physical AS (
            SELECT 
                pc.*, 
                ROW_NUMBER() OVER (PARTITION BY pc.person_id, pc.physicalcharacteristictype_id ORDER BY pc.fromdate DESC) AS rn
            FROM physicalcharacteristic pc
        ),
        ranked_citizenship AS (
            SELECT 
                c.*, 
                ROW_NUMBER() OVER (PARTITION BY c.person_id ORDER BY c.fromdate DESC) AS rn
            FROM citizenship c
        )
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
            pn4.id AS nickname_id,
            pn4.name AS nickname,
            pn4.fromdate AS nickname_fromdate,
            pn4.thrudate AS nickname_thrudate,
            pn4.personnametype_id AS nickname_personnametype_id,
            pnt4.description AS nickname_personnametype_description,
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
        LEFT JOIN ranked_names pn1 
            ON pn1.person_id = p.id 
            AND pn1.rn = 1 
            AND pn1.personnametype_id = (SELECT id FROM personnametype WHERE description = 'FirstName')
        LEFT JOIN personnametype pnt1 ON pn1.personnametype_id = pnt1.id
        LEFT JOIN ranked_names pn2 
            ON pn2.person_id = p.id 
            AND pn2.rn = 1 
            AND pn2.personnametype_id = (SELECT id FROM personnametype WHERE description = 'MiddleName')
        LEFT JOIN personnametype pnt2 ON pn2.personnametype_id = pnt2.id
        LEFT JOIN ranked_names pn3 
            ON pn3.person_id = p.id 
            AND pn3.rn = 1 
            AND pn3.personnametype_id = (SELECT id FROM personnametype WHERE description = 'LastName')
        LEFT JOIN personnametype pnt3 ON pn3.personnametype_id = pnt3.id
        LEFT JOIN ranked_names pn4 
            ON pn4.person_id = p.id 
            AND pn4.rn = 1 
            AND pn4.personnametype_id = (SELECT id FROM personnametype WHERE description = 'Nickname')
        LEFT JOIN personnametype pnt4 ON pn4.personnametype_id = pnt4.id
        LEFT JOIN ranked_marital ms 
            ON ms.person_id = p.id 
            AND ms.rn = 1
        LEFT JOIN maritalstatustype mst ON ms.maritalstatustype_id = mst.id
        LEFT JOIN ranked_physical pc1 
            ON pc1.person_id = p.id 
            AND pc1.rn = 1 
            AND pc1.physicalcharacteristictype_id = (SELECT id FROM physicalcharacteristictype WHERE description = 'Height')
        LEFT JOIN physicalcharacteristictype pct1 ON pc1.physicalcharacteristictype_id = pct1.id
        LEFT JOIN ranked_physical pc2 
            ON pc2.person_id = p.id 
            AND pc2.rn = 1 
            AND pc2.physicalcharacteristictype_id = (SELECT id FROM physicalcharacteristictype WHERE description = 'Weight')
        LEFT JOIN physicalcharacteristictype pct2 ON pc2.physicalcharacteristictype_id = pct2.id
        LEFT JOIN ranked_citizenship c 
            ON c.person_id = p.id 
            AND c.rn = 1
        LEFT JOIN country co ON c.country_id = co.id
        ORDER BY p.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Fetched {len(results)} persons")
    return [PersonOut(**result) for result in results]

async def update_person(person_id: int, person: PersonUpdate) -> Optional[PersonOut]:
    async with database.transaction():
        try:
            # Update person table
            query_person = """
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
            result = await database.fetch_one(query=query_person, values={
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

            # Update personname for fname
            if person.fname:
                query_fname = """
                    INSERT INTO personname (person_id, name, personnametype_id, fromdate)
                    VALUES (:person_id, :name, (SELECT id FROM personnametype WHERE description = 'FirstName'), CURRENT_DATE)
                """
                await database.execute(query_fname, values={"person_id": person_id, "name": person.fname})

            # Update personname for mname
            if person.mname:
                query_mname = """
                    INSERT INTO personname (person_id, name, personnametype_id, fromdate)
                    VALUES (:person_id, :name, (SELECT id FROM personnametype WHERE description = 'MiddleName'), CURRENT_DATE)
                """
                await database.execute(query_mname, values={"person_id": person_id, "name": person.mname})

            # Update personname for lname
            if person.lname:
                query_lname = """
                    INSERT INTO personname (person_id, name, personnametype_id, fromdate)
                    VALUES (:person_id, :name, (SELECT id FROM personnametype WHERE description = 'LastName'), CURRENT_DATE)
                """
                await database.execute(query_lname, values={"person_id": person_id, "name": person.lname})

            # Update personname for nickname
            if person.nickname:
                query_nickname = """
                    INSERT INTO personname (person_id, name, personnametype_id, fromdate)
                    VALUES (:person_id, :name, (SELECT id FROM personnametype WHERE description = 'Nickname'), CURRENT_DATE)
                """
                await database.execute(query_nickname, values={"person_id": person_id, "name": person.nickname})

            # Update maritalstatus
            if person.marital_status_type_id:
                query_marital = """
                    INSERT INTO maritalstatus (person_id, maritalstatustype_id, fromdate)
                    VALUES (:person_id, :maritalstatustype_id, CURRENT_DATE)
                """
                await database.execute(query_marital, values={
                    "person_id": person_id,
                    "maritalstatustype_id": person.marital_status_type_id
                })

            # Update physicalcharacteristic for height
            if person.height_val:
                query_height = """
                    INSERT INTO physicalcharacteristic (person_id, val, physicalcharacteristictype_id, fromdate)
                    VALUES (:person_id, :val, (SELECT id FROM physicalcharacteristictype WHERE description = 'Height'), CURRENT_DATE)
                """
                await database.execute(query_height, values={"person_id": person_id, "val": person.height_val})

            # Update physicalcharacteristic for weight
            if person.weight_val:
                query_weight = """
                    INSERT INTO physicalcharacteristic (person_id, val, physicalcharacteristictype_id, fromdate)
                    VALUES (:person_id, :val, (SELECT id FROM physicalcharacteristictype WHERE description = 'Weight'), CURRENT_DATE)
                """
                await database.execute(query_weight, values={"person_id": person_id, "val": person.weight_val})

            # Update citizenship
            if person.country_id:
                query_citizenship = """
                    INSERT INTO citizenship (person_id, country_id, fromdate)
                    VALUES (:person_id, :country_id, CURRENT_DATE)
                """
                await database.execute(query_citizenship, values={"person_id": person_id, "country_id": person.country_id})

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