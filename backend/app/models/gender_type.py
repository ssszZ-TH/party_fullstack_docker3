from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.gender_type import GenderTypeCreate, GenderTypeUpdate, GenderTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_gender_type(gender_type: GenderTypeCreate) -> Optional[GenderTypeOut]:
    query = """
        SELECT id, description FROM gender_type WHERE description = :description
    """
    existing = await database.fetch_one(query=query, values={"description": gender_type.description})
    if existing:
        logger.warning(f"Gender type with description '{gender_type.description}' already exists")
        return None

    query = """
        INSERT INTO gender_type (description)
        VALUES (:description)
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": gender_type.description})
        logger.info(f"สร้างประเภทเพศ: id={result['id']}, description={result['description']}")
        return GenderTypeOut(**result)
    except Exception as e:
        logger.error(f"ข้อผิดพลาดในการสร้างประเภทเพศ: {str(e)}")
        raise

async def get_gender_type(gender_type_id: int) -> Optional[GenderTypeOut]:
    query = """
        SELECT id, description FROM gender_type WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": gender_type_id})
    if not result:
        logger.warning(f"ไม่พบประเภทเพศ: id={gender_type_id}")
        return None
    logger.info(f"ดึงข้อมูลประเภทเพศ: id={result['id']}, description={result['description']}")
    return GenderTypeOut(**result)

async def get_all_gender_types() -> List[GenderTypeOut]:
    query = """
        SELECT id, description FROM gender_type ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"ดึงข้อมูล {len(results)} ประเภทเพศ")
    return [GenderTypeOut(**result) for result in results]

async def update_gender_type(gender_type_id: int, gender_type: GenderTypeUpdate) -> Optional[GenderTypeOut]:
    if gender_type.description:
        query = """
            SELECT id, description FROM gender_type WHERE description = :description AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"description": gender_type.description, "id": gender_type_id})
        if existing:
            logger.warning(f"ประเภทเพศที่มี description '{gender_type.description}' มีอยู่แล้ว")
            return None

    query = """
        UPDATE gender_type
        SET description = COALESCE(:description, description)
        WHERE id = :id
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": gender_type.description, "id": gender_type_id})
        if not result:
            logger.warning(f"ไม่พบประเภทเพศสำหรับอัปเดต: id={gender_type_id}")
            return None
        logger.info(f"อัปเดตประเภทเพศ: id={result['id']}, description={result['description']}")
        return GenderTypeOut(**result)
    except Exception as e:
        logger.error(f"ข้อผิดพลาดในการอัปเดตประเภทเพศ: {str(e)}")
        raise

async def delete_gender_type(gender_type_id: int) -> bool:
    # ตรวจสอบว่า gender_type_id ถูกอ้างอิงในตาราง person หรือไม่
    query_check = """
        SELECT id FROM person WHERE gender_type_id = :id LIMIT 1
    """
    referenced = await database.fetch_one(query=query_check, values={"id": gender_type_id})
    if referenced:
        logger.warning(f"ไม่สามารถลบประเภทเพศ: id={gender_type_id}, ถูกอ้างอิงในตาราง person")
        return False

    query = """
        DELETE FROM gender_type WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": gender_type_id})
    if not result:
        logger.warning(f"ไม่พบประเภทเพศสำหรับลบ: id={gender_type_id}")
        return False
    logger.info(f"ลบประเภทเพศ: id={gender_type_id}")
    return True