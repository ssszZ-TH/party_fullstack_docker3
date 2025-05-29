### File: /app/schemas/corporation.py
```python
from pydantic import BaseModel, constr
from typing import Optional

class CorporationCreate(BaseModel):
    name_en: constr(max_length=128)
    name_th: constr(max_length=128)
    federal_tax_id_number: Optional[constr(max_length=64)] = None

class CorporationUpdate(BaseModel):
    name_en: Optional[constr(max_length=128)] = None
    name_th: Optional[constr(max_length=128)] = None
    federal_tax_id_number: Optional[constr(max_length=64)] = None

class CorporationOut(BaseModel):
    id: int
    name_en: Optional[str] = None
    name_th: Optional[str] = None
    federal_tax_id_number: Optional[str] = None

    class Config:
        from_attributes = True
```

### File: /app/models/corporation.py
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.corporation import CorporationCreate, CorporationUpdate, CorporationOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_corporation(corporation: CorporationCreate) -> Optional[CorporationOut]:
    async with database.transaction():
        try:
            # 1. Insert into party
            query_party = """
                INSERT INTO party (id)
                VALUES (DEFAULT)
                RETURNING id
            """
            party_result = await database.fetch_one(query=query_party)
            party_id = party_result["id"]

            # 2. Insert into organization
            query_organization = """
                INSERT INTO organization (id, name_en, name_th)
                VALUES (:id, :name_en, :name_th)
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={
                "id": party_id,
                "name_en": corporation.name_en,
                "name_th": corporation.name_th
            })

            # 3. Insert into legal_organization
            query_legal = """
                INSERT INTO legal_organization (id, federal_tax_id_number)
                VALUES (:id, :federal_tax_id_number)
                RETURNING id
            """
            await database.fetch_one(query=query_legal, values={
                "id": party_id,
                "federal_tax_id_number": corporation.federal_tax_id_number
            })

            # 4. Insert into corporation
            query_corporation = """
                INSERT INTO corporation (id)
                VALUES (:id)
                RETURNING id
            """
            result = await database.fetch_one(query=query_corporation, values={"id": party_id})
            logger.info(f"สร้าง corporation: id={result['id']}")
            return CorporationOut(
                id=result['id'],
                name_en=corporation.name_en,
                name_th=corporation.name_th,
                federal_tax_id_number=corporation.federal_tax_id_number
            )
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการสร้าง corporation: {str(e)}")
            raise

async def get_corporation(corporation_id: int) -> Optional[CorporationOut]:
    query = """
        SELECT c.id, o.name_en, o.name_th, lo.federal_tax_id_number
        FROM corporation c
        JOIN legal_organization lo ON c.id = lo.id
        JOIN organization o ON lo.id = o.id
        JOIN party p ON o.id = p.id
        WHERE c.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": corporation_id})
    if not result:
        logger.warning(f"ไม่พบ corporation: id={corporation_id}")
        return None
    logger.info(f"ดึงข้อมูล corporation: id={result['id']}")
    return CorporationOut(**result)

async def get_all_corporations() -> List[CorporationOut]:
    query = """
        SELECT c.id, o.name_en, o.name_th, lo.federal_tax_id_number
        FROM corporation c
        JOIN legal_organization lo ON c.id = lo.id
        JOIN organization o ON lo.id = o.id
        JOIN party p ON o.id = p.id
        ORDER BY c.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"ดึงข้อมูล {len(results)} corporations")
    return [CorporationOut(**result) for result in results]

async def update_corporation(corporation_id: int, corporation: CorporationUpdate) -> Optional[CorporationOut]:
    async with database.transaction():
        try:
            # Update organization
            query_organization = """
                UPDATE organization
                SET name_en = COALESCE(:name_en, name_en),
                    name_th = COALESCE(:name_th, name_th)
                WHERE id = :id
                RETURNING id
            """
            org_result = await database.fetch_one(query=query_organization, values={
                "name_en": corporation.name_en,
                "name_th": corporation.name_th,
                "id": corporation_id
            })
            if not org_result:
                logger.warning(f"ไม่พบ corporation สำหรับอัปเดต: id={corporation_id}")
                return None

            # Update legal_organization
            query_legal = """
                UPDATE legal_organization
                SET federal_tax_id_number = COALESCE(:federal_tax_id_number, federal_tax_id_number)
                WHERE id = :id
                RETURNING id, federal_tax_id_number
            """
            legal_result = await database.fetch_one(query=query_legal, values={
                "federal_tax_id_number": corporation.federal_tax_id_number,
                "id": corporation_id
            })

            # Fetch updated data
            query_fetch = """
                SELECT c.id, o.name_en, o.name_th, lo.federal_tax_id_number
                FROM corporation c
                JOIN legal_organization lo ON c.id = lo.id
                JOIN organization o ON lo.id = o.id
                WHERE c.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": corporation_id})
            logger.info(f"อัปเดต corporation: id={result['id']}")
            return CorporationOut(**result)
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการอัปเดต corporation: {str(e)}")
            raise

async def delete_corporation(corporation_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from corporation
            query_corporation = """
                DELETE FROM corporation WHERE id = :id
                RETURNING id
            """
            corporation_result = await database.fetch_one(query=query_corporation, values={"id": corporation_id})
            if not corporation_result:
                logger.warning(f"ไม่พบ corporation สำหรับลบ: id={corporation_id}")
                return False

            # Delete from legal_organization
            query_legal = """
                DELETE FROM legal_organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_legal, values={"id": corporation_id})

            # Delete from organization
            query_organization = """
                DELETE FROM organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={"id": corporation_id})

            # Delete from party
            query_party = """
                DELETE FROM party WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_party, values={"id": corporation_id})

            logger.info(f"ลบ corporation: id={corporation_id}")
            return True
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการลบ corporation: {str(e)}")
            raise
```

### File: /app/controllers/corporation.py
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.corporation import (
    create_corporation, get_corporation, get_all_corporations,
    update_corporation, delete_corporation
)
from app.schemas.corporation import CorporationCreate, CorporationUpdate, CorporationOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/corporation", tags=["corporation"])

@router.post("/", response_model=CorporationOut)
async def create_corporation_endpoint(corporation: CorporationCreate, current_user: dict = Depends(get_current_user)):
    result = await create_corporation(corporation)
    if not result:
        logger.warning(f"ไม่สามารถสร้าง corporation")
        raise HTTPException(status_code=400, detail="ไม่สามารถสร้าง corporation")
    logger.info(f"สร้าง corporation: id={result.id}")
    return result

@router.get("/{corporation_id}", response_model=CorporationOut)
async def get_corporation_endpoint(corporation_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_corporation(corporation_id)
    if not result:
        logger.warning(f"ไม่พบ corporation: id={corporation_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ corporation")
    logger.info(f"ดึงข้อมูล corporation: id={result.id}")
    return result

@router.get("/", response_model=List[CorporationOut])
async def get_all_corporations_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_corporations()
    logger.info(f"ดึงข้อมูล {len(results)} corporations")
    return results

@router.put("/{corporation_id}", response_model=CorporationOut)
async def update_corporation_endpoint(corporation_id: int, corporation: CorporationUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_corporation(corporation_id, corporation)
    if not result:
        logger.warning(f"ไม่สามารถอัปเดต corporation: id={corporation_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ corporation")
    logger.info(f"อัปเดต corporation: id={result.id}")
    return result

@router.delete("/{corporation_id}")
async def delete_corporation_endpoint(corporation_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_corporation(corporation_id)
    if not result:
        logger.warning(f"ไม่พบ corporation สำหรับลบ: id={corporation_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ corporation")
    logger.info(f"ลบ corporation: id={corporation_id}")
    return {"message": "ลบ corporation เรียบร้อย"}
```

### File: /app/schemas/government_agency.py
```python
from pydantic import BaseModel, constr
from typing import Optional

class GovernmentAgencyCreate(BaseModel):
    name_en: constr(max_length=128)
    name_th: constr(max_length=128)
    federal_tax_id_number: Optional[constr(max_length=64)] = None

class GovernmentAgencyUpdate(BaseModel):
    name_en: Optional[constr(max_length=128)] = None
    name_th: Optional[constr(max_length=128)] = None
    federal_tax_id_number: Optional[constr(max_length=64)] = None

class GovernmentAgencyOut(BaseModel):
    id: int
    name_en: Optional[str] = None
    name_th: Optional[str] = None
    federal_tax_id_number: Optional[str] = None

    class Config:
        from_attributes = True
```

### File: /app/models/government_agency.py
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.government_agency import GovernmentAgencyCreate, GovernmentAgencyUpdate, GovernmentAgencyOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_government_agency(government_agency: GovernmentAgencyCreate) -> Optional[GovernmentAgencyOut]:
    async with database.transaction():
        try:
            # 1. Insert into party
            query_party = """
                INSERT INTO party (id)
                VALUES (DEFAULT)
                RETURNING id
            """
            party_result = await database.fetch_one(query=query_party)
            party_id = party_result["id"]

            # 2. Insert into organization
            query_organization = """
                INSERT INTO organization (id, name_en, name_th)
                VALUES (:id, :name_en, :name_th)
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={
                "id": party_id,
                "name_en": government_agency.name_en,
                "name_th": government_agency.name_th
            })

            # 3. Insert into legal_organization
            query_legal = """
                INSERT INTO legal_organization (id, federal_tax_id_number)
                VALUES (:id, :federal_tax_id_number)
                RETURNING id
            """
            await database.fetch_one(query=query_legal, values={
                "id": party_id,
                "federal_tax_id_number": government_agency.federal_tax_id_number
            })

            # 4. Insert into government_agency
            query_government = """
                INSERT INTO government_agency (id)
                VALUES (:id)
                RETURNING id
            """
            result = await database.fetch_one(query=query_government, values={"id": party_id})
            logger.info(f"สร้าง government agency: id={result['id']}")
            return GovernmentAgencyOut(
                id=result['id'],
                name_en=government_agency.name_en,
                name_th=government_agency.name_th,
                federal_tax_id_number=government_agency.federal_tax_id_number
            )
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการสร้าง government agency: {str(e)}")
            raise

async def get_government_agency(government_agency_id: int) -> Optional[GovernmentAgencyOut]:
    query = """
        SELECT ga.id, o.name_en, o.name_th, lo.federal_tax_id_number
        FROM government_agency ga
        JOIN legal_organization lo ON ga.id = lo.id
        JOIN organization o ON lo.id = o.id
        JOIN party p ON o.id = p.id
        WHERE ga.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": government_agency_id})
    if not result:
        logger.warning(f"ไม่พบ government agency: id={government_agency_id}")
        return None
    logger.info(f"ดึงข้อมูล government agency: id={result['id']}")
    return GovernmentAgencyOut(**result)

async def get_all_government_agencies() -> List[GovernmentAgencyOut]:
    query = """
        SELECT ga.id, o.name_en, o.name_th, lo.federal_tax_id_number
        FROM government_agency ga
        JOIN legal_organization lo ON ga.id = lo.id
        JOIN organization o ON lo.id = o.id
        JOIN party p ON o.id = p.id
        ORDER BY ga.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"ดึงข้อมูล {len(results)} government agencies")
    return [GovernmentAgencyOut(**result) for result in results]

async def update_government_agency(government_agency_id: int, government_agency: GovernmentAgencyUpdate) -> Optional[GovernmentAgencyOut]:
    async with database.transaction():
        try:
            # Update organization
            query_organization = """
                UPDATE organization
                SET name_en = COALESCE(:name_en, name_en),
                    name_th = COALESCE(:name_th, name_th)
                WHERE id = :id
                RETURNING id
            """
            org_result = await database.fetch_one(query=query_organization, values={
                "name_en": government_agency.name_en,
                "name_th": government_agency.name_th,
                "id": government_agency_id
            })
            if not org_result:
                logger.warning(f"ไม่พบ government agency สำหรับอัปเดต: id={government_agency_id}")
                return None

            # Update legal_organization
            query_legal = """
                UPDATE legal_organization
                SET federal_tax_id_number = COALESCE(:federal_tax_id_number, federal_tax_id_number)
                WHERE id = :id
                RETURNING id, federal_tax_id_number
            """
            legal_result = await database.fetch_one(query=query_legal, values={
                "federal_tax_id_number": government_agency.federal_tax_id_number,
                "id": government_agency_id
            })

            # Fetch updated data
            query_fetch = """
                SELECT ga.id, o.name_en, o.name_th, lo.federal_tax_id_number
                FROM government_agency ga
                JOIN legal_organization lo ON ga.id = lo.id
                JOIN organization o ON lo.id = o.id
                WHERE ga.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": government_agency_id})
            logger.info(f"อัปเดต government agency: id={result['id']}")
            return GovernmentAgencyOut(**result)
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการอัปเดต government agency: {str(e)}")
            raise

async def delete_government_agency(government_agency_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from government_agency
            query_government = """
                DELETE FROM government_agency WHERE id = :id
                RETURNING id
            """
            government_result = await database.fetch_one(query=query_government, values={"id": government_agency_id})
            if not government_result:
                logger.warning(f"ไม่พบ government agency สำหรับลบ: id={government_agency_id}")
                return False

            # Delete from legal_organization
            query_legal = """
                DELETE FROM legal_organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_legal, values={"id": government_agency_id})

            # Delete from organization
            query_organization = """
                DELETE FROM organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={"id": government_agency_id})

            # Delete from party
            query_party = """
                DELETE FROM party WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_party, values={"id": government_agency_id})

            logger.info(f"ลบ government agency: id={government_agency_id}")
            return True
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการลบ government agency: {str(e)}")
            raise
```

### File: /app/controllers/government_agency.py
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.government_agency import (
    create_government_agency, get_government_agency, get_all_government_agencies,
    update_government_agency, delete_government_agency
)
from app.schemas.government_agency import GovernmentAgencyCreate, GovernmentAgencyUpdate, GovernmentAgencyOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/governmentagency", tags=["government_agency"])

@router.post("/", response_model=GovernmentAgencyOut)
async def create_government_agency_endpoint(government_agency: GovernmentAgencyCreate, current_user: dict = Depends(get_current_user)):
    result = await create_government_agency(government_agency)
    if not result:
        logger.warning(f"ไม่สามารถสร้าง government agency")
        raise HTTPException(status_code=400, detail="ไม่สามารถสร้าง government agency")
    logger.info(f"สร้าง government agency: id={result.id}")
    return result

@router.get("/{government_agency_id}", response_model=GovernmentAgencyOut)
async def get_government_agency_endpoint(government_agency_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_government_agency(government_agency_id)
    if not result:
        logger.warning(f"ไม่พบ government agency: id={government_agency_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ government agency")
    logger.info(f"ดึงข้อมูล government agency: id={result.id}")
    return result

@router.get("/", response_model=List[GovernmentAgencyOut])
async def get_all_government_agencies_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_government_agencies()
    logger.info(f"ดึงข้อมูล {len(results)} government agencies")
    return results

@router.put("/{government_agency_id}", response_model=GovernmentAgencyOut)
async def update_government_agency_endpoint(government_agency_id: int, government_agency: GovernmentAgencyUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_government_agency(government_agency_id, government_agency)
    if not result:
        logger.warning(f"ไม่สามารถอัปเดต government agency: id={government_agency_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ government agency")
    logger.info(f"อัปเดต government agency: id={result.id}")
    return result

@router.delete("/{government_agency_id}")
async def delete_government_agency_endpoint(government_agency_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_government_agency(government_agency_id)
    if not result:
        logger.warning(f"ไม่พบ government agency สำหรับลบ: id={government_agency_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ government agency")
    logger.info(f"ลบ government agency: id={government_agency_id}")
    return {"message": "ลบ government agency เรียบร้อย"}
```

### File: /app/schemas/team.py
```python
from pydantic import BaseModel, constr
from typing import Optional

class TeamCreate(BaseModel):
    name_en: constr(max_length=128)
    name_th: constr(max_length=128)

class TeamUpdate(BaseModel):
    name_en: Optional[constr(max_length=128)] = None
    name_th: Optional[constr(max_length=128)] = None

class TeamOut(BaseModel):
    id: int
    name_en: Optional[str] = None
    name_th: Optional[str] = None

    class Config:
        from_attributes = True
```

### File: /app/models/team.py
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.team import TeamCreate, TeamUpdate, TeamOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_team(team: TeamCreate) -> Optional[TeamOut]:
    async with database.transaction():
        try:
            # 1. Insert into party
            query_party = """
                INSERT INTO party (id)
                VALUES (DEFAULT)
                RETURNING id
            """
            party_result = await database.fetch_one(query=query_party)
            party_id = party_result["id"]

            # 2. Insert into organization
            query_organization = """
                INSERT INTO organization (id, name_en, name_th)
                VALUES (:id, :name_en, :name_th)
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={
                "id": party_id,
                "name_en": team.name_en,
                "name_th": team.name_th
            })

            # 3. Insert into informal_organization
            query_informal = """
                INSERT INTO informal_organization (id)
                VALUES (:id)
                RETURNING id
            """
            await database.fetch_one(query=query_informal, values={"id": party_id})

            # 4. Insert into team
            query_team = """
                INSERT INTO team (id)
                VALUES (:id)
                RETURNING id
            """
            result = await database.fetch_one(query=query_team, values={"id": party_id})
            logger.info(f"สร้าง team: id={result['id']}")
            return TeamOut(
                id=result['id'],
                name_en=team.name_en,
                name_th=team.name_th
            )
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการสร้าง team: {str(e)}")
            raise

async def get_team(team_id: int) -> Optional[TeamOut]:
    query = """
        SELECT t.id, o.name_en, o.name_th
        FROM team t
        JOIN informal_organization io ON t.id = io.id
        JOIN organization o ON io.id = o.id
        JOIN party p ON o.id = p.id
        WHERE t.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": team_id})
    if not result:
        logger.warning(f"ไม่พบ team: id={team_id}")
        return None
    logger.info(f"ดึงข้อมูล team: id={result['id']}")
    return TeamOut(**result)

async def get_all_teams() -> List[TeamOut]:
    query = """
        SELECT t.id, o.name_en, o.name_th
        FROM team t
        JOIN informal_organization io ON t.id = io.id
        JOIN organization o ON io.id = o.id
        JOIN party p ON o.id = p.id
        ORDER BY t.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"ดึงข้อมูล {len(results)} teams")
    return [TeamOut(**result) for result in results]

async def update_team(team_id: int, team: TeamUpdate) -> Optional[TeamOut]:
    async with database.transaction():
        try:
            # Update organization
            query_organization = """
                UPDATE organization
                SET name_en = COALESCE(:name_en, name_en),
                    name_th = COALESCE(:name_th, name_th)
                WHERE id = :id
                RETURNING id, name_en, name_th
            """
            result = await database.fetch_one(query=query_organization, values={
                "name_en": team.name_en,
                "name_th": team.name_th,
                "id": team_id
            })
            if not result:
                logger.warning(f"ไม่พบ team สำหรับอัปเดต: id={team_id}")
                return None
            logger.info(f"อัปเดต team: id={result['id']}")
            return TeamOut(**result)
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการอัปเดต team: {str(e)}")
            raise

async def delete_team(team_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from team
            query_team = """
                DELETE FROM team WHERE id = :id
                RETURNING id
            """
            team_result = await database.fetch_one(query=query_team, values={"id": team_id})
            if not team_result:
                logger.warning(f"ไม่พบ team สำหรับลบ: id={team_id}")
                return False

            # Delete from informal_organization
            query_informal = """
                DELETE FROM informal_organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_informal, values={"id": team_id})

            # Delete from organization
            query_organization = """
                DELETE FROM organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={"id": team_id})

            # Delete from party
            query_party = """
                DELETE FROM party WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_party, values={"id": team_id})

            logger.info(f"ลบ team: id={team_id}")
            return True
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการลบ team: {str(e)}")
            raise
```

### File: /app/controllers/team.py
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.team import (
    create_team, get_team, get_all_teams,
    update_team, delete_team
)
from app.schemas.team import TeamCreate, TeamUpdate, TeamOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/team", tags=["team"])

@router.post("/", response_model=TeamOut)
async def create_team_endpoint(team: TeamCreate, current_user: dict = Depends(get_current_user)):
    result = await create_team(team)
    if not result:
        logger.warning(f"ไม่สามารถสร้าง team")
        raise HTTPException(status_code=400, detail="ไม่สามารถสร้าง team")
    logger.info(f"สร้าง team: id={result.id}")
    return result

@router.get("/{team_id}", response_model=TeamOut)
async def get_team_endpoint(team_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_team(team_id)
    if not result:
        logger.warning(f"ไม่พบ team: id={team_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ team")
    logger.info(f"ดึงข้อมูล team: id={result.id}")
    return result

@router.get("/", response_model=List[TeamOut])
async def get_all_teams_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_teams()
    logger.info(f"ดึงข้อมูล {len(results)} teams")
    return results

@router.put("/{team_id}", response_model=TeamOut)
async def update_team_endpoint(team_id: int, team: TeamUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_team(team_id, team)
    if not result:
        logger.warning(f"ไม่สามารถอัปเดต team: id={team_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ team")
    logger.info(f"อัปเดต team: id={result.id}")
    return result

@router.delete("/{team_id}")
async def delete_team_endpoint(team_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_team(team_id)
    if not result:
        logger.warning(f"ไม่พบ team สำหรับลบ: id={team_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ team")
    logger.info(f"ลบ team: id={team_id}")
    return {"message": "ลบ team เรียบร้อย"}
```

### File: /app/schemas/family.py
```python
from pydantic import BaseModel, constr
from typing import Optional

class FamilyCreate(BaseModel):
    name_en: constr(max_length=128)
    name_th: constr(max_length=128)

class FamilyUpdate(BaseModel):
    name_en: Optional[constr(max_length=128)] = None
    name_th: Optional[constr(max_length=128)] = None

class FamilyOut(BaseModel):
    id: int
    name_en: Optional[str] = None
    name_th: Optional[str] = None

    class Config:
        from_attributes = True
```

### File: /app/models/family.py
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.family import FamilyCreate, FamilyUpdate, FamilyOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_family(family: FamilyCreate) -> Optional[FamilyOut]:
    async with database.transaction():
        try:
            # 1. Insert into party
            query_party = """
                INSERT INTO party (id)
                VALUES (DEFAULT)
                RETURNING id
            """
            party_result = await database.fetch_one(query=query_party)
            party_id = party_result["id"]

            # 2. Insert into organization
            query_organization = """
                INSERT INTO organization (id, name_en, name_th)
                VALUES (:id, :name_en, :name_th)
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={
                "id": party_id,
                "name_en": family.name_en,
                "name_th": family.name_th
            })

            # 3. Insert into informal_organization
            query_informal = """
                INSERT INTO informal_organization (id)
                VALUES (:id)
                RETURNING id
            """
            await database.fetch_one(query=query_informal, values={"id": party_id})

            # 4. Insert into family
            query_family = """
                INSERT INTO family (id)
                VALUES (:id)
                RETURNING id
            """
            result = await database.fetch_one(query=query_family, values={"id": party_id})
            logger.info(f"สร้าง family: id={result['id']}")
            return FamilyOut(
                id=result['id'],
                name_en=family.name_en,
                name_th=family.name_th
            )
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการสร้าง family: {str(e)}")
            raise

async def get_family(family_id: int) -> Optional[FamilyOut]:
    query = """
        SELECT f.id, o.name_en, o.name_th
        FROM family f
        JOIN informal_organization io ON f.id = io.id
        JOIN organization o ON io.id = o.id
        JOIN party p ON o.id = p.id
        WHERE f.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": family_id})
    if not result:
        logger.warning(f"ไม่พบ family: id={family_id}")
        return None
    logger.info(f"ดึงข้อมูล family: id={result['id']}")
    return FamilyOut(**result)

async def get_all_families() -> List[FamilyOut]:
    query = """
        SELECT f.id, o.name_en, o.name_th
        FROM family f
        JOIN informal_organization io ON f.id = io.id
        JOIN organization o ON io.id = o.id
        JOIN party p ON o.id = p.id
        ORDER BY f.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"ดึงข้อมูล {len(results)} families")
    return [FamilyOut(**result) for result in results]

async def update_family(family_id: int, family: FamilyUpdate) -> Optional[FamilyOut]:
    async with database.transaction():
        try:
            # Update organization
            query_organization = """
                UPDATE organization
                SET name_en = COALESCE(:name_en, name_en),
                    name_th = COALESCE(:name_th, name_th)
                WHERE id = :id
                RETURNING id, name_en, name_th
            """
            result = await database.fetch_one(query=query_organization, values={
                "name_en": family.name_en,
                "name_th": family.name_th,
                "id": family_id
            })
            if not result:
                logger.warning(f"ไม่พบ family สำหรับอัปเดต: id={family_id}")
                return None
            logger.info(f"อัปเดต family: id={result['id']}")
            return FamilyOut(**result)
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการอัปเดต family: {str(e)}")
            raise

async def delete_family(family_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from family
            query_family = """
                DELETE FROM family WHERE id = :id
                RETURNING id
            """
            family_result = await database.fetch_one(query=query_family, values={"id": family_id})
            if not family_result:
                logger.warning(f"ไม่พบ family สำหรับลบ: id={family_id}")
                return False

            # Delete from informal_organization
            query_informal = """
                DELETE FROM informal_organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_informal, values={"id": family_id})

            # Delete from organization
            query_organization = """
                DELETE FROM organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={"id": family_id})

            # Delete from party
            query_party = """
                DELETE FROM party WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_party, values={"id": family_id})

            logger.info(f"ลบ family: id={family_id}")
            return True
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการลบ family: {str(e)}")
            raise
```

### File: /app/controllers/family.py
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.family import (
    create_family, get_family, get_all_families,
    update_family, delete_family
)
from app.schemas.family import FamilyCreate, FamilyUpdate, FamilyOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/family", tags=["family"])

@router.post("/", response_model=FamilyOut)
async def create_family_endpoint(family: FamilyCreate, current_user: dict = Depends(get_current_user)):
    result = await create_family(family)
    if not result:
        logger.warning(f"ไม่สามารถสร้าง family")
        raise HTTPException(status_code=400, detail="ไม่สามารถสร้าง family")
    logger.info(f"สร้าง family: id={result.id}")
    return result

@router.get("/{family_id}", response_model=FamilyOut)
async def get_family_endpoint(family_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_family(family_id)
    if not result:
        logger.warning(f"ไม่พบ family: id={family_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ family")
    logger.info(f"ดึงข้อมูล family: id={result.id}")
    return result

@router.get("/", response_model=List[FamilyOut])
async def get_all_families_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_families()
    logger.info(f"ดึงข้อมูล {len(results)} families")
    return results

@router.put("/{family_id}", response_model=FamilyOut)
async def update_family_endpoint(family_id: int, family: FamilyUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_family(family_id, family)
    if not result:
        logger.warning(f"ไม่สามารถอัปเดต family: id={family_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ family")
    logger.info(f"อัปเดต family: id={result.id}")
    return result

@router.delete("/{family_id}")
async def delete_family_endpoint(family_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_family(family_id)
    if not result:
        logger.warning(f"ไม่พบ family สำหรับลบ: id={family_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ family")
    logger.info(f"ลบ family: id={family_id}")
    return {"message": "ลบ family เรียบร้อย"}
```

### File: /app/schemas/other_informal_organization.py
```python
from pydantic import BaseModel, constr
from typing import Optional

class OtherInformalOrganizationCreate(BaseModel):
    name_en: constr(max_length=128)
    name_th: constr(max_length=128)

class OtherInformalOrganizationUpdate(BaseModel):
    name_en: Optional[constr(max_length=128)] = None
    name_th: Optional[constr(max_length=128)] = None

class OtherInformalOrganizationOut(BaseModel):
    id: int
    name_en: Optional[str] = None
    name_th: Optional[str] = None

    class Config:
        from_attributes = True
```

### File: /app/models/other_informal_organization.py
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.other_informal_organization import OtherInformalOrganizationCreate, OtherInformalOrganizationUpdate, OtherInformalOrganizationOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_other_informal_organization(other_informal_organization: OtherInformalOrganizationCreate) -> Optional[OtherInformalOrganizationOut]:
    async with database.transaction():
        try:
            # 1. Insert into party
            query_party = """
                INSERT INTO party (id)
                VALUES (DEFAULT)
                RETURNING id
            """
            party_result = await database.fetch_one(query=query_party)
            party_id = party_result["id"]

            # 2. Insert into organization
            query_organization = """
                INSERT INTO organization (id, name_en, name_th)
                VALUES (:id, :name_en, :name_th)
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={
                "id": party_id,
                "name_en": other_informal_organization.name_en,
                "name_th": other_informal_organization.name_th
            })

            # 3. Insert into informal_organization
            query_informal = """
                INSERT INTO informal_organization (id)
                VALUES (:id)
                RETURNING id
            """
            await database.fetch_one(query=query_informal, values={"id": party_id})

            # 4. Insert into other_informal_organization
            query_other = """
                INSERT INTO other_informal_organization (id)
                VALUES (:id)
                RETURNING id
            """
            result = await database.fetch_one(query=query_other, values={"id": party_id})
            logger.info(f"สร้าง other informal organization: id={result['id']}")
            return OtherInformalOrganizationOut(
                id=result['id'],
                name_en=other_informal_organization.name_en,
                name_th=other_informal_organization.name_th
            )
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการสร้าง other informal organization: {str(e)}")
            raise

async def get_other_informal_organization(other_informal_organization_id: int) -> Optional[OtherInformalOrganizationOut]:
    query = """
        SELECT oio.id, o.name_en, o.name_th
        FROM other_informal_organization oio
        JOIN informal_organization io ON oio.id = io.id
        JOIN organization o ON io.id = o.id
        JOIN party p ON o.id = p.id
        WHERE oio.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": other_informal_organization_id})
    if not result:
        logger.warning(f"ไม่พบ other informal organization: id={other_informal_organization_id}")
        return None
    logger.info(f"ดึงข้อมูล other informal organization: id={result['id']}")
    return OtherInformalOrganizationOut(**result)

async def get_all_other_informal_organizations() -> List[OtherInformalOrganizationOut]:
    query = """
        SELECT oio.id, o.name_en, o.name_th
        FROM other_informal_organization oio
        JOIN informal_organization io ON oio.id = io.id
        JOIN organization o ON io.id = o.id
        JOIN party p ON o.id = p.id
        ORDER BY oio.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"ดึงข้อมูล {len(results)} other informal organizations")
    return [OtherInformalOrganizationOut(**result) for result in results]

async def update_other_informal_organization(other_informal_organization_id: int, other_informal_organization: OtherInformalOrganizationUpdate) -> Optional[OtherInformalOrganizationOut]:
    async with database.transaction():
        try:
            # Update organization
            query_organization = """
                UPDATE organization
                SET name_en = COALESCE(:name_en, name_en),
                    name_th = COALESCE(:name_th, name_th)
                WHERE id = :id
                RETURNING id, name_en, name_th
            """
            result = await database.fetch_one(query=query_organization, values={
                "name_en": other_informal_organization.name_en,
                "name_th": other_informal_organization.name_th,
                "id": other_informal_organization_id
            })
            if not result:
                logger.warning(f"ไม่พบ other informal organization สำหรับอัปเดต: id={other_informal_organization_id}")
                return None
            logger.info(f"อัปเดต other informal organization: id={result['id']}")
            return OtherInformalOrganizationOut(**result)
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการอัปเดต other informal organization: {str(e)}")
            raise

async def delete_other_informal_organization(other_informal_organization_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from other_informal_organization
            query_other = """
                DELETE FROM other_informal_organization WHERE id = :id
                RETURNING id
            """
            other_result = await database.fetch_one(query=query_other, values={"id": other_informal_organization_id})
            if not other_result:
                logger.warning(f"ไม่พบ other informal organization สำหรับลบ: id={other_informal_organization_id}")
                return False

            # Delete from informal_organization
            query_informal = """
                DELETE FROM informal_organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_informal, values={"id": other_informal_organization_id})

            # Delete from organization
            query_organization = """
                DELETE FROM organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={"id": other_informal_organization_id})

            # Delete from party
            query_party = """
                DELETE FROM party WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_party, values={"id": other_informal_organization_id})

            logger.info(f"ลบ other informal organization: id={other_informal_organization_id}")
            return True
        except Exception as e:
            logger.error(f"ข้อผิดพลาดในการลบ other informal organization: {str(e)}")
            raise
```

### File: /app/controllers/other_informal_organization.py
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.other_informal_organization import (
    create_other_informal_organization, get_other_informal_organization, get_all_other_informal_organizations,
    update_other_informal_organization, delete_other_informal_organization
)
from app.schemas.other_informal_organization import OtherInformalOrganizationCreate, OtherInformalOrganizationUpdate, OtherInformalOrganizationOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/otherinformalorganization", tags=["other_informal_organization"])

@router.post("/", response_model=OtherInformalOrganizationOut)
async def create_other_informal_organization_endpoint(other_informal_organization: OtherInformalOrganizationCreate, current_user: dict = Depends(get_current_user)):
    result = await create_other_informal_organization(other_informal_organization)
    if not result:
        logger.warning(f"ไม่สามารถสร้าง other informal organization")
        raise HTTPException(status_code=400, detail="ไม่สามารถสร้าง other informal organization")
    logger.info(f"สร้าง other informal organization: id={result.id}")
    return result

@router.get("/{other_informal_organization_id}", response_model=OtherInformalOrganizationOut)
async def get_other_informal_organization_endpoint(other_informal_organization_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_other_informal_organization(other_informal_organization_id)
    if not result:
        logger.warning(f"ไม่พบ other informal organization: id={other_informal_organization_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ other informal organization")
    logger.info(f"ดึงข้อมูล other informal organization: id={result.id}")
    return result

@router.get("/", response_model=List[OtherInformalOrganizationOut])
async def get_all_other_informal_organizations_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_other_informal_organizations()
    logger.info(f"ดึงข้อมูล {len(results)} other informal organizations")
    return results

@router.put("/{other_informal_organization_id}", response_model=OtherInformalOrganizationOut)
async def update_other_informal_organization_endpoint(other_informal_organization_id: int, other_informal_organization: OtherInformalOrganizationUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_other_informal_organization(other_informal_organization_id, other_informal_organization)
    if not result:
        logger.warning(f"ไม่สามารถอัปเดต other informal organization: id={other_informal_organization_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ other informal organization")
    logger.info(f"อัปเดต other informal organization: id={result.id}")
    return result

@router.delete("/{other_informal_organization_id}")
async def delete_other_informal_organization_endpoint(other_informal_organization_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_other_informal_organization(other_informal_organization_id)
    if not result:
        logger.warning(f"ไม่พบ other informal organization สำหรับลบ: id={other_informal_organization_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ other informal organization")
    logger.info(f"ลบ other informal organization: id={other_informal_organization_id}")
    return {"message": "ลบ other informal organization เรียบร้อย"}
```