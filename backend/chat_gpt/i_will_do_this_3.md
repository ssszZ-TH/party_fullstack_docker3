### File: /app/schemas/legal_organization.py
### Part: Schema - Pydantic models for legal_organization CRUD
```python
from pydantic import BaseModel, constr
from typing import Optional

class LegalOrganizationCreate(BaseModel):
    name_en: constr(max_length=128)
    name_th: constr(max_length=128)
    federal_tax_id_number: Optional[constr(max_length=64)] = None

class LegalOrganizationUpdate(BaseModel):
    name_en: Optional[constr(max_length=128)] = None
    name_th: Optional[constr(max_length=128)] = None
    federal_tax_id_number: Optional[constr(max_length=64)] = None

class LegalOrganizationOut(BaseModel):
    id: int
    name_en: str
    name_th: str
    federal_tax_id_number: Optional[str] = None

    class Config:
        from_attributes = True
```

### File: /app/models/legal_organization.py
### Part: Model - Database operations for legal_organization CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.legal_organization import LegalOrganizationCreate, LegalOrganizationUpdate, LegalOrganizationOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_legal_organization(legal_organization: LegalOrganizationCreate) -> Optional[LegalOrganizationOut]:
    query_check = """
        SELECT id FROM legal_organization WHERE federal_tax_id_number = :federal_tax_id_number
    """
    existing = await database.fetch_one(query=query_check, values={"federal_tax_id_number": legal_organization.federal_tax_id_number})
    if existing:
        logger.warning(f"Legal organization with federal_tax_id_number '{legal_organization.federal_tax_id_number}' already exists")
        return None

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
                "name_en": legal_organization.name_en,
                "name_th": legal_organization.name_th
            })

            # 3. Insert into legal_organization
            query_legal = """
                INSERT INTO legal_organization (id, federal_tax_id_number)
                VALUES (:id, :federal_tax_id_number)
                RETURNING id, federal_tax_id_number
            """
            result = await database.fetch_one(query=query_legal, values={
                "id": party_id,
                "federal_tax_id_number": legal_organization.federal_tax_id_number
            })
            logger.info(f"Created legal organization: id={result['id']}")
            return LegalOrganizationOut(
                id=result['id'],
                name_en=legal_organization.name_en,
                name_th=legal_organization.name_th,
                federal_tax_id_number=result['federal_tax_id_number']
            )
        except Exception as e:
            logger.error(f"Error creating legal organization: {str(e)}")
            raise

async def get_legal_organization(legal_organization_id: int) -> Optional[LegalOrganizationOut]:
    query = """
        SELECT lo.id, o.name_en, o.name_th, lo.federal_tax_id_number
        FROM legal_organization lo
        JOIN organization o ON lo.id = o.id
        JOIN party p ON o.id = p.id
        WHERE lo.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": legal_organization_id})
    if not result:
        logger.warning(f"Legal organization not found: id={legal_organization_id}")
        return None
    logger.info(f"Retrieved legal organization: id={result['id']}")
    return LegalOrganizationOut(**result)

async def get_all_legal_organizations() -> List[LegalOrganizationOut]:
    query = """
        SELECT lo.id, o.name_en, o.name_th, lo.federal_tax_id_number
        FROM legal_organization lo
        JOIN organization o ON lo.id = o.id
        JOIN party p ON o.id = p.id
        ORDER BY lo.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} legal organizations")
    return [LegalOrganizationOut(**result) for result in results]

async def update_legal_organization(legal_organization_id: int, legal_organization: LegalOrganizationUpdate) -> Optional[LegalOrganizationOut]:
    if legal_organization.federal_tax_id_number:
        query_check = """
            SELECT id FROM legal_organization 
            WHERE federal_tax_id_number = :federal_tax_id_number AND id != :id
        """
        existing = await database.fetch_one(query=query_check, values={
            "federal_tax_id_number": legal_organization.federal_tax_id_number,
            "id": legal_organization_id
        })
        if existing:
            logger.warning(f"Legal organization with federal_tax_id_number '{legal_organization.federal_tax_id_number}' already exists")
            return None

    async with database.transaction():
        try:
            # Update organization
            if legal_organization.name_en or legal_organization.name_th:
                query_organization = """
                    UPDATE organization
                    SET name_en = COALESCE(:name_en, name_en),
                        name_th = COALESCE(:name_th, name_th)
                    WHERE id = :id
                    RETURNING name_en, name_th
                """
                org_result = await database.fetch_one(query=query_organization, values={
                    "name_en": legal_organization.name_en,
                    "name_th": legal_organization.name_th,
                    "id": legal_organization_id
                })

            # Update legal_organization
            query_legal = """
                UPDATE legal_organization
                SET federal_tax_id_number = COALESCE(:federal_tax_id_number, federal_tax_id_number)
                WHERE id = :id
                RETURNING id, federal_tax_id_number
            """
            result = await database.fetch_one(query=query_legal, values={
                "federal_tax_id_number": legal_organization.federal_tax_id_number,
                "id": legal_organization_id
            })
            if not result:
                logger.warning(f"Legal organization not found for update: id={legal_organization_id}")
                return None

            # Fetch updated organization data
            query_fetch = """
                SELECT o.name_en, o.name_th
                FROM organization o
                WHERE o.id = :id
            """
            org_data = await database.fetch_one(query=query_fetch, values={"id": legal_organization_id})
            logger.info(f"Updated legal organization: id={result['id']}")
            return LegalOrganizationOut(
                id=result['id'],
                name_en=org_data['name_en'],
                name_th=org_data['name_th'],
                federal_tax_id_number=result['federal_tax_id_number']
            )
        except Exception as e:
            logger.error(f"Error updating legal organization: {str(e)}")
            raise

async def delete_legal_organization(legal_organization_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from legal_organization
            query_legal = """
                DELETE FROM legal_organization WHERE id = :id
                RETURNING id
            """
            legal_result = await database.fetch_one(query=query_legal, values={"id": legal_organization_id})
            if not legal_result:
                logger.warning(f"Legal organization not found for deletion: id={legal_organization_id}")
                return False

            # Delete from organization
            query_organization = """
                DELETE FROM organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={"id": legal_organization_id})

            # Delete from party
            query_party = """
                DELETE FROM party WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_party, values={"id": legal_organization_id})

            logger.info(f"Deleted legal organization: id={legal_organization_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting legal organization: {str(e)}")
            raise
```

### File: /app/controllers/legal_organization.py
### Part: Controller - API endpoints for legal_organization CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.legal_organization import (
    create_legal_organization, get_legal_organization, get_all_legal_organizations,
    update_legal_organization, delete_legal_organization
)
from app.schemas.legal_organization import LegalOrganizationCreate, LegalOrganizationUpdate, LegalOrganizationOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/legal_organization", tags=["legal_organization"])

@router.post("/", response_model=LegalOrganizationOut)
async def create_legal_organization_endpoint(legal_organization: LegalOrganizationCreate, current_user: dict = Depends(get_current_user)):
    result = await create_legal_organization(legal_organization)
    if not result:
        logger.warning(f"Failed to create legal organization: federal_tax_id_number={legal_organization.federal_tax_id_number}")
        raise HTTPException(status_code=400, detail="Legal organization already exists")
    logger.info(f"Created legal organization: id={result.id}")
    return result

@router.get("/{legal_organization_id}", response_model=LegalOrganizationOut)
async def get_legal_organization_endpoint(legal_organization_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_legal_organization(legal_organization_id)
    if not result:
        logger.warning(f"Legal organization not found: id={legal_organization_id}")
        raise HTTPException(status_code=404, detail="Legal organization not found")
    logger.info(f"Retrieved legal organization: id={result.id}")
    return result

@router.get("/", response_model=List[LegalOrganizationOut])
async def get_all_legal_organizations_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_legal_organizations()
    logger.info(f"Retrieved {len(results)} legal organizations")
    return results

@router.put("/{legal_organization_id}", response_model=LegalOrganizationOut)
async def update_legal_organization_endpoint(legal_organization_id: int, legal_organization: LegalOrganizationUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_legal_organization(legal_organization_id, legal_organization)
    if not result:
        logger.warning(f"Failed to update legal organization: id={legal_organization_id}")
        raise HTTPException(status_code=404, detail="Legal organization not found or federal_tax_id_number already exists")
    logger.info(f"Updated legal organization: id={result.id}")
    return result

@router.delete("/{legal_organization_id}")
async def delete_legal_organization_endpoint(legal_organization_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_legal_organization(legal_organization_id)
    if not result:
        logger.warning(f"Legal organization not found for deletion: id={legal_organization_id}")
        raise HTTPException(status_code=404, detail="Legal organization not found")
    logger.info(f"Deleted legal organization: id={legal_organization_id}")
    return {"message": "Legal organization deleted"}
```

### File: /app/schemas/informal_organization.py
### Part: Schema - Pydantic models for informal_organization CRUD
```python
from pydantic import BaseModel, constr
from typing import Optional

class InformalOrganizationCreate(BaseModel):
    name_en: constr(max_length=128)
    name_th: constr(max_length=128)

class InformalOrganizationUpdate(BaseModel):
    name_en: Optional[constr(max_length=128)] = None
    name_th: Optional[constr(max_length=128)] = None

class InformalOrganizationOut(BaseModel):
    id: int
    name_en: str
    name_th: str

    class Config:
        from_attributes = True
```

### File: /app/models/informal_organization.py
### Part: Model - Database operations for informal_organization CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.informal_organization import InformalOrganizationCreate, InformalOrganizationUpdate, InformalOrganizationOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_informal_organization(informal_organization: InformalOrganizationCreate) -> Optional[InformalOrganizationOut]:
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
                "name_en": informal_organization.name_en,
                "name_th": informal_organization.name_th
            })

            # 3. Insert into informal_organization
            query_informal = """
                INSERT INTO informal_organization (id)
                VALUES (:id)
                RETURNING id
            """
            result = await database.fetch_one(query=query_informal, values={"id": party_id})
            logger.info(f"Created informal organization: id={result['id']}")
            return InformalOrganizationOut(
                id=result['id'],
                name_en=informal_organization.name_en,
                name_th=informal_organization.name_th
            )
        except Exception as e:
            logger.error(f"Error creating informal organization: {str(e)}")
            raise

async def get_informal_organization(informal_organization_id: int) -> Optional[InformalOrganizationOut]:
    query = """
        SELECT io.id, o.name_en, o.name_th
        FROM informal_organization io
        JOIN organization o ON io.id = o.id
        JOIN party p ON o.id = p.id
        WHERE io.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": informal_organization_id})
    if not result:
        logger.warning(f"Informal organization not found: id={informal_organization_id}")
        return None
    logger.info(f"Retrieved informal organization: id={result['id']}")
    return InformalOrganizationOut(**result)

async def get_all_informal_organizations() -> List[InformalOrganizationOut]:
    query = """
        SELECT io.id, o.name_en, o.name_th
        FROM informal_organization io
        JOIN organization o ON io.id = o.id
        JOIN party p ON o.id = p.id
        ORDER BY io.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} informal organizations")
    return [InformalOrganizationOut(**result) for result in results]

async def update_informal_organization(informal_organization_id: int, informal_organization: InformalOrganizationUpdate) -> Optional[InformalOrganizationOut]:
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
                "name_en": informal_organization.name_en,
                "name_th": informal_organization.name_th,
                "id": informal_organization_id
            })
            if not result:
                logger.warning(f"Informal organization not found for update: id={informal_organization_id}")
                return None
            logger.info(f"Updated informal organization: id={result['id']}")
            return InformalOrganizationOut(**result)
        except Exception as e:
            logger.error(f"Error updating informal organization: {str(e)}")
            raise

async def delete_informal_organization(informal_organization_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from informal_organization
            query_informal = """
                DELETE FROM informal_organization WHERE id = :id
                RETURNING id
            """
            informal_result = await database.fetch_one(query=query_informal, values={"id": informal_organization_id})
            if not informal_result:
                logger.warning(f"Informal organization not found for deletion: id={informal_organization_id}")
                return False

            # Delete from organization
            query_organization = """
                DELETE FROM organization WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_organization, values={"id": informal_organization_id})

            # Delete from party
            query_party = """
                DELETE FROM party WHERE id = :id
                RETURNING id
            """
            await database.fetch_one(query=query_party, values={"id": informal_organization_id})

            logger.info(f"Deleted informal organization: id={informal_organization_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting informal organization: {str(e)}")
            raise
```

### File: /app/controllers/informal_organization.py
### Part: Controller - API endpoints for informal_organization CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.informal_organization import (
    create_informal_organization, get_informal_organization, get_all_informal_organizations,
    update_informal_organization, delete_informal_organization
)
from app.schemas.informal_organization import InformalOrganizationCreate, InformalOrganizationUpdate, InformalOrganizationOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/informal_organization", tags=["informal_organization"])

@router.post("/", response_model=InformalOrganizationOut)
async def create_informal_organization_endpoint(informal_organization: InformalOrganizationCreate, current_user: dict = Depends(get_current_user)):
    result = await create_informal_organization(informal_organization)
    if not result:
        logger.warning(f"Failed to create informal organization")
        raise HTTPException(status_code=400, detail="Failed to create informal organization")
    logger.info(f"Created informal organization: id={result.id}")
    return result

@router.get("/{informal_organization_id}", response_model=InformalOrganizationOut)
async def get_informal_organization_endpoint(informal_organization_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_informal_organization(informal_organization_id)
    if not result:
        logger.warning(f"Informal organization not found: id={informal_organization_id}")
        raise HTTPException(status_code=404, detail="Informal organization not found")
    logger.info(f"Retrieved informal organization: id={result.id}")
    return result

@router.get("/", response_model=List[InformalOrganizationOut])
async def get_all_informal_organizations_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_informal_organizations()
    logger.info(f"Retrieved {len(results)} informal organizations")
    return results

@router.put("/{informal_organization_id}", response_model=InformalOrganizationOut)
async def update_informal_organization_endpoint(informal_organization_id: int, informal_organization: InformalOrganizationUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_informal_organization(informal_organization_id, informal_organization)
    if not result:
        logger.warning(f"Failed to update informal organization: id={informal_organization_id}")
        raise HTTPException(status_code=404, detail="Informal organization not found")
    logger.info(f"Updated informal organization: id={result.id}")
    return result

@router.delete("/{informal_organization_id}")
async def delete_informal_organization_endpoint(informal_organization_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_informal_organization(informal_organization_id)
    if not result:
        logger.warning(f"Informal organization not found for deletion: id={informal_organization_id}")
        raise HTTPException(status_code=404, detail="Informal organization not found")
    logger.info(f"Deleted informal organization: id={informal_organization_id}")
    return {"message": "Informal organization deleted"}
```