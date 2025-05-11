### File: /app/schemas/industry_type.py
### Part: Schema - Pydantic models for industry_type CRUD
```python
from pydantic import BaseModel, constr
from typing import Optional

class IndustryTypeCreate(BaseModel):
    naics_code: constr(max_length=64)
    description: Optional[constr(max_length=128)] = None

class IndustryTypeUpdate(BaseModel):
    naics_code: Optional[constr(max_length=64)] = None
    description: Optional[constr(max_length=128)] = None

class IndustryTypeOut(BaseModel):
    id: int
    naics_code: str
    description: Optional[str] = None

    class Config:
        from_attributes = True
```

### File: /app/models/industry_type.py
### Part: Model - Database operations for industry_type CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.industry_type import IndustryTypeCreate, IndustryTypeUpdate, IndustryTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_industry_type(industry_type: IndustryTypeCreate) -> Optional[IndustryTypeOut]:
    query = """
        SELECT id, naics_code, description FROM industry_type WHERE naics_code = :naics_code
    """
    existing = await database.fetch_one(query=query, values={"naics_code": industry_type.naics_code})
    if existing:
        logger.warning(f"Industry type with naics_code '{industry_type.naics_code}' already exists")
        return None

    query = """
        INSERT INTO industry_type (naics_code, description)
        VALUES (:naics_code, :description)
        RETURNING id, naics_code, description
    """
    try:
        result = await database.fetch_one(query=query, values={"naics_code": industry_type.naics_code, "description": industry_type.description})
        logger.info(f"Created industry type: id={result['id']}, naics_code={result['naics_code']}")
        return IndustryTypeOut(**result)
    except Exception as e:
        logger.error(f"Error creating industry type: {str(e)}")
        raise

async def get_industry_type(industry_type_id: int) -> Optional[IndustryTypeOut]:
    query = """
        SELECT id, naics_code, description FROM industry_type WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": industry_type_id})
    if not result:
        logger.warning(f"Industry type not found: id={industry_type_id}")
        return None
    logger.info(f"Retrieved industry type: id={result['id']}, naics_code={result['naics_code']}")
    return IndustryTypeOut(**result)

async def get_all_industry_types() -> List[IndustryTypeOut]:
    query = """
        SELECT id, naics_code, description FROM industry_type
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} industry types")
    return [IndustryTypeOut(**result) for result in results]

async def update_industry_type(industry_type_id: int, industry_type: IndustryTypeUpdate) -> Optional[IndustryTypeOut]:
    if industry_type.naics_code:
        query = """
            SELECT id, naics_code, description FROM industry_type WHERE naics_code = :naics_code AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"naics_code": industry_type.naics_code, "id": industry_type_id})
        if existing:
            logger.warning(f"Industry type with naics_code '{industry_type.naics_code}' already exists")
            return None

    query = """
        UPDATE industry_type
        SET naics_code = COALESCE(:naics_code, naics_code),
            description = COALESCE(:description, description)
        WHERE id = :id
        RETURNING id, naics_code, description
    """
    try:
        result = await database.fetch_one(query=query, values={"naics_code": industry_type.naics_code, "description": industry_type.description, "id": industry_type_id})
        if not result:
            logger.warning(f"Industry type not found for update: id={industry_type_id}")
            return None
        logger.info(f"Updated industry type: id={result['id']}, naics_code={result['naics_code']}")
        return IndustryTypeOut(**result)
    except Exception as e:
        logger.error(f"Error updating industry type: {str(e)}")
        raise

async def delete_industry_type(industry_type_id: int) -> bool:
    query = """
        DELETE FROM industry_type WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": industry_type_id})
    if not result:
        logger.warning(f"Industry type not found for deletion: id={industry_type_id}")
        return False
    logger.info(f"Deleted industry type: id={industry_type_id}")
    return True
```

### File: /app/controllers/industry_type.py
### Part: Controller - API endpoints for industry_type CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.industry_type import (
    create_industry_type, get_industry_type, get_all_industry_types,
    update_industry_type, delete_industry_type
)
from app.schemas.industry_type import IndustryTypeCreate, IndustryTypeUpdate, IndustryTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/industry_type", tags=["industry_type"])

@router.post("/", response_model=IndustryTypeOut)
async def create_industry_type_endpoint(industry_type: IndustryTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_industry_type(industry_type)
    if not result:
        logger.warning(f"Failed to create industry type: naics_code={industry_type.naics_code}")
        raise HTTPException(status_code=400, detail="NAICS code already exists")
    logger.info(f"Created industry type: id={result.id}, naics_code={result.naics_code}")
    return result

@router.get("/{industry_type_id}", response_model=IndustryTypeOut)
async def get_industry_type_endpoint(industry_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_industry_type(industry_type_id)
    if not result:
        logger.warning(f"Industry type not found: id={industry_type_id}")
        raise HTTPException(status_code=404, detail="Industry type not found")
    logger.info(f"Retrieved industry type: id={result.id}, naics_code={result.naics_code}")
    return result

@router.get("/", response_model=List[IndustryTypeOut])
async def get_all_industry_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_industry_types()
    logger.info(f"Retrieved {len(results)} industry types")
    return results

@router.put("/{industry_type_id}", response_model=IndustryTypeOut)
async def update_industry_type_endpoint(industry_type_id: int, industry_type: IndustryTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_industry_type(industry_type_id, industry_type)
    if not result:
        logger.warning(f"Failed to update industry type: id={industry_type_id}")
        raise HTTPException(status_code=404, detail="Industry type not found or NAICS code already exists")
    logger.info(f"Updated industry type: id={result.id}, naics_code={result.naics_code}")
    return result

@router.delete("/{industry_type_id}")
async def delete_industry_type_endpoint(industry_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_industry_type(industry_type_id)
    if not result:
        logger.warning(f"Industry type not found for deletion: id={industry_type_id}")
        raise HTTPException(status_code=404, detail="Industry type not found")
    logger.info(f"Deleted industry type: id={industry_type_id}")
    return {"message": "Industry type deleted"}
```

### File: /app/schemas/employee_count_range.py
### Part: Schema - Pydantic models for employee_count_range CRUD
```python
from pydantic import BaseModel, constr
from typing import Optional

class EmployeeCountRangeCreate(BaseModel):
    description: constr(max_length=128)

class EmployeeCountRangeUpdate(BaseModel):
    description: Optional[constr(max_length=128)] = None

class EmployeeCountRangeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True
```

### File: /app/models/employee_count_range.py
### Part: Model - Database operations for employee_count_range CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.employee_count_range import EmployeeCountRangeCreate, EmployeeCountRangeUpdate, EmployeeCountRangeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_employee_count_range(employee_count_range: EmployeeCountRangeCreate) -> Optional[EmployeeCountRangeOut]:
    query = """
        SELECT id, description FROM employee_count_range WHERE description = :description
    """
    existing = await database.fetch_one(query=query, values={"description": employee_count_range.description})
    if existing:
        logger.warning(f"Employee count range with description '{employee_count_range.description}' already exists")
        return None

    query = """
        INSERT INTO employee_count_range (description)
        VALUES (:description)
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": employee_count_range.description})
        logger.info(f"Created employee count range: id={result['id']}, description={result['description']}")
        return EmployeeCountRangeOut(**result)
    except Exception as e:
        logger.error(f"Error creating employee count range: {str(e)}")
        raise

async def get_employee_count_range(employee_count_range_id: int) -> Optional[EmployeeCountRangeOut]:
    query = """
        SELECT id, description FROM employee_count_range WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": employee_count_range_id})
    if not result:
        logger.warning(f"Employee count range not found: id={employee_count_range_id}")
        return None
    logger.info(f"Retrieved employee count range: id={result['id']}, description={result['description']}")
    return EmployeeCountRangeOut(**result)

async def get_all_employee_count_ranges() -> List[EmployeeCountRangeOut]:
    query = """
        SELECT id, description FROM employee_count_range
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} employee count ranges")
    return [EmployeeCountRangeOut(**result) for result in results]

async def update_employee_count_range(employee_count_range_id: int, employee_count_range: EmployeeCountRangeUpdate) -> Optional[EmployeeCountRangeOut]:
    if employee_count_range.description:
        query = """
            SELECT id, description FROM employee_count_range WHERE description = :description AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"description": employee_count_range.description, "id": employee_count_range_id})
        if existing:
            logger.warning(f"Employee count range with description '{employee_count_range.description}' already exists")
            return None

    query = """
        UPDATE employee_count_range
        SET description = COALESCE(:description, description)
        WHERE id = :id
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": employee_count_range.description, "id": employee_count_range_id})
        if not result:
            logger.warning(f"Employee count range not found for update: id={employee_count_range_id}")
            return None
        logger.info(f"Updated employee count range: id={result['id']}, description={result['description']}")
        return EmployeeCountRangeOut(**result)
    except Exception as e:
        logger.error(f"Error updating employee count range: {str(e)}")
        raise

async def delete_employee_count_range(employee_count_range_id: int) -> bool:
    query = """
        DELETE FROM employee_count_range WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": employee_count_range_id})
    if not result:
        logger.warning(f"Employee count range not found for deletion: id={employee_count_range_id}")
        return False
    logger.info(f"Deleted employee count range: id={employee_count_range_id}")
    return True
```

### File: /app/controllers/employee_count_range.py
### Part: Controller - API endpoints for employee_count_range CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.employee_count_range import (
    create_employee_count_range, get_employee_count_range, get_all_employee_count_ranges,
    update_employee_count_range, delete_employee_count_range
)
from app.schemas.employee_count_range import EmployeeCountRangeCreate, EmployeeCountRangeUpdate, EmployeeCountRangeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/employee_count_range", tags=["employee_count_range"])

@router.post("/", response_model=EmployeeCountRangeOut)
async def create_employee_count_range_endpoint(employee_count_range: EmployeeCountRangeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_employee_count_range(employee_count_range)
    if not result:
        logger.warning(f"Failed to create employee count range: description={employee_count_range.description}")
        raise HTTPException(status_code=400, detail="Description already exists")
    logger.info(f"Created employee count range: id={result.id}, description={result.description}")
    return result

@router.get("/{employee_count_range_id}", response_model=EmployeeCountRangeOut)
async def get_employee_count_range_endpoint(employee_count_range_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_employee_count_range(employee_count_range_id)
    if not result:
        logger.warning(f"Employee count range not found: id={employee_count_range_id}")
        raise HTTPException(status_code=404, detail="Employee count range not found")
    logger.info(f"Retrieved employee count range: id={result.id}, description={result.description}")
    return result

@router.get("/", response_model=List[EmployeeCountRangeOut])
async def get_all_employee_count_ranges_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_employee_count_ranges()
    logger.info(f"Retrieved {len(results)} employee count ranges")
    return results

@router.put("/{employee_count_range_id}", response_model=EmployeeCountRangeOut)
async def update_employee_count_range_endpoint(employee_count_range_id: int, employee_count_range: EmployeeCountRangeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_employee_count_range(employee_count_range_id, employee_count_range)
    if not result:
        logger.warning(f"Failed to update employee count range: id={employee_count_range_id}")
        raise HTTPException(status_code=404, detail="Employee count range not found or description already exists")
    logger.info(f"Updated employee count range: id={result.id}, description={result.description}")
    return result

@router.delete("/{employee_count_range_id}")
async def delete_employee_count_range_endpoint(employee_count_range_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_employee_count_range(employee_count_range_id)
    if not result:
        logger.warning(f"Employee count range not found for deletion: id={employee_count_range_id}")
        raise HTTPException(status_code=404, detail="Employee count range not found")
    logger.info(f"Deleted employee count range: id={employee_count_range_id}")
    return {"message": "Employee count range deleted"}
```

### File: /app/schemas/ethnicity.py
### Part: Schema - Pydantic models for ethnicity CRUD
```python
from pydantic import BaseModel, constr
from typing import Optional

class EthnicityCreate(BaseModel):
    name_en: constr(max_length=128)
    name_th: Optional[constr(max_length=128)] = None

class EthnicityUpdate(BaseModel):
    name_en: Optional[constr(max_length=128)] = None
    name_th: Optional[constr(max_length=128)] = None

class EthnicityOut(BaseModel):
    id: int
    name_en: str
    name_th: Optional[str] = None

    class Config:
        from_attributes = True
```

### File: /app/models/ethnicity.py
### Part: Model - Database operations for ethnicity CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.ethnicity import EthnicityCreate, EthnicityUpdate, EthnicityOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_ethnicity(ethnicity: EthnicityCreate) -> Optional[EthnicityOut]:
    query = """
        SELECT id, name_en, name_th FROM ethnicity WHERE name_en = :name_en
    """
    existing = await database.fetch_one(query=query, values={"name_en": ethnicity.name_en})
    if existing:
        logger.warning(f"Ethnicity with name_en '{ethnicity.name_en}' already exists")
        return None

    query = """
        INSERT INTO ethnicity (name_en, name_th)
        VALUES (:name_en, :name_th)
        RETURNING id, name_en, name_th
    """
    try:
        result = await database.fetch_one(query=query, values={"name_en": ethnicity.name_en, "name_th": ethnicity.name_th})
        logger.info(f"Created ethnicity: id={result['id']}, name_en={result['name_en']}")
        return EthnicityOut(**result)
    except Exception as e:
        logger.error(f"Error creating ethnicity: {str(e)}")
        raise

async def get_ethnicity(ethnicity_id: int) -> Optional[EthnicityOut]:
    query = """
        SELECT id, name_en, name_th FROM ethnicity WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": ethnicity_id})
    if not result:
        logger.warning(f"Ethnicity not found: id={ethnicity_id}")
        return None
    logger.info(f"Retrieved ethnicity: id={result['id']}, name_en={result['name_en']}")
    return EthnicityOut(**result)

async def get_all_ethnicities() -> List[EthnicityOut]:
    query = """
        SELECT id, name_en, name_th FROM ethnicity
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} ethnicities")
    return [EthnicityOut(**result) for result in results]

async def update_ethnicity(ethnicity_id: int, ethnicity: EthnicityUpdate) -> Optional[EthnicityOut]:
    if ethnicity.name_en:
        query = """
            SELECT id, name_en, name_th FROM ethnicity WHERE name_en = :name_en AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"name_en": ethnicity.name_en, "id": ethnicity_id})
        if existing:
            logger.warning(f"Ethnicity with name_en '{ethnicity.name_en}' already exists")
            return None

    query = """
        UPDATE ethnicity
        SET name_en = COALESCE(:name_en, name_en),
            name_th = COALESCE(:name_th, name_th)
        WHERE id = :id
        RETURNING id, name_en, name_th
    """
    try:
        result = await database.fetch_one(query=query, values={"name_en": ethnicity.name_en, "name_th": ethnicity.name_th, "id": ethnicity_id})
        if not result:
            logger.warning(f"Ethnicity not found for update: id={ethnicity_id}")
            return None
        logger.info(f"Updated ethnicity: id={result['id']}, name_en={result['name_en']}")
        return EthnicityOut(**result)
    except Exception as e:
        logger.error(f"Error updating ethnicity: {str(e)}")
        raise

async def delete_ethnicity(ethnicity_id: int) -> bool:
    query = """
        DELETE FROM ethnicity WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": ethnicity_id})
    if not result:
        logger.warning(f"Ethnicity not found for deletion: id={ethnicity_id}")
        return False
    logger.info(f"Deleted ethnicity: id={ethnicity_id}")
    return True
```

### File: /app/controllers/ethnicity.py
### Part: Controller - API endpoints for ethnicity CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.ethnicity import (
    create_ethnicity, get_ethnicity, get_all_ethnicities,
    update_ethnicity, delete_ethnicity
)
from app.schemas.ethnicity import EthnicityCreate, EthnicityUpdate, EthnicityOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/ethnicity", tags=["ethnicity"])

@router.post("/", response_model=EthnicityOut)
async def create_ethnicity_endpoint(ethnicity: EthnicityCreate, current_user: dict = Depends(get_current_user)):
    result = await create_ethnicity(ethnicity)
    if not result:
        logger.warning(f"Failed to create ethnicity: name_en={ethnicity.name_en}")
        raise HTTPException(status_code=400, detail="Name_en already exists")
    logger.info(f"Created ethnicity: id={result.id}, name_en={result.name_en}")
    return result

@router.get("/{ethnicity_id}", response_model=EthnicityOut)
async def get_ethnicity_endpoint(ethnicity_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_ethnicity(ethnicity_id)
    if not result:
        logger.warning(f"Ethnicity not found: id={ethnicity_id}")
        raise HTTPException(status_code=404, detail="Ethnicity not found")
    logger.info(f"Retrieved ethnicity: id={result.id}, name_en={result.name_en}")
    return result

@router.get("/", response_model=List[EthnicityOut])
async def get_all_ethnicities_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_ethnicities()
    logger.info(f"Retrieved {len(results)} ethnicities")
    return results

@router.put("/{ethnicity_id}", response_model=EthnicityOut)
async def update_ethnicity_endpoint(ethnicity_id: int, ethnicity: EthnicityUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_ethnicity(ethnicity_id, ethnicity)
    if not result:
        logger.warning(f"Failed to update ethnicity: id={ethnicity_id}")
        raise HTTPException(status_code=404, detail="Ethnicity not found or name_en already exists")
    logger.info(f"Updated ethnicity: id={result.id}, name_en={result.name_en}")
    return result

@router.delete("/{ethnicity_id}")
async def delete_ethnicity_endpoint(ethnicity_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_ethnicity(ethnicity_id)
    if not result:
        logger.warning(f"Ethnicity not found for deletion: id={ethnicity_id}")
        raise HTTPException(status_code=404, detail="Ethnicity not found")
    logger.info(f"Deleted ethnicity: id={ethnicity_id}")
    return {"message": "Ethnicity deleted"}
```

### File: /app/schemas/income_range.py
### Part: Schema - Pydantic models for income_range CRUD
```python
from pydantic import BaseModel, constr
from typing import Optional

class IncomeRangeCreate(BaseModel):
    description: constr(max_length=128)

class IncomeRangeUpdate(BaseModel):
    description: Optional[constr(max_length=128)] = None

class IncomeRangeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True
```

### File: /app/models/income_range.py
### Part: Model - Database operations for income_range CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.income_range import IncomeRangeCreate, IncomeRangeUpdate, IncomeRangeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_income_range(income_range: IncomeRangeCreate) -> Optional[IncomeRangeOut]:
    query = """
        SELECT id, description FROM income_range WHERE description = :description
    """
    existing = await database.fetch_one(query=query, values={"description": income_range.description})
    if existing:
        logger.warning(f"Income range with description '{income_range.description}' already exists")
        return None

    query = """
        INSERT INTO income_range (description)
        VALUES (:description)
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": income_range.description})
        logger.info(f"Created income range: id={result['id']}, description={result['description']}")
        return IncomeRangeOut(**result)
    except Exception as e:
        logger.error(f"Error creating income range: {str(e)}")
        raise

async def get_income_range(income_range_id: int) -> Optional[IncomeRangeOut]:
    query = """
        SELECT id, description FROM income_range WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": income_range_id})
    if not result:
        logger.warning(f"Income range not found: id={income_range_id}")
        return None
    logger.info(f"Retrieved income range: id={result['id']}, description={result['description']}")
    return IncomeRangeOut(**result)

async def get_all_income_ranges() -> List[IncomeRangeOut]:
    query = """
        SELECT id, description FROM income_range
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} income ranges")
    return [IncomeRangeOut(**result) for result in results]

async def update_income_range(income_range_id: int, income_range: IncomeRangeUpdate) -> Optional[IncomeRangeOut]:
    if income_range.description:
        query = """
            SELECT id, description FROM income_range WHERE description = :description AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"description": income_range.description, "id": income_range_id})
        if existing:
            logger.warning(f"Income range with description '{income_range.description}' already exists")
            return None

    query = """
        UPDATE income_range
        SET description = COALESCE(:description, description)
        WHERE id = :id
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": income_range.description, "id": income_range_id})
        if not result:
            logger.warning(f"Income range not found for update: id={income_range_id}")
            return None
        logger.info(f"Updated income range: id={result['id']}, description={result['description']}")
        return IncomeRangeOut(**result)
    except Exception as e:
        logger.error(f"Error updating income range: {str(e)}")
        raise

async def delete_income_range(income_range_id: int) -> bool:
    query = """
        DELETE FROM income_range WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": income_range_id})
    if not result:
        logger.warning(f"Income range not found for deletion: id={income_range_id}")
        return False
    logger.info(f"Deleted income range: id={income_range_id}")
    return True
```

### File: /app/controllers/income_range.py
### Part: Controller - API endpoints for income_range CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.income_range import (
    create_income_range, get_income_range, get_all_income_ranges,
    update_income_range, delete_income_range
)
from app.schemas.income_range import IncomeRangeCreate, IncomeRangeUpdate, IncomeRangeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/income_range", tags=["income_range"])

@router.post("/", response_model=IncomeRangeOut)
async def create_income_range_endpoint(income_range: IncomeRangeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_income_range(income_range)
    if not result:
        logger.warning(f"Failed to create income range: description={income_range.description}")
        raise HTTPException(status_code=400, detail="Description already exists")
    logger.info(f"Created income range: id={result.id}, description={result.description}")
    return result

@router.get("/{income_range_id}", response_model=IncomeRangeOut)
async def get_income_range_endpoint(income_range_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_income_range(income_range_id)
    if not result:
        logger.warning(f"Income range not found: id={income_range_id}")
        raise HTTPException(status_code=404, detail="Income range not found")
    logger.info(f"Retrieved income range: id={result.id}, description={result.description}")
    return result

@router.get("/", response_model=List[IncomeRangeOut])
async def get_all_income_ranges_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_income_ranges()
    logger.info(f"Retrieved {len(results)} income ranges")
    return results

@router.put("/{income_range_id}", response_model=IncomeRangeOut)
async def update_income_range_endpoint(income_range_id: int, income_range: IncomeRangeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_income_range(income_range_id, income_range)
    if not result:
        logger.warning(f"Failed to update income range: id={income_range_id}")
        raise HTTPException(status_code=404, detail="Income range not found or description already exists")
    logger.info(f"Updated income range: id={result.id}, description={result.description}")
    return result

@router.delete("/{income_range_id}")
async def delete_income_range_endpoint(income_range_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_income_range(income_range_id)
    if not result:
        logger.warning(f"Income range not found for deletion: id={income_range_id}")
        raise HTTPException(status_code=404, detail="Income range not found")
    logger.info(f"Deleted income range: id={income_range_id}")
    return {"message": "Income range deleted"}
```

### File: /app/schemas/physical_characteristic_type.py
### Part: Schema - Pydantic models for physicalcharacteristictype CRUD
```python
from pydantic import BaseModel, constr
from typing import Optional

class PhysicalCharacteristicTypeCreate(BaseModel):
    description: constr(max_length=128)

class PhysicalCharacteristicTypeUpdate(BaseModel):
    description: Optional[constr(max_length=128)] = None

class PhysicalCharacteristicTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True
```

### File: /app/models/physical_characteristic_type.py
### Part: Model - Database operations for physicalcharacteristictype CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.physical_characteristic_type import PhysicalCharacteristicTypeCreate, PhysicalCharacteristicTypeUpdate, PhysicalCharacteristicTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_physical_characteristic_type(physical_characteristic_type: PhysicalCharacteristicTypeCreate) -> Optional[PhysicalCharacteristicTypeOut]:
    query = """
        SELECT id, description FROM physicalcharacteristictype WHERE description = :description
    """
    existing = await database.fetch_one(query=query, values={"description": physical_characteristic_type.description})
    if existing:
        logger.warning(f"Physical characteristic type with description '{physical_characteristic_type.description}' already exists")
        return None

    query = """
 Going to continue generating the CRUD operations for the remaining tables (`physicalcharacteristictype`, `personnametype`, and `country`) based on the provided schema and the pattern established in the previous responses. I'll ensure each table has schema, model, and controller files with consistent structure, using named parameters for queries, and maintaining the `/v1/` prefix for API endpoints as requested. The code will include validation for unique fields, logging, and admin-only access via JWT.

---

### File: /app/models/physical_characteristic_type.py (continued)
### Part: Model - Database operations for physicalcharacteristictype CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.physical_characteristic_type import PhysicalCharacteristicTypeCreate, PhysicalCharacteristicTypeUpdate, PhysicalCharacteristicTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_physical_characteristic_type(physical_characteristic_type: PhysicalCharacteristicTypeCreate) -> Optional[PhysicalCharacteristicTypeOut]:
    query = """
        SELECT id, description FROM physicalcharacteristictype WHERE description = :description
    """
    existing = await database.fetch_one(query=query, values={"description": physical_characteristic_type.description})
    if existing:
        logger.warning(f"Physical characteristic type with description '{physical_characteristic_type.description}' already exists")
        return None

    query = """
        INSERT INTO physicalcharacteristictype (description)
        VALUES (:description)
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": physical_characteristic_type.description})
        logger.info(f"Created physical characteristic type: id={result['id']}, description={result['description']}")
        return PhysicalCharacteristicTypeOut(**result)
    except Exception as e:
        logger.error(f"Error creating physical characteristic type: {str(e)}")
        raise

async def get_physical_characteristic_type(physical_characteristic_type_id: int) -> Optional[PhysicalCharacteristicTypeOut]:
    query = """
        SELECT id, description FROM physicalcharacteristictype WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": physical_characteristic_type_id})
    if not result:
        logger.warning(f"Physical characteristic type not found: id={physical_characteristic_type_id}")
        return None
    logger.info(f"Retrieved physical characteristic type: id={result['id']}, description={result['description']}")
    return PhysicalCharacteristicTypeOut(**result)

async def get_all_physical_characteristic_types() -> List[PhysicalCharacteristicTypeOut]:
    query = """
        SELECT id, description FROM physicalcharacteristictype
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} physical characteristic types")
    return [PhysicalCharacteristicTypeOut(**result) for result in results]

async def update_physical_characteristic_type(physical_characteristic_type_id: int, physical_characteristic_type: PhysicalCharacteristicTypeUpdate) -> Optional[PhysicalCharacteristicTypeOut]:
    if physical_characteristic_type.description:
        query = """
            SELECT id, description FROM physicalcharacteristictype WHERE description = :description AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"description": physical_characteristic_type.description, "id": physical_characteristic_type_id})
        if existing:
            logger.warning(f"Physical characteristic type with description '{physical_characteristic_type.description}' already exists")
            return None

    query = """
        UPDATE physicalcharacteristictype
        SET description = COALESCE(:description, description)
        WHERE id = :id
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": physical_characteristic_type.description, "id": physical_characteristic_type_id})
        if not result:
            logger.warning(f"Physical characteristic type not found for update: id={physical_characteristic_type_id}")
            return None
        logger.info(f"Updated physical characteristic type: id={result['id']}, description={result['description']}")
        return PhysicalCharacteristicTypeOut(**result)
    except Exception as e:
        logger.error(f"Error updating physical characteristic type: {str(e)}")
        raise

async def delete_physical_characteristic_type(physical_characteristic_type_id: int) -> bool:
    query = """
        DELETE FROM physicalcharacteristictype WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": physical_characteristic_type_id})
    if not result:
        logger.warning(f"Physical characteristic type not found for deletion: id={physical_characteristic_type_id}")
        return False
    logger.info(f"Deleted physical characteristic type: id={physical_characteristic_type_id}")
    return True
```

### File: /app/controllers/physical_characteristic_type.py
### Part: Controller - API endpoints for physicalcharacteristictype CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.physical_characteristic_type import (
    create_physical_characteristic_type, get_physical_characteristic_type, get_all_physical_characteristic_types,
    update_physical_characteristic_type, delete_physical_characteristic_type
)
from app.schemas.physical_characteristic_type import PhysicalCharacteristicTypeCreate, PhysicalCharacteristicTypeUpdate, PhysicalCharacteristicTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/physical_characteristic_type", tags=["physical_characteristic_type"])

@router.post("/", response_model=PhysicalCharacteristicTypeOut)
async def create_physical_characteristic_type_endpoint(physical_characteristic_type: PhysicalCharacteristicTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_physical_characteristic_type(physical_characteristic_type)
    if not result:
        logger.warning(f"Failed to create physical characteristic type: description={physical_characteristic_type.description}")
        raise HTTPException(status_code=400, detail="Description already exists")
    logger.info(f"Created physical characteristic type: id={result.id}, description={result.description}")
    return result

@router.get("/{physical_characteristic_type_id}", response_model=PhysicalCharacteristicTypeOut)
async def get_physical_characteristic_type_endpoint(physical_characteristic_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_physical_characteristic_type(physical_characteristic_type_id)
    if not result:
        logger.warning(f"Physical characteristic type not found: id={physical_characteristic_type_id}")
        raise HTTPException(status_code=404, detail="Physical characteristic type not found")
    logger.info(f"Retrieved physical characteristic type: id={result.id}, description={result.description}")
    return result

@router.get("/", response_model=List[PhysicalCharacteristicTypeOut])
async def get_all_physical_characteristic_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_physical_characteristic_types()
    logger.info(f"Retrieved {len(results)} physical characteristic types")
    return results

@router.put("/{physical_characteristic_type_id}", response_model=PhysicalCharacteristicTypeOut)
async def update_physical_characteristic_type_endpoint(physical_characteristic_type_id: int, physical_characteristic_type: PhysicalCharacteristicTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_physical_characteristic_type(physical_characteristic_type_id, physical_characteristic_type)
    if not result:
        logger.warning(f"Failed to update physical characteristic type: id={physical_characteristic_type_id}")
        raise HTTPException(status_code=404, detail="Physical characteristic type not found or description already exists")
    logger.info(f"Updated physical characteristic type: id={result.id}, description={result.description}")
    return result

@router.delete("/{physical_characteristic_type_id}")
async def delete_physical_characteristic_type_endpoint(physical_characteristic_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_physical_characteristic_type(physical_characteristic_type_id)
    if not result:
        logger.warning(f"Physical characteristic type not found for deletion: id={physical_characteristic_type_id}")
        raise HTTPException(status_code=404, detail="Physical characteristic type not found")
    logger.info(f"Deleted physical characteristic type: id={physical_characteristic_type_id}")
    return {"message": "Physical characteristic type deleted"}
```

### File: /app/schemas/person_name_type.py
### Part: Schema - Pydantic models for personnametype CRUD
```python
from pydantic import BaseModel, constr
from typing import Optional

class PersonNameTypeCreate(BaseModel):
    description: constr(max_length=128)

class PersonNameTypeUpdate(BaseModel):
    description: Optional[constr(max_length=128)] = None

class PersonNameTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True
```

### File: /app/models/person_name_type.py
### Part: Model - Database operations for personnametype CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.person_name_type import PersonNameTypeCreate, PersonNameTypeUpdate, PersonNameTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_person_name_type(person_name_type: PersonNameTypeCreate) -> Optional[PersonNameTypeOut]:
    query = """
        SELECT id, description FROM personnametype WHERE description = :description
    """
    existing = await database.fetch_one(query=query, values={"description": person_name_type.description})
    if existing:
        logger.warning(f"Person name type with description '{person_name_type.description}' already exists")
        return None

    query = """
        INSERT INTO personnametype (description)
        VALUES (:description)
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": person_name_type.description})
        logger.info(f"Created person name type: id={result['id']}, description={result['description']}")
        return PersonNameTypeOut(**result)
    except Exception as e:
        logger.error(f"Error creating person name type: {str(e)}")
        raise

async def get_person_name_type(person_name_type_id: int) -> Optional[PersonNameTypeOut]:
    query = """
        SELECT id, description FROM personnametype WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": person_name_type_id})
    if not result:
        logger.warning(f"Person name type not found: id={person_name_type_id}")
        return None
    logger.info(f"Retrieved person name type: id={result['id']}, description={result['description']}")
    return PersonNameTypeOut(**result)

async def get_all_person_name_types() -> List[PersonNameTypeOut]:
    query = """
        SELECT id, description FROM personnametype
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} person name types")
    return [PersonNameTypeOut(**result) for result in results]

async def update_person_name_type(person_name_type_id: int, person_name_type: PersonNameTypeUpdate) -> Optional[PersonNameTypeOut]:
    if person_name_type.description:
        query = """
            SELECT id, description FROM personnametype WHERE description = :description AND id != :id
        """
        existing = await database.fetch_one(query=query, values={"description": person_name_type.description, "id": person_name_type_id})
        if existing:
            logger.warning(f"Person name type with description '{person_name_type.description}' already exists")
            return None

    query = """
        UPDATE personnametype
        SET description = COALESCE(:description, description)
        WHERE id = :id
        RETURNING id, description
    """
    try:
        result = await database.fetch_one(query=query, values={"description": person_name_type.description, "id": person_name_type_id})
        if not result:
            logger.warning(f"Person name type not found for update: id={person_name_type_id}")
            return None
        logger.info(f"Updated person name type: id={result['id']}, description={result['description']}")
        return PersonNameTypeOut(**result)
    except Exception as e:
        logger.error(f"Error updating person name type: {str(e)}")
        raise

async def delete_person_name_type(person_name_type_id: int) -> bool:
    query = """
        DELETE FROM personnametype WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": person_name_type_id})
    if not result:
        logger.warning(f"Person name type not found for deletion: id={person_name_type_id}")
        return False
    logger.info(f"Deleted person name type: id={person_name_type_id}")
    return True
```

### File: /app/controllers/person_name_type.py
### Part: Controller - API endpoints for personnametype CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.person_name_type import (
    create_person_name_type, get_person_name_type, get_all_person_name_types,
    update_person_name_type, delete_person_name_type
)
from app.schemas.person_name_type import PersonNameTypeCreate, PersonNameTypeUpdate, PersonNameTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/person_name_type", tags=["person_name_type"])

@router.post("/", response_model=PersonNameTypeOut)
async def create_person_name_type_endpoint(person_name_type: PersonNameTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_person_name_type(person_name_type)
    if not result:
        logger.warning(f"Failed to create person name type: description={person_name_type.description}")
        raise HTTPException(status_code=400, detail="Description already exists")
    logger.info(f"Created person name type: id={result.id}, description={result.description}")
    return result

@router.get("/{person_name_type_id}", response_model=PersonNameTypeOut)
async def get_person_name_type_endpoint(person_name_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_person_name_type(person_name_type_id)
    if not result:
        logger.warning(f"Person name type not found: id={person_name_type_id}")
        raise HTTPException(status_code=404, detail="Person name type not found")
    logger.info(f"Retrieved person name type: id={result.id}, description={result.description}")
    return result

@router.get("/", response_model=List[PersonNameTypeOut])
async def get_all_person_name_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_person_name_types()
    logger.info(f"Retrieved {len(results)} person name types")
    return results

@router.put("/{person_name_type_id}", response_model=PersonNameTypeOut)
async def update_person_name_type_endpoint(person_name_type_id: int, person_name_type: PersonNameTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_person_name_type(person_name_type_id, person_name_type)
    if not result:
        logger.warning(f"Failed to update person name type: id={person_name_type_id}")
        raise HTTPException(status_code=404, detail="Person name type not found or description already exists")
    logger.info(f"Updated person name type: id={result.id}, description={result.description}")
    return result

@router.delete("/{person_name_type_id}")
async def delete_person_name_type_endpoint(person_name_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_person_name_type(person_name_type_id)
    if not result:
        logger.warning(f"Person name type not found for deletion: id={person_name_type_id}")
        raise HTTPException(status_code=404, detail="Person name type not found")
    logger.info(f"Deleted person name type: id={person_name_type_id}")
    return {"message": "Person name type deleted"}
```

### File: /app/schemas/country.py
### Part: Schema - Pydantic models for country CRUD
```python
from pydantic import BaseModel, constr
from typing import Optional

class CountryCreate(BaseModel):
    isocode: constr(max_length=2)
    name_en: constr(max_length=128)
    name_th: Optional[constr(max_length=128)] = None

class CountryUpdate(BaseModel):
    isocode: Optional[constr(max_length=2)] = None
    name_en: Optional[constr(max_length=128)] = None
    name_th: Optional[constr(max_length=128)] = None

class CountryOut(BaseModel):
    id: int
    isocode: str
    name_en: str
    name_th: Optional[str] = None

    class Config:
        from_attributes = True
```

### File: /app/models/country.py
### Part: Model - Database operations for country CRUD
```python
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
```

### File: /app/controllers/country.py
### Part: Controller - API endpoints for country CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.country import (
    create_country, get_country, get_all_countries,
    update_country, delete_country
)
from app.schemas.country import CountryCreate, CountryUpdate, CountryOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/country", tags=["country"])

@router.post("/", response_model=CountryOut)
async def create_country_endpoint(country: CountryCreate, current_user: dict = Depends(get_current_user)):
    result = await create_country(country)
    if not result:
        logger.warning(f"Failed to create country: isocode={country.isocode}")
        raise HTTPException(status_code=400, detail="ISO code already exists")
    logger.info(f"Created country: id={result.id}, isocode={result.isocode}")
    return result

@router.get("/{country_id}", response_model=CountryOut)
async def get_country_endpoint(country_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_country(country_id)
    if not result:
        logger.warning(f"Country not found: id={country_id}")
        raise HTTPException(status_code=404, detail="Country not found")
    logger.info(f"Retrieved country: id={result.id}, isocode={result.isocode}")
    return result

@router.get("/", response_model=List[CountryOut])
async def get_all_countries_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_countries()
    logger.info(f"Retrieved {len(results)} countries")
    return results

@router.put("/{country_id}", response_model=CountryOut)
async def update_country_endpoint(country_id: int, country: CountryUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_country(country_id, country)
    if not result:
        logger.warning(f"Failed to update country: id={country_id}")
        raise HTTPException(status_code=404, detail="Country not found or ISO code already exists")
    logger.info(f"Updated country: id={result.id}, isocode={result.isocode}")
    return result

@router.delete("/{country_id}")
async def delete_country_endpoint(country_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_country(country_id)
    if not result:
        logger.warning(f"Country not found for deletion: id={country_id}")
        raise HTTPException(status_code=404, detail="Country not found")
    logger.info(f"Deleted country: id={country_id}")
    return {"message": "Country deleted"}
```