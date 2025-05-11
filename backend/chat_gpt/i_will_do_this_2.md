### File: /app/schemas/citizenship.py
### Part: Schema - Pydantic models for citizenship CRUD
```python
from pydantic import BaseModel
from typing import Optional
from datetime import date

class CitizenshipCreate(BaseModel):
    fromdate: date
    thrudate: Optional[date] = None
    person_id: int
    country_id: int

class CitizenshipUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    person_id: Optional[int] = None
    country_id: Optional[int] = None

class CitizenshipOut(BaseModel):
    id: int
    fromdate: date
    thrudate: Optional[date] = None
    person_id: int
    country_id: int

    class Config:
        from_attributes = True
```

### File: /app/models/citizenship.py
### Part: Model - Database operations for citizenship CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.citizenship import CitizenshipCreate, CitizenshipUpdate, CitizenshipOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_citizenship(citizenship: CitizenshipCreate) -> Optional[CitizenshipOut]:
    query = """
        SELECT id FROM citizenship 
        WHERE person_id = :person_id AND country_id = :country_id 
        AND fromdate = :fromdate AND (thrudate = :thrudate OR (thrudate IS NULL AND :thrudate IS NULL))
    """
    existing = await database.fetch_one(query=query, values={
        "person_id": citizenship.person_id,
        "country_id": citizenship.country_id,
        "fromdate": citizenship.fromdate,
        "thrudate": citizenship.thrudate
    })
    if existing:
        logger.warning(f"Citizenship already exists for person_id={citizenship.person_id}, country_id={citizenship.country_id}")
        return None

    query = """
        INSERT INTO citizenship (fromdate, thrudate, person_id, country_id)
        VALUES (:fromdate, :thrudate, :person_id, :country_id)
        RETURNING id, fromdate, thrudate, person_id, country_id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "fromdate": citizenship.fromdate,
            "thrudate": citizenship.thrudate,
            "person_id": citizenship.person_id,
            "country_id": citizenship.country_id
        })
        logger.info(f"Created citizenship: id={result['id']}, person_id={result['person_id']}")
        return CitizenshipOut(**result)
    except Exception as e:
        logger.error(f"Error creating citizenship: {str(e)}")
        raise

async def get_citizenship(citizenship_id: int) -> Optional[CitizenshipOut]:
    query = """
        SELECT id, fromdate, thrudate, person_id, country_id 
        FROM citizenship WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": citizenship_id})
    if not result:
        logger.warning(f"Citizenship not found: id={citizenship_id}")
        return None
    logger.info(f"Retrieved citizenship: id={result['id']}, person_id={result['person_id']}")
    return CitizenshipOut(**result)

async def get_all_citizenships() -> List[CitizenshipOut]:
    query = """
        SELECT id, fromdate, thrudate, person_id, country_id 
        FROM citizenship
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} citizenships")
    return [CitizenshipOut(**result) for result in results]

async def update_citizenship(citizenship_id: int, citizenship: CitizenshipUpdate) -> Optional[CitizenshipOut]:
    if any([citizenship.fromdate, citizenship.thrudate, citizenship.person_id, citizenship.country_id]):
        query = """
            SELECT id FROM citizenship 
            WHERE person_id = COALESCE(:person_id, person_id) 
            AND country_id = COALESCE(:country_id, country_id)
            AND fromdate = COALESCE(:fromdate, fromdate)
            AND (thrudate = COALESCE(:thrudate, thrudate) OR (thrudate IS NULL AND :thrudate IS NULL))
            AND id != :id
        """
        existing = await database.fetch_one(query=query, values={
            "person_id": citizenship.person_id,
            "country_id": citizenship.country_id,
            "fromdate": citizenship.fromdate,
            "thrudate": citizenship.thrudate,
            "id": citizenship_id
        })
        if existing:
            logger.warning(f"Citizenship already exists for person_id={citizenship.person_id}, country_id={citizenship.country_id}")
            return None

    query = """
        UPDATE citizenship
        SET fromdate = COALESCE(:fromdate, fromdate),
            thrudate = COALESCE(:thrudate, thrudate),
            person_id = COALESCE(:person_id, person_id),
            country_id = COALESCE(:country_id, country_id)
        WHERE id = :id
        RETURNING id, fromdate, thrudate, person_id, country_id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "fromdate": citizenship.fromdate,
            "thrudate": citizenship.thrudate,
            "person_id": citizenship.person_id,
            "country_id": citizenship.country_id,
            "id": citizenship_id
        })
        if not result:
            logger.warning(f"Citizenship not found for update: id={citizenship_id}")
            return None
        logger.info(f"Updated citizenship: id={result['id']}, person_id={result['person_id']}")
        return CitizenshipOut(**result)
    except Exception as e:
        logger.error(f"Error updating citizenship: {str(e)}")
        raise

async def delete_citizenship(citizenship_id: int) -> bool:
    query = """
        SELECT id FROM passport WHERE citizenship_id = :id LIMIT 1
    """
    referenced = await database.fetch_one(query=query, values={"id": citizenship_id})
    if referenced:
        logger.warning(f"Cannot delete citizenship: id={citizenship_id}, referenced in passport")
        return False

    query = """
        DELETE FROM citizenship WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": citizenship_id})
    if not result:
        logger.warning(f"Citizenship not found for deletion: id={citizenship_id}")
        return False
    logger.info(f"Deleted citizenship: id={citizenship_id}")
    return True
```

### File: /app/controllers/citizenship.py
### Part: Controller - API endpoints for citizenship CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.citizenship import (
    create_citizenship, get_citizenship, get_all_citizenships,
    update_citizenship, delete_citizenship
)
from app.schemas.citizenship import CitizenshipCreate, CitizenshipUpdate, CitizenshipOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/citizenship", tags=["citizenship"])

@router.post("/", response_model=CitizenshipOut)
async def create_citizenship_endpoint(citizenship: CitizenshipCreate, current_user: dict = Depends(get_current_user)):
    result = await create_citizenship(citizenship)
    if not result:
        logger.warning(f"Failed to create citizenship: person_id={citizenship.person_id}, country_id={citizenship.country_id}")
        raise HTTPException(status_code=400, detail="Citizenship already exists")
    logger.info(f"Created citizenship: id={result.id}, person_id={result.person_id}")
    return result

@router.get("/{citizenship_id}", response_model=CitizenshipOut)
async def get_citizenship_endpoint(citizenship_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_citizenship(citizenship_id)
    if not result:
        logger.warning(f"Citizenship not found: id={citizenship_id}")
        raise HTTPException(status_code=404, detail="Citizenship not found")
    logger.info(f"Retrieved citizenship: id={result.id}, person_id={result.person_id}")
    return result

@router.get("/", response_model=List[CitizenshipOut])
async def get_all_citizenships_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_citizenships()
    logger.info(f"Retrieved {len(results)} citizenships")
    return results

@router.put("/{citizenship_id}", response_model=CitizenshipOut)
async def update_citizenship_endpoint(citizenship_id: int, citizenship: CitizenshipUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_citizenship(citizenship_id, citizenship)
    if not result:
        logger.warning(f"Failed to update citizenship: id={citizenship_id}")
        raise HTTPException(status_code=404, detail="Citizenship not found or already exists")
    logger.info(f"Updated citizenship: id={result.id}, person_id={result.person_id}")
    return result

@router.delete("/{citizenship_id}")
async def delete_citizenship_endpoint(citizenship_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_citizenship(citizenship_id)
    if not result:
        logger.warning(f"Citizenship not found for deletion or referenced: id={citizenship_id}")
        raise HTTPException(status_code=404, detail="Citizenship not found or referenced in passport")
    logger.info(f"Deleted citizenship: id={citizenship_id}")
    return {"message": "Citizenship deleted"}
```

### File: /app/schemas/passport.py
### Part: Schema - Pydantic models for passport CRUD
```python
from pydantic import BaseModel, constr
from typing import Optional
from datetime import date

class PassportCreate(BaseModel):
    passportnumber: constr(max_length=64)
    fromdate: date
    thrudate: date
    citizenship_id: int

class PassportUpdate(BaseModel):
    passportnumber: Optional[constr(max_length=64)] = None
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    citizenship_id: Optional[int] = None

class PassportOut(BaseModel):
    id: int
    passportnumber: str
    fromdate: date
    thrudate: date
    citizenship_id: int

    class Config:
        from_attributes = True
```

### File: /app/models/passport.py
### Part: Model - Database operations for passport CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.passport import PassportCreate, PassportUpdate, PassportOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_passport(passport: PassportCreate) -> Optional[PassportOut]:
    query = """
        SELECT id FROM passport 
        WHERE passportnumber = :passportnumber AND citizenship_id = :citizenship_id
    """
    existing = await database.fetch_one(query=query, values={
        "passportnumber": passport.passportnumber,
        "citizenship_id": passport.citizenship_id
    })
    if existing:
        logger.warning(f"Passport already exists: passportnumber={passport.passportnumber}, citizenship_id={passport.citizenship_id}")
        return None

    query = """
        INSERT INTO passport (passportnumber, fromdate, thrudate, citizenship_id)
        VALUES (:passportnumber, :fromdate, :thrudate, :citizenship_id)
        RETURNING id, passportnumber, fromdate, thrudate, citizenship_id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "passportnumber": passport.passportnumber,
            "fromdate": passport.fromdate,
            "thrudate": passport.thrudate,
            "citizenship_id": passport.citizenship_id
        })
        logger.info(f"Created passport: id={result['id']}, passportnumber={result['passportnumber']}")
        return PassportOut(**result)
    except Exception as e:
        logger.error(f"Error creating passport: {str(e)}")
        raise

async def get_passport(passport_id: int) -> Optional[PassportOut]:
    query = """
        SELECT id, passportnumber, fromdate, thrudate, citizenship_id 
        FROM passport WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": passport_id})
    if not result:
        logger.warning(f"Passport not found: id={passport_id}")
        return None
    logger.info(f"Retrieved passport: id={result['id']}, passportnumber={result['passportnumber']}")
    return PassportOut(**result)

async def get_all_passports() -> List[PassportOut]:
    query = """
        SELECT id, passportnumber, fromdate, thrudate, citizenship_id 
        FROM passport
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} passports")
    return [PassportOut(**result) for result in results]

async def update_passport(passport_id: int, passport: PassportUpdate) -> Optional[PassportOut]:
    if passport.passportnumber or passport.citizenship_id:
        query = """
            SELECT id FROM passport 
            WHERE passportnumber = COALESCE(:passportnumber, passportnumber) 
            AND citizenship_id = COALESCE(:citizenship_id, citizenship_id)
            AND id != :id
        """
        existing = await database.fetch_one(query=query, values={
            "passportnumber": passport.passportnumber,
            "citizenship_id": passport.citizenship_id,
            "id": passport_id
        })
        if existing:
            logger.warning(f"Passport already exists: passportnumber={passport.passportnumber}, citizenship_id={passport.citizenship_id}")
            return None

    query = """
        UPDATE passport
        SET passportnumber = COALESCE(:passportnumber, passportnumber),
            fromdate = COALESCE(:fromdate, fromdate),
            thrudate = COALESCE(:thrudate, thrudate),
            citizenship_id = COALESCE(:citizenship_id, citizenship_id)
        WHERE id = :id
        RETURNING id, passportnumber, fromdate, thrudate, citizenship_id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "passportnumber": passport.passportnumber,
            "fromdate": passport.fromdate,
            "thrudate": passport.thrudate,
            "citizenship_id": passport.citizenship_id,
            "id": passport_id
        })
        if not result:
            logger.warning(f"Passport not found for update: id={passport_id}")
            return None
        logger.info(f"Updated passport: id={result['id']}, passportnumber={result['passportnumber']}")
        return PassportOut(**result)
    except Exception as e:
        logger.error(f"Error updating passport: {str(e)}")
        raise

async def delete_passport(passport_id: int) -> bool:
    query = """
        DELETE FROM passport WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": passport_id})
    if not result:
        logger.warning(f"Passport not found for deletion: id={passport_id}")
        return False
    logger.info(f"Deleted passport: id={passport_id}")
    return True
```

### File: /app/controllers/passport.py
### Part: Controller - API endpoints for passport CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.passport import (
    create_passport, get_passport, get_all_passports,
    update_passport, delete_passport
)
from app.schemas.passport import PassportCreate, PassportUpdate, PassportOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/passport", tags=["passport"])

@router.post("/", response_model=PassportOut)
async def create_passport_endpoint(passport: PassportCreate, current_user: dict = Depends(get_current_user)):
    result = await create_passport(passport)
    if not result:
        logger.warning(f"Failed to create passport: passportnumber={passport.passportnumber}")
        raise HTTPException(status_code=400, detail="Passport already exists")
    logger.info(f"Created passport: id={result.id}, passportnumber={result.passportnumber}")
    return result

@router.get("/{passport_id}", response_model=PassportOut)
async def get_passport_endpoint(passport_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_passport(passport_id)
    if not result:
        logger.warning(f"Passport not found: id={passport_id}")
        raise HTTPException(status_code=404, detail="Passport not found")
    logger.info(f"Retrieved passport: id={result.id}, passportnumber={result.passportnumber}")
    return result

@router.get("/", response_model=List[PassportOut])
async def get_all_passports_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_passports()
    logger.info(f"Retrieved {len(results)} passports")
    return results

@router.put("/{passport_id}", response_model=PassportOut)
async def update_passport_endpoint(passport_id: int, passport: PassportUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_passport(passport_id, passport)
    if not result:
        logger.warning(f"Failed to update passport: id={passport_id}")
        raise HTTPException(status_code=404, detail="Passport not found or already exists")
    logger.info(f"Updated passport: id={result.id}, passportnumber={result.passportnumber}")
    return result

@router.delete("/{passport_id}")
async def delete_passport_endpoint(passport_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_passport(passport_id)
    if not result:
        logger.warning(f"Passport not found for deletion: id={passport_id}")
        raise HTTPException(status_code=404, detail="Passport not found")
    logger.info(f"Deleted passport: id={passport_id}")
    return {"message": "Passport deleted"}
```

### File: /app/schemas/person_name.py
### Part: Schema - Pydantic models for personname CRUD
```python
from pydantic import BaseModel, constr
from typing import Optional
from datetime import date

class PersonNameCreate(BaseModel):
    fromdate: date
    thrudate: Optional[date] = None
    person_id: int
    personnametype_id: int
    name: constr(max_length=128)

class PersonNameUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    person_id: Optional[int] = None
    personnametype_id: Optional[int] = None
    name: Optional[constr(max_length=128)] = None

class PersonNameOut(BaseModel):
    id: int
    fromdate: date
    thrudate: Optional[date] = None
    person_id: int
    personnametype_id: int
    name: str

    class Config:
        from_attributes = True
```

### File: /app/models/person_name.py
### Part: Model - Database operations for personname CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.person_name import PersonNameCreate, PersonNameUpdate, PersonNameOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_person_name(person_name: PersonNameCreate) -> Optional[PersonNameOut]:
    query = """
        SELECT id FROM personname 
        WHERE person_id = :person_id AND personnametype_id = :personnametype_id 
        AND name = :name AND fromdate = :fromdate 
        AND (thrudate = :thrudate OR (thrudate IS NULL AND :thrudate IS NULL))
    """
    existing = await database.fetch_one(query=query, values={
        "person_id": person_name.person_id,
        "personnametype_id": person_name.personnametype_id,
        "name": person_name.name,
        "fromdate": person_name.fromdate,
        "thrudate": person_name.thrudate
    })
    if existing:
        logger.warning(f"Person name already exists: person_id={person_name.person_id}, name={person_name.name}")
        return None

    query = """
        INSERT INTO personname (fromdate, thrudate, person_id, personnametype_id, name)
        VALUES (:fromdate, :thrudate, :person_id, :personnametype_id, :name)
        RETURNING id, fromdate, thrudate, person_id, personnametype_id, name
    """
    try:
        result = await database.fetch_one(query=query, values={
            "fromdate": person_name.fromdate,
            "thrudate": person_name.thrudate,
            "person_id": person_name.person_id,
            "personnametype_id": person_name.personnametype_id,
            "name": person_name.name
        })
        logger.info(f"Created person name: id={result['id']}, name={result['name']}")
        return PersonNameOut(**result)
    except Exception as e:
        logger.error(f"Error creating person name: {str(e)}")
        raise

async def get_person_name(person_name_id: int) -> Optional[PersonNameOut]:
    query = """
        SELECT id, fromdate, thrudate, person_id, personnametype_id, name 
        FROM personname WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": person_name_id})
    if not result:
        logger.warning(f"Person name not found: id={person_name_id}")
        return None
    logger.info(f"Retrieved person name: id={result['id']}, name={result['name']}")
    return PersonNameOut(**result)

async def get_all_person_names() -> List[PersonNameOut]:
    query = """
        SELECT id, fromdate, thrudate, person_id, personnametype_id, name 
        FROM personname
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} person names")
    return [PersonNameOut(**result) for result in results]

async def update_person_name(person_name_id: int, person_name: PersonNameUpdate) -> Optional[PersonNameOut]:
    if any([person_name.fromdate, person_name.thrudate, person_name.person_id, person_name.personnametype_id, person_name.name]):
        query = """
            SELECT id FROM personname 
            WHERE person_id = COALESCE(:person_id, person_id)
            AND personnametype_id = COALESCE(:personnametype_id, personnametype_id)
            AND name = COALESCE(:name, name)
            AND fromdate = COALESCE(:fromdate, fromdate)
            AND (thrudate = COALESCE(:thrudate, thrudate) OR (thrudate IS NULL AND :thrudate IS NULL))
            AND id != :id
        """
        existing = await database.fetch_one(query=query, values={
            "person_id": person_name.person_id,
            "personnametype_id": person_name.personnametype_id,
            "name": person_name.name,
            "fromdate": person_name.fromdate,
            "thrudate": person_name.thrudate,
            "id": person_name_id
        })
        if existing:
            logger.warning(f"Person name already exists: person_id={person_name.person_id}, name={person_name.name}")
            return None

    query = """
        UPDATE personname
        SET fromdate = COALESCE(:fromdate, fromdate),
            thrudate = COALESCE(:thrudate, thrudate),
            person_id = COALESCE(:person_id, person_id),
            personnametype_id = COALESCE(:personnametype_id, personnametype_id),
            name = COALESCE(:name, name)
        WHERE id = :id
        RETURNING id, fromdate, thrudate, person_id, personnametype_id, name
    """
    try:
        result = await database.fetch_one(query=query, values={
            "fromdate": person_name.fromdate,
            "thrudate": person_name.thrudate,
            "person_id": person_name.person_id,
            "personnametype_id": person_name.personnametype_id,
            "name": person_name.name,
            "id": person_name_id
        })
        if not result:
            logger.warning(f"Person name not found for update: id={person_name_id}")
            return None
        logger.info(f"Updated person name: id={result['id']}, name={result['name']}")
        return PersonNameOut(**result)
    except Exception as e:
        logger.error(f"Error updating person name: {str(e)}")
        raise

async def delete_person_name(person_name_id: int) -> bool:
    query = """
        DELETE FROM personname WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": person_name_id})
    if not result:
        logger.warning(f"Person name not found for deletion: id={person_name_id}")
        return False
    logger.info(f"Deleted person name: id={person_name_id}")
    return True
```

### File: /app/controllers/person_name.py
### Part: Controller - API endpoints for personname CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.person_name import (
    create_person_name, get_person_name, get_all_person_names,
    update_person_name, delete_person_name
)
from app.schemas.person_name import PersonNameCreate, PersonNameUpdate, PersonNameOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/person_name", tags=["person_name"])

@router.post("/", response_model=PersonNameOut)
async def create_person_name_endpoint(person_name: PersonNameCreate, current_user: dict = Depends(get_current_user)):
    result = await create_person_name(person_name)
    if not result:
        logger.warning(f"Failed to create person name: name={person_name.name}")
        raise HTTPException(status_code=400, detail="Person name already exists")
    logger.info(f"Created person name: id={result.id}, name={result.name}")
    return result

@router.get("/{person_name_id}", response_model=PersonNameOut)
async def get_person_name_endpoint(person_name_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_person_name(person_name_id)
    if not result:
        logger.warning(f"Person name not found: id={person_name_id}")
        raise HTTPException(status_code=404, detail="Person name not found")
    logger.info(f"Retrieved person name: id={result.id}, name={result.name}")
    return result

@router.get("/", response_model=List[PersonNameOut])
async def get_all_person_names_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_person_names()
    logger.info(f"Retrieved {len(results)} person names")
    return results

@router.put("/{person_name_id}", response_model=PersonNameOut)
async def update_person_name_endpoint(person_name_id: int, person_name: PersonNameUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_person_name(person_name_id, person_name)
    if not result:
        logger.warning(f"Failed to update person name: id={person_name_id}")
        raise HTTPException(status_code=404, detail="Person name not found or already exists")
    logger.info(f"Updated person name: id={result.id}, name={result.name}")
    return result

@router.delete("/{person_name_id}")
async def delete_person_name_endpoint(person_name_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_person_name(person_name_id)
    if not result:
        logger.warning(f"Person name not found for deletion: id={person_name_id}")
        raise HTTPException(status_code=404, detail="Person name not found")
    logger.info(f"Deleted person name: id={person_name_id}")
    return {"message": "Person name deleted"}
```

### File: /app/schemas/physical_characteristic.py
### Part: Schema - Pydantic models for physicalcharacteristic CRUD
```python
from pydantic import BaseModel
from typing import Optional
from datetime import date

class PhysicalCharacteristicCreate(BaseModel):
    fromdate: date
    thrudate: Optional[date] = None
    val: int
    person_id: int
    physicalcharacteristictype_id: int

class PhysicalCharacteristicUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    val: Optional[int] = None
    person_id: Optional[int] = None
    physicalcharacteristictype_id: Optional[int] = None

class PhysicalCharacteristicOut(BaseModel):
    id: int
    fromdate: date
    thrudate: Optional[date] = None
    val: int
    person_id: int
    physicalcharacteristictype_id: int

    class Config:
        from_attributes = True
```

### File: /app/models/physical_characteristic.py
### Part: Model - Database operations for physicalcharacteristic CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.physical_characteristic import PhysicalCharacteristicCreate, PhysicalCharacteristicUpdate, PhysicalCharacteristicOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_physical_characteristic(physical_characteristic: PhysicalCharacteristicCreate) -> Optional[PhysicalCharacteristicOut]:
    query = """
        SELECT id FROM physicalcharacteristic 
        WHERE person_id = :person_id AND physicalcharacteristictype_id = :physicalcharacteristictype_id 
        AND val = :val AND fromdate = :fromdate 
        AND (thrudate = :thrudate OR (thrudate IS NULL AND :thrudate IS NULL))
    """
    existing = await database.fetch_one(query=query, values={
        "person_id": physical_characteristic.person_id,
        "physicalcharacteristictype_id": physical_characteristic.physicalcharacteristictype_id,
        "val": physical_characteristic.val,
        "fromdate": physical_characteristic.fromdate,
        "thrudate": physical_characteristic.thrudate
    })
    if existing:
        logger.warning(f"Physical characteristic already exists: person_id={physical_characteristic.person_id}, type_id={physical_characteristic.physicalcharacteristictype_id}")
        return None

    query = """
        INSERT INTO physicalcharacteristic (fromdate, thrudate, val, person_id, physicalcharacteristictype_id)
        VALUES (:fromdate, :thrudate, :val, :person_id, :physicalcharacteristictype_id)
        RETURNING id, fromdate, thrudate, val, person_id, physicalcharacteristictype_id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "fromdate": physical_characteristic.fromdate,
            "thrudate": physical_characteristic.thrudate,
            "val": physical_characteristic.val,
            "person_id": physical_characteristic.person_id,
            "physicalcharacteristictype_id": physical_characteristic.physicalcharacteristictype_id
        })
        logger.info(f"Created physical characteristic: id={result['id']}, person_id={result['person_id']}")
        return PhysicalCharacteristicOut(**result)
    except Exception as e:
        logger.error(f"Error creating physical characteristic: {str(e)}")
        raise

async def get_physical_characteristic(physical_characteristic_id: int) -> Optional[PhysicalCharacteristicOut]:
    query = """
        SELECT id, fromdate, thrudate, val, person_id, physicalcharacteristictype_id 
        FROM physicalcharacteristic WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": physical_characteristic_id})
    if not result:
        logger.warning(f"Physical characteristic not found: id={physical_characteristic_id}")
        return None
    logger.info(f"Retrieved physical characteristic: id={result['id']}, person_id={result['person_id']}")
    return PhysicalCharacteristicOut(**result)

async def get_all_physical_characteristics() -> List[PhysicalCharacteristicOut]:
    query = """
        SELECT id, fromdate, thrudate, val, person_id, physicalcharacteristictype_id 
        FROM physicalcharacteristic
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} physical characteristics")
    return [PhysicalCharacteristicOut(**result) for result in results]

async def update_physical_characteristic(physical_characteristic_id: int, physical_characteristic: PhysicalCharacteristicUpdate) -> Optional[PhysicalCharacteristicOut]:
    if any([physical_characteristic.fromdate, physical_characteristic.thrudate, physical_characteristic.val, physical_characteristic.person_id, physical_characteristic.physicalcharacteristictype_id]):
        query = """
            SELECT id FROM physicalcharacteristic 
            WHERE person_id = COALESCE(:person_id, person_id)
            AND physicalcharacteristictype_id = COALESCE(:physicalcharacteristictype_id, physicalcharacteristictype_id)
            AND val = COALESCE(:val, val)
            AND fromdate = COALESCE(:fromdate, fromdate)
            AND (thrudate = COALESCE(:thrudate, thrudate) OR (thrudate IS NULL AND :thrudate IS NULL))
            AND id != :id
        """
        existing = await database.fetch_one(query=query, values={
            "person_id": physical_characteristic.person_id,
            "physicalcharacteristictype_id": physical_characteristic.physicalcharacteristictype_id,
            "val": physical_characteristic.val,
            "fromdate": physical_characteristic.fromdate,
            "thrudate": physical_characteristic.thrudate,
            "id": physical_characteristic_id
        })
        if existing:
            logger.warning(f"Physical characteristic already exists: person_id={physical_characteristic.person_id}, type_id={physical_characteristic.physicalcharacteristictype_id}")
            return None

    query = """
        UPDATE physicalcharacteristic
        SET fromdate = COALESCE(:fromdate, fromdate),
            thrudate = COALESCE(:thrudate, thrudate),
            val = COALESCE(:val, val),
            person_id = COALESCE(:person_id, person_id),
            physicalcharacteristictype_id = COALESCE(:physicalcharacteristictype_id, physicalcharacteristictype_id)
        WHERE id = :id
        RETURNING id, fromdate, thrudate, val, person_id, physicalcharacteristictype_id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "fromdate": physical_characteristic.fromdate,
            "thrudate": physical_characteristic.thrudate,
            "val": physical_characteristic.val,
            "person_id": physical_characteristic.person_id,
            "physicalcharacteristictype_id": physical_characteristic.physicalcharacteristictype_id,
            "id": physical_characteristic_id
        })
        if not result:
            logger.warning(f"Physical characteristic not found for update: id={physical_characteristic_id}")
            return None
        logger.info(f"Updated physical characteristic: id={result['id']}, person_id={result['person_id']}")
        return PhysicalCharacteristicOut(**result)
    except Exception as e:
        logger.error(f"Error updating physical characteristic: {str(e)}")
        raise

async def delete_physical_characteristic(physical_characteristic_id: int) -> bool:
    query = """
        DELETE FROM physicalcharacteristic WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": physical_characteristic_id})
    if not result:
        logger.warning(f"Physical characteristic not found for deletion: id={physical_characteristic_id}")
        return False
    logger.info(f"Deleted physical characteristic: id={physical_characteristic_id}")
    return True
```

### File: /app/controllers/physical_characteristic.py
### Part: Controller - API endpoints for physicalcharacteristic CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.physical_characteristic import (
    create_physical_characteristic, get_physical_characteristic, get_all_physical_characteristics,
    update_physical_characteristic, delete_physical_characteristic
)
from app.schemas.physical_characteristic import PhysicalCharacteristicCreate, PhysicalCharacteristicUpdate, PhysicalCharacteristicOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/physical_characteristic", tags=["physical_characteristic"])

@router.post("/", response_model=PhysicalCharacteristicOut)
async def create_physical_characteristic_endpoint(physical_characteristic: PhysicalCharacteristicCreate, current_user: dict = Depends(get_current_user)):
    result = await create_physical_characteristic(physical_characteristic)
    if not result:
        logger.warning(f"Failed to create physical characteristic: person_id={physical_characteristic.person_id}")
        raise HTTPException(status_code=400, detail="Physical characteristic already exists")
    logger.info(f"Created physical characteristic: id={result.id}, person_id={result.person_id}")
    return result

@router.get("/{physical_characteristic_id}", response_model=PhysicalCharacteristicOut)
async def get_physical_characteristic_endpoint(physical_characteristic_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_physical_characteristic(physical_characteristic_id)
    if not result:
        logger.warning(f"Physical characteristic not found: id={physical_characteristic_id}")
        raise HTTPException(status_code=404, detail="Physical characteristic not found")
    logger.info(f"Retrieved physical characteristic: id={result.id}, person_id={result.person_id}")
    return result

@router.get("/", response_model=List[PhysicalCharacteristicOut])
async def get_all_physical_characteristics_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_physical_characteristics()
    logger.info(f"Retrieved {len(results)} physical characteristics")
    return results

@router.put("/{physical_characteristic_id}", response_model=PhysicalCharacteristicOut)
async def update_physical_characteristic_endpoint(physical_characteristic_id: int, physical_characteristic: PhysicalCharacteristicUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_physical_characteristic(physical_characteristic_id, physical_characteristic)
    if not result:
        logger.warning(f"Failed to update physical characteristic: id={physical_characteristic_id}")
        raise HTTPException(status_code=404, detail="Physical characteristic not found or already exists")
    logger.info(f"Updated physical characteristic: id={result.id}, person_id={result.person_id}")
    return result

@router.delete("/{physical_characteristic_id}")
async def delete_physical_characteristic_endpoint(physical_characteristic_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_physical_characteristic(physical_characteristic_id)
    if not result:
        logger.warning(f"Physical characteristic not found for deletion: id={physical_characteristic_id}")
        raise HTTPException(status_code=404, detail="Physical characteristic not found")
    logger.info(f"Deleted physical characteristic: id={physical_characteristic_id}")
    return {"message": "Physical characteristic deleted"}
```

### File: /app/schemas/marital_status.py
### Part: Schema - Pydantic models for maritalstatus CRUD
```python
from pydantic import BaseModel
from typing import Optional
from datetime import date

class MaritalStatusCreate(BaseModel):
    fromdate: date
    thrudate: Optional[date] = None
    person_id: int
    maritalstatustype_id: int

class MaritalStatusUpdate(BaseModel):
    fromdate: Optional[date] = None
    thrudate: Optional[date] = None
    person_id: Optional[int] = None
    maritalstatustype_id: Optional[int] = None

class MaritalStatusOut(BaseModel):
    id: int
    fromdate: date
    thrudate: Optional[date] = None
    person_id: int
    maritalstatustype_id: int

    class Config:
        from_attributes = True
```

### File: /app/models/marital_status.py
### Part: Model - Database operations for maritalstatus CRUD
```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.marital_status import MaritalStatusCreate, MaritalStatusUpdate, MaritalStatusOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_marital_status(marital_status: MaritalStatusCreate) -> Optional[MaritalStatusOut]:
    query = """
        SELECT id FROM maritalstatus 
        WHERE person_id = :person_id AND maritalstatustype_id = :maritalstatustype_id 
        AND fromdate = :fromdate 
        AND (thrudate = :thrudate OR (thrudate IS NULL AND :thrudate IS NULL))
    """
    existing = await database.fetch_one(query=query, values={
        "person_id": marital_status.person_id,
        "maritalstatustype_id": marital_status.maritalstatustype_id,
        "fromdate": marital_status.fromdate,
        "thrudate": marital_status.thrudate
    })
    if existing:
        logger.warning(f"Marital status already exists: person_id={marital_status.person_id}, type_id={marital_status.maritalstatustype_id}")
        return None

    query = """
        INSERT INTO maritalstatus (fromdate, thrudate, person_id, maritalstatustype_id)
        VALUES (:fromdate, :thrudate, :person_id, :maritalstatustype_id)
        RETURNING id, fromdate, thrudate, person_id, maritalstatustype_id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "fromdate": marital_status.fromdate,
            "thrudate": marital_status.thrudate,
            "person_id": marital_status.person_id,
            "maritalstatustype_id": marital_status.maritalstatustype_id
        })
        logger.info(f"Created marital status: id={result['id']}, person_id={result['person_id']}")
        return MaritalStatusOut(**result)
    except Exception as e:
        logger.error(f"Error creating marital status: {str(e)}")
        raise

async def get_marital_status(marital_status_id: int) -> Optional[MaritalStatusOut]:
    query = """
        SELECT id, fromdate, thrudate, person_id, maritalstatustype_id 
        FROM maritalstatus WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": marital_status_id})
    if not result:
        logger.warning(f"Marital status not found: id={marital_status_id}")
        return None
    logger.info(f"Retrieved marital status: id={result['id']}, person_id={result['person_id']}")
    return MaritalStatusOut(**result)

async def get_all_marital_statuses() -> List[MaritalStatusOut]:
    query = """
        SELECT id, fromdate, thrudate, person_id, maritalstatustype_id 
        FROM maritalstatus
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} marital statuses")
    return [MaritalStatusOut(**result) for result in results]

async def update_marital_status(marital_status_id: int, marital_status: MaritalStatusUpdate) -> Optional[MaritalStatusOut]:
    if any([marital_status.fromdate, marital_status.thrudate, marital_status.person_id, marital_status.maritalstatustype_id]):
        query = """
            SELECT id FROM maritalstatus 
            WHERE person_id = COALESCE(:person_id, person_id)
            AND maritalstatustype_id = COALESCE(:maritalstatustype_id, maritalstatustype_id)
            AND fromdate = COALESCE(:fromdate, fromdate)
            AND (thrudate = COALESCE(:thrudate, thrudate) OR (thrudate IS NULL AND :thrudate IS NULL))
            AND id != :id
        """
        existing = await database.fetch_one(query=query, values={
            "person_id": marital_status.person_id,
            "maritalstatustype_id": marital_status.maritalstatustype_id,
            "fromdate": marital_status.fromdate,
            "thrudate": marital_status.thrudate,
            "id": marital_status_id
        })
        if existing:
            logger.warning(f"Marital status already exists: person_id={marital_status.person_id}, type_id={marital_status.maritalstatustype_id}")
            return None

    query = """
        UPDATE maritalstatus
        SET fromdate = COALESCE(:fromdate, fromdate),
            thrudate = COALESCE(:thrudate, thrudate),
            person_id = COALESCE(:person_id, person_id),
            maritalstatustype_id = COALESCE(:maritalstatustype_id, maritalstatustype_id)
        WHERE id = :id
        RETURNING id, fromdate, thrudate, person_id, maritalstatustype_id
    """
    try:
        result = await database.fetch_one(query=query, values={
            "fromdate": marital_status.fromdate,
            "thrudate": marital_status.thrudate,
            "person_id": marital_status.person_id,
            "maritalstatustype_id": marital_status.maritalstatustype_id,
            "id": marital_status_id
        })
        if not result:
            logger.warning(f"Marital status not found for update: id={marital_status_id}")
            return None
        logger.info(f"Updated marital status: id={result['id']}, person_id={result['person_id']}")
        return MaritalStatusOut(**result)
    except Exception as e:
        logger.error(f"Error updating marital status: {str(e)}")
        raise

async def delete_marital_status(marital_status_id: int) -> bool:
    query = """
        DELETE FROM maritalstatus WHERE id = :id
        RETURNING id
    """
    result = await database.fetch_one(query=query, values={"id": marital_status_id})
    if not result:
        logger.warning(f"Marital status not found for deletion: id={marital_status_id}")
        return False
    logger.info(f"Deleted marital status: id={marital_status_id}")
    return True
```

### File: /app/controllers/marital_status.py
### Part: Controller - API endpoints for maritalstatus CRUD
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.marital_status import (
    create_marital_status, get_marital_status, get_all_marital_statuses,
    update_marital_status, delete_marital_status
)
from app.schemas.marital_status import MaritalStatusCreate, MaritalStatusUpdate, MaritalStatusOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/marital_status", tags=["marital_status"])

@router.post("/", response_model=MaritalStatusOut)
async def create_marital_status_endpoint(marital_status: MaritalStatusCreate, current_user: dict = Depends(get_current_user)):
    result = await create_marital_status(marital_status)
    if not result:
        logger.warning(f"Failed to create marital status: person_id={marital_status.person_id}")
        raise HTTPException(status_code=400, detail="Marital status already exists")
    logger.info(f"Created marital status: id={result.id}, person_id={result.person_id}")
    return result

@router.get("/{marital_status_id}", response_model=MaritalStatusOut)
async def get_marital_status_endpoint(marital_status_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_marital_status(marital_status_id)
    if not result:
        logger.warning(f"Marital status not found: id={marital_status_id}")
        raise HTTPException(status_code=404, detail="Marital status not found")
    logger.info(f"Retrieved marital status: id={result.id}, person_id={result.person_id}")
    return result

@router.get("/", response_model=List[MaritalStatusOut])
async def get_all_marital_statuses_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_marital_statuses()
    logger.info(f"Retrieved {len(results)} marital statuses")
    return results

@router.put("/{marital_status_id}", response_model=MaritalStatusOut)
async def update_marital_status_endpoint(marital_status_id: int, marital_status: MaritalStatusUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_marital_status(marital_status_id, marital_status)
    if not result:
        logger.warning(f"Failed to update marital status: id={marital_status_id}")
        raise HTTPException(status_code=404, detail="Marital status not found or already exists")
    logger.info(f"Updated marital status: id={result.id}, person_id={result.person_id}")
    return result

@router.delete("/{marital_status_id}")
async def delete_marital_status_endpoint(marital_status_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_marital_status(marital_status_id)
    if not result:
        logger.warning(f"Marital status not found for deletion: id={marital_status_id}")
        raise HTTPException(status_code=404, detail="Marital status not found")
    logger.info(f"Deleted marital status: id={marital_status_id}")
    return {"message": "Marital status deleted"}
```