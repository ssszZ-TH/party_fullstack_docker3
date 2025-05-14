### File: /app/schemas/classify_by_minority.py
### Part: Schema - Pydantic models for classify_by_minority CRUD
```python
from pydantic import BaseModel
from typing import Optional
from datetime import date

class ClassifyByMinorityCreate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    minority_type_id: int

class ClassifyByMinorityUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: Optional[int] = None
    party_type_id: Optional[int] = None
    minority_type_id: Optional[int] = None

class ClassifyByMinorityOut(BaseModel):
    id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    minority_type_id: int
    name_en: str
    name_th: str

    class Config:
        from_attributes = True
```

### File: /app/models/classify_by_minority.py
### Part: Model - Database operations for classify_by_minority CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.classify_by_minority import ClassifyByMinorityCreate, ClassifyByMinorityUpdate, ClassifyByMinorityOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_classify_by_minority(classify_by_minority: ClassifyByMinorityCreate) -> Optional[ClassifyByMinorityOut]:
    async with database.transaction():
        try:
            # 1. Insert into party_classification
            query_party_cl = """
                INSERT INTO party_classification (fromdate, thrudate, party_id, party_type_id)
                VALUES (:fromdate, :thrudate, :party_id, :party_type_id)
                RETURNING id
            """
            party_cl_result = await database.fetch_one(query=query_party_cl, values={
                "fromdate": classify_by_minority.fromdate,
                "thrudate": classify_by_minority.thrudate,
                "party_id": classify_by_minority.party_id,
                "party_type_id": classify_by_minority.party_type_id
            })
            new_id = party_cl_result["id"]

            # 2. Insert into organization_classification
            query_org_cl = """
                INSERT INTO organization_classification (id)
                VALUES (:id)
            """
            await database.execute(query=query_org_cl, values={"id": new_id})

            # 3. Insert into classify_by_minority
            query_minority = """
                INSERT INTO classify_by_minority (id, minority_type_id)
                VALUES (:id, :minority_type_id)
                RETURNING id
            """
            await database.execute(query=query_minority, values={
                "id": new_id,
                "minority_type_id": classify_by_minority.minority_type_id
            })

            # Fetch the complete data
            query_fetch = """
                SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
                       cm.minority_type_id, mt.name_en, mt.name_th
                FROM classify_by_minority cm
                JOIN organization_classification oc ON cm.id = oc.id
                JOIN party_classification pc ON cm.id = pc.id
                JOIN minority_type mt ON cm.minority_type_id = mt.id
                WHERE cm.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": new_id})
            logger.info(f"Created classify_by_minority: id={new_id}")
            return ClassifyByMinorityOut(**result)
        except Exception as e:
            logger.error(f"Error creating classify_by_minority: {str(e)}")
            raise

async def get_classify_by_minority(classify_by_minority_id: int) -> Optional[ClassifyByMinorityOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               cm.minority_type_id, mt.name_en, mt.name_th
        FROM classify_by_minority cm
        JOIN organization_classification oc ON cm.id = oc.id
        JOIN party_classification pc ON cm.id = pc.id
        JOIN minority_type mt ON cm.minority_type_id = mt.id
        WHERE cm.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": classify_by_minority_id})
    if not result:
        logger.warning(f"Classify_by_minority not found: id={classify_by_minority_id}")
        return None
    logger.info(f"Retrieved classify_by_minority: id={result['id']}")
    return ClassifyByMinorityOut(**result)

async def get_all_classify_by_minorities() -> List[ClassifyByMinorityOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               cm.minority_type_id, mt.name_en, mt.name_th
        FROM classify_by_minority cm
        JOIN organization_classification oc ON cm.id = oc.id
        JOIN party_classification pc ON cm.id = pc.id
        JOIN minority_type mt ON cm.minority_type_id = mt.id
        ORDER BY pc.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} classify_by_minorities")
    return [ClassifyByMinorityOut(**result) for result in results]

async def update_classify_by_minority(classify_by_minority_id: int, classify_by_minority: ClassifyByMinorityUpdate) -> Optional[ClassifyByMinorityOut]:
    async with database.transaction():
        try:
            # Update party_classification
            query_party_cl = """
                UPDATE party_classification
                SET fromdate = COALESCE(:fromdate, fromdate),
                    thrudate = COALESCE(:thrudate, thrudate),
                    party_id = COALESCE(:party_id, party_id),
                    party_type_id = COALESCE(:party_type_id, party_type_id)
                WHERE id = :id
            """
            await database.execute(query=query_party_cl, values={
                "fromdate": classify_by_minority.fromdate,
                "thrudate": classify_by_minority.thrudate,
                "party_id": classify_by_minority.party_id,
                "party_type_id": classify_by_minority.party_type_id,
                "id": classify_by_minority_id
            })

            # Update classify_by_minority
            query_minority = """
                UPDATE classify_by_minority
                SET minority_type_id = COALESCE(:minority_type_id, minority_type_id)
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query_minority, values={
                "minority_type_id": classify_by_minority.minority_type_id,
                "id": classify_by_minority_id
            })
            if not result:
                logger.warning(f"Classify_by_minority not found for update: id={classify_by_minority_id}")
                return None

            # Fetch updated data
            query_fetch = """
                SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
                       cm.minority_type_id, mt.name_en, mt.name_th
                FROM classify_by_minority cm
                JOIN organization_classification oc ON cm.id = oc.id
                JOIN party_classification pc ON cm.id = pc.id
                JOIN minority_type mt ON cm.minority_type_id = mt.id
                WHERE cm.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": classify_by_minority_id})
            logger.info(f"Updated classify_by_minority: id={classify_by_minority_id}")
            return ClassifyByMinorityOut(**result)
        except Exception as e:
            logger.error(f"Error updating classify_by_minority: {str(e)}")
            raise

async def delete_classify_by_minority(classify_by_minority_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from classify_by_minority
            query_minority = """
                DELETE FROM classify_by_minority WHERE id = :id
                RETURNING id
            """
            minority_result = await database.fetch_one(query=query_minority, values={"id": classify_by_minority_id})
            if not minority_result:
                logger.warning(f"Classify_by_minority not found for deletion: id={classify_by_minority_id}")
                return False

            # Delete from organization_classification
            query_org_cl = """
                DELETE FROM organization_classification WHERE id = :id
            """
            await database.execute(query=query_org_cl, values={"id": classify_by_minority_id})

            # Delete from party_classification
            query_party_cl = """
                DELETE FROM party_classification WHERE id = :id
            """
            await database.execute(query=query_party_cl, values={"id": classify_by_minority_id})

            logger.info(f"Deleted classify_by_minority: id={classify_by_minority_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting classify_by_minority: {str(e)}")
            raise
```

### File: /app/controllers/classify_by_minority.py
### Part: Controller - API endpoints for classify_by_minority CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.classify_by_minority import (
    create_classify_by_minority, get_classify_by_minority, get_all_classify_by_minorities,
    update_classify_by_minority, delete_classify_by_minority
)
from app.schemas.classify_by_minority import ClassifyByMinorityCreate, ClassifyByMinorityUpdate, ClassifyByMinorityOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/classify_by_minority", tags=["classify_by_minority"])

@router.post("/", response_model=ClassifyByMinorityOut)
async def create_classify_by_minority_endpoint(classify_by_minority: ClassifyByMinorityCreate, current_user: dict = Depends(get_current_user)):
    result = await create_classify_by_minority(classify_by_minority)
    if not result:
        logger.warning(f"Failed to create classify_by_minority")
        raise HTTPException(status_code=400, detail="Failed to create classify_by_minority")
    logger.info(f"Created classify_by_minority: id={result.id}")
    return result

@router.get("/{classify_by_minority_id}", response_model=ClassifyByMinorityOut)
async def get_classify_by_minority_endpoint(classify_by_minority_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_classify_by_minority(classify_by_minority_id)
    if not result:
        logger.warning(f"Classify_by_minority not found: id={classify_by_minority_id}")
        raise HTTPException(status_code=404, detail="Classify_by_minority not found")
    logger.info(f"Retrieved classify_by_minority: id={result.id}")
    return result

@router.get("/", response_model=List[ClassifyByMinorityOut])
async def get_all_classify_by_minorities_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_classify_by_minorities()
    logger.info(f"Retrieved {len(results)} classify_by_minorities")
    return results

@router.put("/{classify_by_minority_id}", response_model=ClassifyByMinorityOut)
async def update_classify_by_minority_endpoint(classify_by_minority_id: int, classify_by_minority: ClassifyByMinorityUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_classify_by_minority(classify_by_minority_id, classify_by_minority)
    if not result:
        logger.warning(f"Classify_by_minority not found for update: id={classify_by_minority_id}")
        raise HTTPException(status_code=404, detail="Classify_by_minority not found")
    logger.info(f"Updated classify_by_minority: id={result.id}")
    return result

@router.delete("/{classify_by_minority_id}")
async def delete_classify_by_minority_endpoint(classify_by_minority_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_classify_by_minority(classify_by_minority_id)
    if not result:
        logger.warning(f"Classify_by_minority not found for deletion: id={classify_by_minority_id}")
        raise HTTPException(status_code=404, detail="Classify_by_minority not found")
    logger.info(f"Deleted classify_by_minority: id={classify_by_minority_id}")
    return {"message": "Classify_by_minority deleted"}
```

### File: /app/schemas/classify_by_industry.py
### Part: Schema - Pydantic models for classify_by_industry CRUD
```python
from pydantic import BaseModel
from typing import Optional
from datetime import date

class ClassifyByIndustryCreate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    industry_type_id: int

class ClassifyByIndustryUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: Optional[int] = None
    party_type_id: Optional[int] = None
    industry_type_id: Optional[int] = None

class ClassifyByIndustryOut(BaseModel):
    id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    industry_type_id: int
    naics_code: str
    description: str

    class Config:
        from_attributes = True
```

### File: /app/models/classify_by_industry.py
### Part: Model - Database operations for classify_by_industry CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.classify_by_industry import ClassifyByIndustryCreate, ClassifyByIndustryUpdate, ClassifyByIndustryOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_classify_by_industry(classify_by_industry: ClassifyByIndustryCreate) -> Optional[ClassifyByIndustryOut]:
    async with database.transaction():
        try:
            # 1. Insert into party_classification
            query_party_cl = """
                INSERT INTO party_classification (fromdate, thrudate, party_id, party_type_id)
                VALUES (:fromdate, :thrudate, :party_id, :party_type_id)
                RETURNING id
            """
            party_cl_result = await database.fetch_one(query=query_party_cl, values={
                "fromdate": classify_by_industry.fromdate,
                "thrudate": classify_by_industry.thrudate,
                "party_id": classify_by_industry.party_id,
                "party_type_id": classify_by_industry.party_type_id
            })
            new_id = party_cl_result["id"]

            # 2. Insert into organization_classification
            query_org_cl = """
                INSERT INTO organization_classification (id)
                VALUES (:id)
            """
            await database.execute(query=query_org_cl, values={"id": new_id})

            # 3. Insert into classify_by_industry
            query_industry = """
                INSERT INTO classify_by_industry (id, industry_type_id)
                VALUES (:id, :industry_type_id)
                RETURNING id
            """
            await database.execute(query=query_industry, values={
                "id": new_id,
                "industry_type_id": classify_by_industry.industry_type_id
            })

            # Fetch the complete data
            query_fetch = """
                SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
                       ci.industry_type_id, it.naics_code, it.description
                FROM classify_by_industry ci
                JOIN organization_classification oc ON ci.id = oc.id
                JOIN party_classification pc ON ci.id = pc.id
                JOIN industry_type it ON ci.industry_type_id = it.id
                WHERE ci.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": new_id})
            logger.info(f"Created classify_by_industry: id={new_id}")
            return ClassifyByIndustryOut(**result)
        except Exception as e:
            logger.error(f"Error creating classify_by_industry: {str(e)}")
            raise

async def get_classify_by_industry(classify_by_industry_id: int) -> Optional[ClassifyByIndustryOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               ci.industry_type_id, it.naics_code, it.description
        FROM classify_by_industry ci
        JOIN organization_classification oc ON ci.id = oc.id
        JOIN party_classification pc ON ci.id = pc.id
        JOIN industry_type it ON ci.industry_type_id = it.id
        WHERE ci.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": classify_by_industry_id})
    if not result:
        logger.warning(f"Classify_by_industry not found: id={classify_by_industry_id}")
        return None
    logger.info(f"Retrieved classify_by_industry: id={result['id']}")
    return ClassifyByIndustryOut(**result)

async def get_all_classify_by_industries() -> List[ClassifyByIndustryOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               ci.industry_type_id, it.naics_code, it.description
        FROM classify_by_industry ci
        JOIN organization_classification oc ON ci.id = oc.id
        JOIN party_classification pc ON ci.id = pc.id
        JOIN industry_type it ON ci.industry_type_id = it.id
        ORDER BY pc.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} classify_by_industries")
    return [ClassifyByIndustryOut(**result) for result in results]

async def update_classify_by_industry(classify_by_industry_id: int, classify_by_industry: ClassifyByIndustryUpdate) -> Optional[ClassifyByIndustryOut]:
    async with database.transaction():
        try:
            # Update party_classification
            query_party_cl = """
                UPDATE party_classification
                SET fromdate = COALESCE(:fromdate, fromdate),
                    thrudate = COALESCE(:thrudate, thrudate),
                    party_id = COALESCE(:party_id, party_id),
                    party_type_id = COALESCE(:party_type_id, party_type_id)
                WHERE id = :id
            """
            await database.execute(query=query_party_cl, values={
                "fromdate": classify_by_industry.fromdate,
                "thrudate": classify_by_industry.thrudate,
                "party_id": classify_by_industry.party_id,
                "party_type_id": classify_by_industry.party_type_id,
                "id": classify_by_industry_id
            })

            # Update classify_by_industry
            query_industry = """
                UPDATE classify_by_industry
                SET industry_type_id = COALESCE(:industry_type_id, industry_type_id)
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query_industry, values={
                "industry_type_id": classify_by_industry.industry_type_id,
                "id": classify_by_industry_id
            })
            if not result:
                logger.warning(f"Classify_by_industry not found for update: id={classify_by_industry_id}")
                return None

            # Fetch updated data
            query_fetch = """
                SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
                       ci.industry_type_id, it.naics_code, it.description
                FROM classify_by_industry ci
                JOIN organization_classification oc ON ci.id = oc.id
                JOIN party_classification pc ON ci.id = pc.id
                JOIN industry_type it ON ci.industry_type_id = it.id
                WHERE ci.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": classify_by_industry_id})
            logger.info(f"Updated classify_by_industry: id={classify_by_industry_id}")
            return ClassifyByIndustryOut(**result)
        except Exception as e:
            logger.error(f"Error updating classify_by_industry: {str(e)}")
            raise

async def delete_classify_by_industry(classify_by_industry_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from classify_by_industry
            query_industry = """
                DELETE FROM classify_by_industry WHERE id = :id
                RETURNING id
            """
            industry_result = await database.fetch_one(query=query_industry, values={"id": classify_by_industry_id})
            if not industry_result:
                logger.warning(f"Classify_by_industry not found for deletion: id={classify_by_industry_id}")
                return False

            # Delete from organization_classification
            query_org_cl = """
                DELETE FROM organization_classification WHERE id = :id
            """
            await database.execute(query=query_org_cl, values={"id": classify_by_industry_id})

            # Delete from party_classification
            query_party_cl = """
                DELETE FROM party_classification WHERE id = :id
            """
            await database.execute(query=query_party_cl, values={"id": classify_by_industry_id})

            logger.info(f"Deleted classify_by_industry: id={classify_by_industry_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting classify_by_industry: {str(e)}")
            raise
```

### File: /app/controllers/classify_by_industry.py
### Part: Controller - API endpoints for classify_by_industry CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.classify_by_industry import (
    create_classify_by_industry, get_classify_by_industry, get_all_classify_by_industries,
    update_classify_by_industry, delete_classify_by_industry
)
from app.schemas.classify_by_industry import ClassifyByIndustryCreate, ClassifyByIndustryUpdate, ClassifyByIndustryOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/classify_by_industry", tags=["classify_by_industry"])

@router.post("/", response_model=ClassifyByIndustryOut)
async def create_classify_by_industry_endpoint(classify_by_industry: ClassifyByIndustryCreate, current_user: dict = Depends(get_current_user)):
    result = await create_classify_by_industry(classify_by_industry)
    if not result:
        logger.warning(f"Failed to create classify_by_industry")
        raise HTTPException(status_code=400, detail="Failed to create classify_by_industry")
    logger.info(f"Created classify_by_industry: id={result.id}")
    return result

@router.get("/{classify_by_industry_id}", response_model=ClassifyByIndustryOut)
async def get_classify_by_industry_endpoint(classify_by_industry_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_classify_by_industry(classify_by_industry_id)
    if not result:
        logger.warning(f"Classify_by_industry not found: id={classify_by_industry_id}")
        raise HTTPException(status_code=404, detail="Classify_by_industry not found")
    logger.info(f"Retrieved classify_by_industry: id={result.id}")
    return result

@router.get("/", response_model=List[ClassifyByIndustryOut])
async def get_all_classify_by_industries_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_classify_by_industries()
    logger.info(f"Retrieved {len(results)} classify_by_industries")
    return results

@router.put("/{classify_by_industry_id}", response_model=ClassifyByIndustryOut)
async def update_classify_by_industry_endpoint(classify_by_industry_id: int, classify_by_industry: ClassifyByIndustryUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_classify_by_industry(classify_by_industry_id, classify_by_industry)
    if not result:
        logger.warning(f"Classify_by_industry not found for update: id={classify_by_industry_id}")
        raise HTTPException(status_code=404, detail="Classify_by_industry not found")
    logger.info(f"Updated classify_by_industry: id={result.id}")
    return result

@router.delete("/{classify_by_industry_id}")
async def delete_classify_by_industry_endpoint(classify_by_industry_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_classify_by_industry(classify_by_industry_id)
    if not result:
        logger.warning(f"Classify_by_industry not found for deletion: id={classify_by_industry_id}")
        raise HTTPException(status_code=404, detail="Classify_by_industry not found")
    logger.info(f"Deleted classify_by_industry: id={classify_by_industry_id}")
    return {"message": "Classify_by_industry deleted"}
```

### File: /app/schemas/classify_by_size.py
### Part: Schema - Pydantic models for classify_by_size CRUD
```python
from pydantic import BaseModel
from typing import Optional
from datetime import date

class ClassifyBySizeCreate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    employee_count_range_id: int

class ClassifyBySizeUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: Optional[int] = None
    party_type_id: Optional[int] = None
    employee_count_range_id: Optional[int] = None

class ClassifyBySizeOut(BaseModel):
    id: int
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    party_id: int
    party_type_id: int
    employee_count_range_id: int
    description: str

    class Config:
        from_attributes = True
```

### File: /app/models/classify_by_size.py
### Part: Model - Database operations for classify_by_size CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.classify_by_size import ClassifyBySizeCreate, ClassifyBySizeUpdate, ClassifyBySizeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_classify_by_size(classify_by_size: ClassifyBySizeCreate) -> Optional[ClassifyBySizeOut]:
    async with database.transaction():
        try:
            # 1. Insert into party_classification
            query_party_cl = """
                INSERT INTO party_classification (fromdate, thrudate, party_id, party_type_id)
                VALUES (:fromdate, :thrudate, :party_id, :party_type_id)
                RETURNING id
            """
            party_cl_result = await database.fetch_one(query=query_party_cl, values={
                "fromdate": classify_by_size.fromdate,
                "thrudate": classify_by_size.thrudate,
                "party_id": classify_by_size.party_id,
                "party_type_id": classify_by_size.party_type_id
            })
            new_id = party_cl_result["id"]

            # 2. Insert into organization_classification
            query_org_cl = """
                INSERT INTO organization_classification (id)
                VALUES (:id)
            """
            await database.execute(query=query_org_cl, values={"id": new_id})

            # 3. Insert into classify_by_size
            query_size = """
                INSERT INTO classify_by_size (id, employee_count_range_id)
                VALUES (:id, :employee_count_range_id)
                RETURNING id
            """
            await database.execute(query=query_size, values={
                "id": new_id,
                "employee_count_range_id": classify_by_size.employee_count_range_id
            })

            # Fetch the complete data
            query_fetch = """
                SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
                       cs.employee_count_range_id, ecr.description
                FROM classify_by_size cs
                JOIN organization_classification oc ON cs.id = oc.id
                JOIN party_classification pc ON cs.id = pc.id
                JOIN employee_count_range ecr ON cs.employee_count_range_id = ecr.id
                WHERE cs.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": new_id})
            logger.info(f"Created classify_by_size: id={new_id}")
            return ClassifyBySizeOut(**result)
        except Exception as e:
            logger.error(f"Error creating classify_by_size: {str(e)}")
            raise

async def get_classify_by_size(classify_by_size_id: int) -> Optional[ClassifyBySizeOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               cs.employee_count_range_id, ecr.description
        FROM classify_by_size cs
        JOIN organization_classification oc ON cs.id = oc.id
        JOIN party_classification pc ON cs.id = pc.id
        JOIN employee_count_range ecr ON cs.employee_count_range_id = ecr.id
        WHERE cs.id = :id
    """
    result = await database.fetch_one(query=query, values={"id": classify_by_size_id})
    if not result:
        logger.warning(f"Classify_by_size not found: id={classify_by_size_id}")
        return None
    logger.info(f"Retrieved classify_by_size: id={result['id']}")
    return ClassifyBySizeOut(**result)

async def get_all_classify_by_sizes() -> List[ClassifyBySizeOut]:
    query = """
        SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
               cs.employee_count_range_id, ecr.description
        FROM classify_by_size cs
        JOIN organization_classification oc ON cs.id = oc.id
        JOIN party_classification pc ON cs.id = pc.id
        JOIN employee_count_range ecr ON cs.employee_count_range_id = ecr.id
        ORDER BY pc.id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} classify_by_sizes")
    return [ClassifyBySizeOut(**result) for result in results]

async def update_classify_by_size(classify_by_size_id: int, classify_by_size: ClassifyBySizeUpdate) -> Optional[ClassifyBySizeOut]:
    async with database.transaction():
        try:
            # Update party_classification
            query_party_cl = """
                UPDATE party_classification
                SET fromdate = COALESCE(:fromdate, fromdate),
                    thrudate = COALESCE(:thrudate, thrudate),
                    party_id = COALESCE(:party_id, party_id),
                    party_type_id = COALESCE(:party_type_id, party_type_id)
                WHERE id = :id
            """
            await database.execute(query=query_party_cl, values={
                "fromdate": classify_by_size.fromdate,
                "thrudate": classify_by_size.thrudate,
                "party_id": classify_by_size.party_id,
                "party_type_id": classify_by_size.party_type_id,
                "id": classify_by_size_id
            })

            # Update classify_by_size
            query_size = """
                UPDATE classify_by_size
                SET employee_count_range_id = COALESCE(:employee_count_range_id, employee_count_range_id)
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query_size, values={
                "employee_count_range_id": classify_by_size.employee_count_range_id,
                "id": classify_by_size_id
            })
            if not result:
                logger.warning(f"Classify_by_size not found for update: id={classify_by_size_id}")
                return None

            # Fetch updated data
            query_fetch = """
                SELECT pc.id, pc.fromdate, pc.thrudate, pc.party_id, pc.party_type_id, 
                       cs.employee_count_range_id, ecr.description
                FROM classify_by_size cs
                JOIN organization_classification oc ON cs.id = oc.id
                JOIN party_classification pc ON cs.id = pc.id
                JOIN employee_count_range ecr ON cs.employee_count_range_id = ecr.id
                WHERE cs.id = :id
            """
            result = await database.fetch_one(query=query_fetch, values={"id": classify_by_size_id})
            logger.info(f"Updated classify_by_size: id={classify_by_size_id}")
            return ClassifyBySizeOut(**result)
        except Exception as e:
            logger.error(f"Error updating classify_by_size: {str(e)}")
            raise

async def delete_classify_by_size(classify_by_size_id: int) -> bool:
    async with database.transaction():
        try:
            # Delete from classify_by_size
            query_size = """
                DELETE FROM classify_by_size WHERE id = :id
                RETURNING id
            """
            size_result = await database.fetch_one(query=query_size, values={"id": classify_by_size_id})
            if not size_result:
                logger.warning(f"Classify_by_size not found for deletion: id={classify_by_size_id}")
                return False

            # Delete from organization_classification
            query_org_cl = """
                DELETE FROM organization_classification WHERE id = :id
            """
            await database.execute(query=query_org_cl, values={"id": classify_by_size_id})

            # Delete from party_classification
            query_party_cl = """
                DELETE FROM party_classification WHERE id = :id
            """
            await database.execute(query=query_party_cl, values={"id": classify_by_size_id})

            logger.info(f"Deleted classify_by_size: id={classify_by_size_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting classify_by_size: {str(e)}")
            raise
```

### File: /app/controllers/classify_by_size.py
### Part: Controller - API endpoints for classify_by_size CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.classify_by_size import (
    create_classify_by_size, get_classify_by_size, get_all_classify_by_sizes,
    update_classify_by_size, delete_classify_by_size
)
from app.schemas.classify_by_size import ClassifyBySizeCreate, ClassifyBySizeUpdate, ClassifyBySizeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/classify_by_size", tags=["classify_by_size"])

@router.post("/", response_model=ClassifyBySizeOut)
async def create_classify_by_size_endpoint(classify_by_size: ClassifyBySizeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_classify_by_size(classify_by_size)
    if not result:
        logger.warning(f"Failed to create classify_by_size")
        raise HTTPException(status_code=400, detail="Failed to create classify_by_size")
    logger.info(f"Created classify_by_size: id={result.id}")
    return result

@router.get("/{classify_by_size_id}", response_model=ClassifyBySizeOut)
async def get_classify_by_size_endpoint(classify_by_size_id: int, current_user: dict | None = Depends(get_current_user)):
    result = await get_classify_by_size(classify_by_size_id)
    if not result:
        logger.warning(f"Classify_by_size not found: id={classify_by_size_id}")
        raise HTTPException(status_code=404, detail="Classify_by_size not found")
    logger.info(f"Retrieved classify_by_size: id={result.id}")
    return result

@router.get("/", response_model=List[ClassifyBySizeOut])
async def get_all_classify_by_sizes_endpoint(current_user: dict | None = Depends(get_current_user)):
    results = await get_all_classify_by_sizes()
    logger.info(f"Retrieved {len(results)} classify_by_sizes")
    return results

@router.put("/{classify_by_size_id}", response_model=ClassifyBySizeOut)
async def update_classify_by_size_endpoint(classify_by_size_id: int, classify_by_size: ClassifyBySizeUpdate, current_user: dict | None = Depends(get_current_user)):
    result = await update_classify_by_size(classify_by_size_id, classify_by_size)
    if not result:
        logger.warning(f"Classify_by_size not found for update: id={classify_by_size_id}")
        raise HTTPException(status_code=404, detail="Classify_by_size not found")
    logger.info(f"Updated classify_by_size: id={result.id}")
    return result

@router.delete("/{classify_by_size_id}")
async def delete_classify_by_size_endpoint(classify_by_size_id: int, current_user: dict | None = Depends(get_current_user)):
    result = await delete_classify_by_size(classify_by_size_id)
    if not result:
        logger.warning(f"Classify_by_size not found for deletion: id={classify_by_size_id}")
        raise HTTPException(status_code=404, detail="Classify_by_size not found")
    logger.info(f"Deleted classify_by_size: id={classify_by_size_id}")
    return {"message": "Classify_by_size deleted"}
```