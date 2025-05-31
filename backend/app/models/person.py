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
                    id, personal_id_number, birthdate, mothermaidenname, 
                    totalyearworkexperience, comment, gender_type_id
                )
                VALUES (
                    :id, :personal_id_number, :birthdate, :mothermaidenname, 
                    :totalyearworkexperience, :comment, :gender_type_id
                )
                RETURNING id, personal_id_number, birthdate, mothermaidenname, 
                          totalyearworkexperience, comment, gender_type_id
            """
            result = await database.fetch_one(query=query_person, values={
                "id": new_id,
                "personal_id_number": person.personal_id_number,
                "birthdate": person.birthdate,
                "mothermaidenname": person.mothermaidenname,
                "totalyearworkexperience": person.totalyearworkexperience,
                "comment": person.comment,
                "gender_type_id": person.gender_type_id
            })
            logger.info(f"สร้างบุคคล: id={result['id']}")
            return PersonOut(**result)
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการสร้างบุคคล: {str(e)}")
            raise

async def get_person(person_id: int) -> Optional[PersonOut]:
    query = """
        SELECT id, personal_id_number, birthdate, mothermaidenname, 
               totalyearworkexperience, comment, gender_type_id
        FROM person WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": person_id})
    if not result:
        logger.warning(f"ไม่พบบุคคล: id={person_id}")
        return None
    logger.info(f"ดึงข้อมูลบุคคล: id={result['id']}")
    return PersonOut(**result)

async def get_all_persons() -> List[PersonOut]:
    query = """
        SELECT id, personal_id_number, birthdate, mothermaidenname, 
               totalyearworkexperience, comment, gender_type_id
        FROM person ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"ดึงข้อมูล {len(results)} บุคคล")
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
        RETURNING id, personal_id_number, birthdate, mothermaidenname, 
                  totalyearworkexperience, comment, gender_type_id
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
            logger.warning(f"ไม่พบบุคคลสำหรับอัปเดต: id={person_id}")
            return None
        logger.info(f"อัปเดตบุคคล: id={result['id']}")
        return PersonOut(**result)
    except Exception as e:
        logger.error(f"ข้อผิดพลาดในการอัปเดตบุคคล: {str(e)}")
        raise

async def delete_person(person_id: int) -> bool:
    # ตรวจสอบว่าบุคคลถูกอ้างอิงในตารางที่เกี่ยวข้องหรือไม่
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
        logger.warning(f"ไม่สามารถลบบุคคล: id={person_id}, ถูกอ้างอิงในตารางที่เกี่ยวข้อง")
        return False

    async with database.transaction():
        try:
            # ลบจาก person
            query_person = """
                DELETE FROM person WHERE id = :id
                RETURNING id
            """
            person_result = await database.fetch_one(query=query_person, values={"id": person_id})
            if not person_result:
                logger.warning(f"ไม่พบบุคคลสำหรับลบ: id={person_id}")
                return False

            # ลบจาก party
            query_party = """
                DELETE FROM party WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_party, values={"id": person_id})

            logger.info(f"ลบบุคคล: id={person_id}")
            return True
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการลบบุคคล: {str(e)}")
            raise