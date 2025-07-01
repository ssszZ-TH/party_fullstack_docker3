I'll create the schema, model, and controller files for each of the specified tables. Each table will have CRUD operations with endpoints following the pattern `/v1/{table_name}`. The files will be structured similarly to your previous examples, with proper imports, logging, and error handling.

### 1. Role Type

```python
from pydantic import BaseModel
from typing import Optional

class RoleTypeCreate(BaseModel):
    description: str

class RoleTypeUpdate(BaseModel):
    description: Optional[str] = None

class RoleTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True
```

```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.role_type import RoleTypeCreate, RoleTypeUpdate, RoleTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_role_type(role_type: RoleTypeCreate) -> Optional[RoleTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO role_type (description)
                VALUES (:description)
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={"description": role_type.description})
            logger.info(f"Created role_type: id={result['id']}")
            return RoleTypeOut(**result)
        except Exception as e:
            logger.error(f"Error creating role_type: {str(e)}")
            raise

async def get_role_type(role_type_id: int) -> Optional[RoleTypeOut]:
    query = """
        SELECT id, description
        FROM role_type
        WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": role_type_id})
    if not result:
        logger.warning(f"Role_type not found: id={role_type_id}")
        return None
    logger.info(f"Retrieved role_type: id={result['id']}")
    return RoleTypeOut(**result)

async def get_all_role_types() -> List[RoleTypeOut]:
    query = """
        SELECT id, description
        FROM role_type
        ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} role_types")
    return [RoleTypeOut(**result) for result in results]

async def update_role_type(role_type_id: int, role_type: RoleTypeUpdate) -> Optional[RoleTypeOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE role_type
                SET description = COALESCE(:description, description)
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={
                "description": role_type.description,
                "id": role_type_id
            })
            if not result:
                logger.warning(f"Role_type not found for update: id={role_type_id}")
                return None
            logger.info(f"Updated role_type: id={role_type_id}")
            return RoleTypeOut(**result)
        except Exception as e:
            logger.error(f"Error updating role_type: {str(e)}")
            raise

async def delete_role_type(role_type_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM role_type
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": role_type_id})
            if not result:
                logger.warning(f"Role_type not found for deletion: id={role_type_id}")
                return False
            logger.info(f"Deleted role_type: id={role_type_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting role_type: {str(e)}")
            raise
```

```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.role_type import (
    create_role_type, get_role_type, get_all_role_types,
    update_role_type, delete_role_type
)
from app.schemas.role_type import RoleTypeCreate, RoleTypeUpdate, RoleTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/roletypes", tags=["roletypes"])

@router.post("/", response_model=RoleTypeOut)
async def create_role_type_endpoint(role_type: RoleTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_role_type(role_type)
    if not result:
        logger.warning(f"Failed to create role_type")
        raise HTTPException(status_code=400, detail="Failed to create role_type")
    logger.info(f"Created role_type: id={result.id}")
    return result

@router.get("/{role_type_id}", response_model=RoleTypeOut)
async def get_role_type_endpoint(role_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_role_type(role_type_id)
    if not result:
        logger.warning(f"Role_type not found: id={role_type_id}")
        raise HTTPException(status_code=404, detail="Role_type not found")
    logger.info(f"Retrieved role_type: id={result.id}")
    return result

@router.get("/", response_model=List[RoleTypeOut])
async def get_all_role_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_role_types()
    logger.info(f"Retrieved {len(results)} role_types")
    return results

@router.put("/{role_type_id}", response_model=RoleTypeOut)
async def update_role_type_endpoint(role_type_id: int, role_type: RoleTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_role_type(role_type_id, role_type)
    if not result:
        logger.warning(f"Role_type not found for update: id={role_type_id}")
        raise HTTPException(status_code=404, detail="Role_type not found")
    logger.info(f"Updated role_type: id={result.id}")
    return result

@router.delete("/{role_type_id}")
async def delete_role_type_endpoint(role_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_role_type(role_type_id)
    if not result:
        logger.warning(f"Role_type not found for deletion: id={role_type_id}")
        raise HTTPException(status_code=404, detail="Role_type not found")
    logger.info(f"Deleted role_type: id={role_type_id}")
    return {"message": "Role_type deleted"}
```

### 2. Party Relationship Type

```python
from pydantic import BaseModel
from typing import Optional

class PartyRelationshipTypeCreate(BaseModel):
    description: str

class PartyRelationshipTypeUpdate(BaseModel):
    description: Optional[str] = None

class PartyRelationshipTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True
```

```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.party_relationship_type import PartyRelationshipTypeCreate, PartyRelationshipTypeUpdate, PartyRelationshipTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_party_relationship_type(party_relationship_type: PartyRelationshipTypeCreate) -> Optional[PartyRelationshipTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO party_relationship_type (description)
                VALUES (:description)
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={"description": party_relationship_type.description})
            logger.info(f"Created party_relationship_type: id={result['id']}")
            return PartyRelationshipTypeOut(**result)
        except Exception as e:
            logger.error(f"Error creating party_relationship_type: {str(e)}")
            raise

async def get_party_relationship_type(party_relationship_type_id: int) -> Optional[PartyRelationshipTypeOut]:
    query = """
        SELECT id, description
        FROM party_relationship_type
        WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": party_relationship_type_id})
    if not result:
        logger.warning(f"Party_relationship_type not found: id={party_relationship_type_id}")
        return None
    logger.info(f"Retrieved party_relationship_type: id={result['id']}")
    return PartyRelationshipTypeOut(**result)

async def get_all_party_relationship_types() -> List[PartyRelationshipTypeOut]:
    query = """
        SELECT id, description
        FROM party_relationship_type
        ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} party_relationship_types")
    return [PartyRelationshipTypeOut(**result) for result in results]

async def update_party_relationship_type(party_relationship_type_id: int, party_relationship_type: PartyRelationshipTypeUpdate) -> Optional[PartyRelationshipTypeOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE party_relationship_type
                SET description = COALESCE(:description, description)
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={
                "description": party_relationship_type.description,
                "id": party_relationship_type_id
            })
            if not result:
                logger.warning(f"Party_relationship_type not found for update: id={party_relationship_type_id}")
                return None
            logger.info(f"Updated party_relationship_type: id={party_relationship_type_id}")
            return PartyRelationshipTypeOut(**result)
        except Exception as e:
            logger.error(f"Error updating party_relationship_type: {str(e)}")
            raise

async def delete_party_relationship_type(party_relationship_type_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM party_relationship_type
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": party_relationship_type_id})
            if not result:
                logger.warning(f"Party_relationship_type not found for deletion: id={party_relationship_type_id}")
                return False
            logger.info(f"Deleted party_relationship_type: id={party_relationship_type_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting party_relationship_type: {str(e)}")
            raise
```

```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.party_relationship_type import (
    create_party_relationship_type, get_party_relationship_type, get_all_party_relationship_types,
    update_party_relationship_type, delete_party_relationship_type
)
from app.schemas.party_relationship_type import PartyRelationshipTypeCreate, PartyRelationshipTypeUpdate, PartyRelationshipTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/partyrelationshiptypes", tags=["partyrelationshiptypes"])

@router.post("/", response_model=PartyRelationshipTypeOut)
async def create_party_relationship_type_endpoint(party_relationship_type: PartyRelationshipTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_party_relationship_type(party_relationship_type)
    if not result:
        logger.warning(f"Failed to create party_relationship_type")
        raise HTTPException(status_code=400, detail="Failed to create party_relationship_type")
    logger.info(f"Created party_relationship_type: id={result.id}")
    return result

@router.get("/{party_relationship_type_id}", response_model=PartyRelationshipTypeOut)
async def get_party_relationship_type_endpoint(party_relationship_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_party_relationship_type(party_relationship_type_id)
    if not result:
        logger.warning(f"Party_relationship_type not found: id={party_relationship_type_id}")
        raise HTTPException(status_code=404, detail="Party_relationship_type not found")
    logger.info(f"Retrieved party_relationship_type: id={result.id}")
    return result

@router.get("/", response_model=List[PartyRelationshipTypeOut])
async def get_all_party_relationship_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_party_relationship_types()
    logger.info(f"Retrieved {len(results)} party_relationship_types")
    return results

@router.put("/{party_relationship_type_id}", response_model=PartyRelationshipTypeOut)
async def update_party_relationship_type_endpoint(party_relationship_type_id: int, party_relationship_type: PartyRelationshipTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_party_relationship_type(party_relationship_type_id, party_relationship_type)
    if not result:
        logger.warning(f"Party_relationship_type not found for update: id={party_relationship_type_id}")
        raise HTTPException(status_code=404, detail="Party_relationship_type not found")
    logger.info(f"Updated party_relationship_type: id={result.id}")
    return result

@router.delete("/{party_relationship_type_id}")
async def delete_party_relationship_type_endpoint(party_relationship_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_party_relationship_type(party_relationship_type_id)
    if not result:
        logger.warning(f"Party_relationship_type not found for deletion: id={party_relationship_type_id}")
        raise HTTPException(status_code=404, detail="Party_relationship_type not found")
    logger.info(f"Deleted party_relationship_type: id={party_relationship_type_id}")
    return {"message": "Party_relationship_type deleted"}
```

### 3. Party Relationship Status Type

```python
from pydantic import BaseModel
from typing import Optional

class PartyRelationshipStatusTypeCreate(BaseModel):
    description: str

class PartyRelationshipStatusTypeUpdate(BaseModel):
    description: Optional[str] = None

class PartyRelationshipStatusTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True
```

```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.party_relationship_status_type import PartyRelationshipStatusTypeCreate, PartyRelationshipStatusTypeUpdate, PartyRelationshipStatusTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_party_relationship_status_type(party_relationship_status_type: PartyRelationshipStatusTypeCreate) -> Optional[PartyRelationshipStatusTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO party_relationship_status_type (description)
                VALUES (:description)
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={"description": party_relationship_status_type.description})
            logger.info(f"Created party_relationship_status_type: id={result['id']}")
            return PartyRelationshipStatusTypeOut(**result)
        except Exception as e:
            logger.error(f"Error creating party_relationship_status_type: {str(e)}")
            raise

async def get_party_relationship_status_type(party_relationship_status_type_id: int) -> Optional[PartyRelationshipStatusTypeOut]:
    query = """
        SELECT id, description
        FROM party_relationship_status_type
        WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": party_relationship_status_type_id})
    if not result:
        logger.warning(f"Party_relationship_status_type not found: id={party_relationship_status_type_id}")
        return None
    logger.info(f"Retrieved party_relationship_status_type: id={result['id']}")
    return PartyRelationshipStatusTypeOut(**result)

async def get_all_party_relationship_status_types() -> List[PartyRelationshipStatusTypeOut]:
    query = """
        SELECT id, description
        FROM party_relationship_status_type
        ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} party_relationship_status_types")
    return [PartyRelationshipStatusTypeOut(**result) for result in results]

async def update_party_relationship_status_type(party_relationship_status_type_id: int, party_relationship_status_type: PartyRelationshipStatusTypeUpdate) -> Optional[PartyRelationshipStatusTypeOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE party_relationship_status_type
                SET description = COALESCE(:description, description)
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={
                "description": party_relationship_status_type.description,
                "id": party_relationship_status_type_id
            })
            if not result:
                logger.warning(f"Party_relationship_status_type not found for update: id={party_relationship_status_type_id}")
                return None
            logger.info(f"Updated party_relationship_status_type: id={party_relationship_status_type_id}")
            return PartyRelationshipStatusTypeOut(**result)
        except Exception as e:
            logger.error(f"Error updating party_relationship_status_type: {str(e)}")
            raise

async def delete_party_relationship_status_type(party_relationship_status_type_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM party_relationship_status_type
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": party_relationship_status_type_id})
            if not result:
                logger.warning(f"Party_relationship_status_type not found for deletion: id={party_relationship_status_type_id}")
                return False
            logger.info(f"Deleted party_relationship_status_type: id={party_relationship_status_type_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting party_relationship_status_type: {str(e)}")
            raise
```

```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.party_relationship_status_type import (
    create_party_relationship_status_type, get_party_relationship_status_type, get_all_party_relationship_status_types,
    update_party_relationship_status_type, delete_party_relationship_status_type
)
from app.schemas.party_relationship_status_type import PartyRelationshipStatusTypeCreate, PartyRelationshipStatusTypeUpdate, PartyRelationshipStatusTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/partyrelationshipstatustypes", tags=["partyrelationshipstatustypes"])

@router.post("/", response_model=PartyRelationshipStatusTypeOut)
async def create_party_relationship_status_type_endpoint(party_relationship_status_type: PartyRelationshipStatusTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_party_relationship_status_type(party_relationship_status_type)
    if not result:
        logger.warning(f"Failed to create party_relationship_status_type")
        raise HTTPException(status_code=400, detail="Failed to create party_relationship_status_type")
    logger.info(f"Created party_relationship_status_type: id={result.id}")
    return result

@router.get("/{party_relationship_status_type_id}", response_model=PartyRelationshipStatusTypeOut)
async def get_party_relationship_status_type_endpoint(party_relationship_status_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_party_relationship_status_type(party_relationship_status_type_id)
    if not result:
        logger.warning(f"Party_relationship_status_type not found: id={party_relationship_status_type_id}")
        raise HTTPException(status_code=404, detail="Party_relationship_status_type not found")
    logger.info(f"Retrieved party_relationship_status_type: id={result.id}")
    return result

@router.get("/", response_model=List[PartyRelationshipStatusTypeOut])
async def get_all_party_relationship_status_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_party_relationship_status_types()
    logger.info(f"Retrieved {len(results)} party_relationship_status_types")
    return results

@router.put("/{party_relationship_status_type_id}", response_model=PartyRelationshipStatusTypeOut)
async def update_party_relationship_status_type_endpoint(party_relationship_status_type_id: int, party_relationship_status_type: PartyRelationshipStatusTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_party_relationship_status_type(party_relationship_status_type_id, party_relationship_status_type)
    if not result:
        logger.warning(f"Party_relationship_status_type not found for update: id={party_relationship_status_type_id}")
        raise HTTPException(status_code=404, detail="Party_relationship_status_type not found")
    logger.info(f"Updated party_relationship_status_type: id={result.id}")
    return result

@router.delete("/{party_relationship_status_type_id}")
async def delete_party_relationship_status_type_endpoint(party_relationship_status_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_party_relationship_status_type(party_relationship_status_type_id)
    if not result:
        logger.warning(f"Party_relationship_status_type not found for deletion: id={party_relationship_status_type_id}")
        raise HTTPException(status_code=404, detail="Party_relationship_status_type not found")
    logger.info(f"Deleted party_relationship_status_type: id={party_relationship_status_type_id}")
    return {"message": "Party_relationship_status_type deleted"}
```

### 4. Priority Type

```python
from pydantic import BaseModel
from typing import Optional

class PriorityTypeCreate(BaseModel):
    description: str

class PriorityTypeUpdate(BaseModel):
    description: Optional[str] = None

class PriorityTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True
```

```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.priority_type import PriorityTypeCreate, PriorityTypeUpdate, PriorityTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_priority_type(priority_type: PriorityTypeCreate) -> Optional[PriorityTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO priority_type (description)
                VALUES (:description)
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={"description": priority_type.description})
            logger.info(f"Created priority_type: id={result['id']}")
            return PriorityTypeOut(**result)
        except Exception as e:
            logger.error(f"Error creating priority_type: {str(e)}")
            raise

async def get_priority_type(priority_type_id: int) -> Optional[PriorityTypeOut]:
    query = """
        SELECT id, description
        FROM priority_type
        WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": priority_type_id})
    if not result:
        logger.warning(f"Priority_type not found: id={priority_type_id}")
        return None
    logger.info(f"Retrieved priority_type: id={result['id']}")
    return PriorityTypeOut(**result)

async def get_all_priority_types() -> List[PriorityTypeOut]:
    query = """
        SELECT id, description
        FROM priority_type
        ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} priority_types")
    return [PriorityTypeOut(**result) for result in results]

async def update_priority_type(priority_type_id: int, priority_type: PriorityTypeUpdate) -> Optional[PriorityTypeOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE priority_type
                SET description = COALESCE(:description, description)
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={
                "description": priority_type.description,
                "id": priority_type_id
            })
            if not result:
                logger.warning(f"Priority_type not found for update: id={priority_type_id}")
                return None
            logger.info(f"Updated priority_type: id={priority_type_id}")
            return PriorityTypeOut(**result)
        except Exception as e:
            logger.error(f"Error updating priority_type: {str(e)}")
            raise

async def delete_priority_type(priority_type_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM priority_type
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": priority_type_id})
            if not result:
                logger.warning(f"Priority_type not found for deletion: id={priority_type_id}")
                return False
            logger.info(f"Deleted priority_type: id={priority_type_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting priority_type: {str(e)}")
            raise
```

```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.priority_type import (
    create_priority_type, get_priority_type, get_all_priority_types,
    update_priority_type, delete_priority_type
)
from app.schemas.priority_type import PriorityTypeCreate, PriorityTypeUpdate, PriorityTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/prioritytypes", tags=["prioritytypes"])

@router.post("/", response_model=PriorityTypeOut)
async def create_priority_type_endpoint(priority_type: PriorityTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_priority_type(priority_type)
    if not result:
        logger.warning(f"Failed to create priority_type")
        raise HTTPException(status_code=400, detail="Failed to create priority_type")
    logger.info(f"Created priority_type: id={result.id}")
    return result

@router.get("/{priority_type_id}", response_model=PriorityTypeOut)
async def get_priority_type_endpoint(priority_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_priority_type(priority_type_id)
    if not result:
        logger.warning(f"Priority_type not found: id={priority_type_id}")
        raise HTTPException(status_code=404, detail="Priority_type not found")
    logger.info(f"Retrieved priority_type: id={result.id}")
    return result

@router.get("/", response_model=List[PriorityTypeOut])
async def get_all_priority_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_priority_types()
    logger.info(f"Retrieved {len(results)} priority_types")
    return results

@router.put("/{priority_type_id}", response_model=PriorityTypeOut)
async def update_priority_type_endpoint(priority_type_id: int, priority_type: PriorityTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_priority_type(priority_type_id, priority_type)
    if not result:
        logger.warning(f"Priority_type not found for update: id={priority_type_id}")
        raise HTTPException(status_code=404, detail="Priority_type not found")
    logger.info(f"Updated priority_type: id={result.id}")
    return result

@router.delete("/{priority_type_id}")
async def delete_priority_type_endpoint(priority_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_priority_type(priority_type_id)
    if not result:
        logger.warning(f"Priority_type not found for deletion: id={priority_type_id}")
        raise HTTPException(status_code=404, detail="Priority_type not found")
    logger.info(f"Deleted priority_type: id={priority_type_id}")
    return {"message": "Priority_type deleted"}
```

### 5. Communication Event Status Type

```python
from pydantic import BaseModel
from typing import Optional

class CommunicationEventStatusTypeCreate(BaseModel):
    description: str

class CommunicationEventStatusTypeUpdate(BaseModel):
    description: Optional[str] = None

class CommunicationEventStatusTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True
```

```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.communication_event_status_type import CommunicationEventStatusTypeCreate, CommunicationEventStatusTypeUpdate, CommunicationEventStatusTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_communication_event_status_type(communication_event_status_type: CommunicationEventStatusTypeCreate) -> Optional[CommunicationEventStatusTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO communication_event_status_type (description)
                VALUES (:description)
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={"description": communication_event_status_type.description})
            logger.info(f"Created communication_event_status_type: id={result['id']}")
            return CommunicationEventStatusTypeOut(**result)
        except Exception as e:
            logger.error(f"Error creating communication_event_status_type: {str(e)}")
            raise

async def get_communication_event_status_type(communication_event_status_type_id: int) -> Optional[CommunicationEventStatusTypeOut]:
    query = """
        SELECT id, description
        FROM communication_event_status_type
        WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": communication_event_status_type_id})
    if not result:
        logger.warning(f"Communication_event_status_type not found: id={communication_event_status_type_id}")
        return None
    logger.info(f"Retrieved communication_event_status_type: id={result['id']}")
    return CommunicationEventStatusTypeOut(**result)

async def get_all_communication_event_status_types() -> List[CommunicationEventStatusTypeOut]:
    query = """
        SELECT id, description
        FROM communication_event_status_type
        ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} communication_event_status_types")
    return [CommunicationEventStatusTypeOut(**result) for result in results]

async def update_communication_event_status_type(communication_event_status_type_id: int, communication_event_status_type: CommunicationEventStatusTypeUpdate) -> Optional[CommunicationEventStatusTypeOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE communication_event_status_type
                SET description = COALESCE(:description, description)
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={
                "description": communication_event_status_type.description,
                "id": communication_event_status_type_id
            })
            if not result:
                logger.warning(f"Communication_event_status_type not found for update: id={communication_event_status_type_id}")
                return None
            logger.info(f"Updated communication_event_status_type: id={communication_event_status_type_id}")
            return CommunicationEventStatusTypeOut(**result)
        except Exception as e:
            logger.error(f"Error updating communication_event_status_type: {str(e)}")
            raise

async def delete_communication_event_status_type(communication_event_status_type_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM communication_event_status_type
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": communication_event_status_type_id})
            if not result:
                logger.warning(f"Communication_event_status_type not found for deletion: id={communication_event_status_type_id}")
                return False
            logger.info(f"Deleted communication_event_status_type: id={communication_event_status_type_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting communication_event_status_type: {str(e)}")
            raise
```

```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.communication_event_status_type import (
    create_communication_event_status_type, get_communication_event_status_type, get_all_communication_event_status_types,
    update_communication_event_status_type, delete_communication_event_status_type
)
from app.schemas.communication_event_status_type import CommunicationEventStatusTypeCreate, CommunicationEventStatusTypeUpdate, CommunicationEventStatusTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/communicationeventstatustypes", tags=["communicationeventstatustypes"])

@router.post("/", response_model=CommunicationEventStatusTypeOut)
async def create_communication_event_status_type_endpoint(communication_event_status_type: CommunicationEventStatusTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_communication_event_status_type(communication_event_status_type)
    if not result:
        logger.warning(f"Failed to create communication_event_status_type")
        raise HTTPException(status_code=400, detail="Failed to create communication_event_status_type")
    logger.info(f"Created communication_event_status_type: id={result.id}")
    return result

@router.get("/{communication_event_status_type_id}", response_model=CommunicationEventStatusTypeOut)
async def get_communication_event_status_type_endpoint(communication_event_status_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_communication_event_status_type(communication_event_status_type_id)
    if not result:
        logger.warning(f"Communication_event_status_type not found: id={communication_event_status_type_id}")
        raise HTTPException(status_code=404, detail="Communication_event_status_type not found")
    logger.info(f"Retrieved communication_event_status_type: id={result.id}")
    return result

@router.get("/", response_model=List[CommunicationEventStatusTypeOut])
async def get_all_communication_event_status_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_communication_event_status_types()
    logger.info(f"Retrieved {len(results)} communication_event_status_types")
    return results

@router.put("/{communication_event_status_type_id}", response_model=CommunicationEventStatusTypeOut)
async def update_communication_event_status_type_endpoint(communication_event_status_type_id: int, communication_event_status_type: CommunicationEventStatusTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_communication_event_status_type(communication_event_status_type_id, communication_event_status_type)
    if not result:
        logger.warning(f"Communication_event_status_type not found for update: id={communication_event_status_type_id}")
        raise HTTPException(status_code=404, detail="Communication_event_status_type not found")
    logger.info(f"Updated communication_event_status_type: id={result.id}")
    return result

@router.delete("/{communication_event_status_type_id}")
async def delete_communication_event_status_type_endpoint(communication_event_status_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_communication_event_status_type(communication_event_status_type_id)
    if not result:
        logger.warning(f"Communication_event_status_type not found for deletion: id={communication_event_status_type_id}")
        raise HTTPException(status_code=404, detail="Communication_event_status_type not found")
    logger.info(f"Deleted communication_event_status_type: id={communication_event_status_type_id}")
    return {"message": "Communication_event_status_type deleted"}
```

### 6. Contact Mechanism Type

```python
from pydantic import BaseModel
from typing import Optional

class ContactMechanismTypeCreate(BaseModel):
    description: str

class ContactMechanismTypeUpdate(BaseModel):
    description: Optional[str] = None

class ContactMechanismTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True
```

```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.contact_mechanism_type import ContactMechanismTypeCreate, ContactMechanismTypeUpdate, ContactMechanismTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_contact_mechanism_type(contact_mechanism_type: ContactMechanismTypeCreate) -> Optional[ContactMechanismTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO contact_mechanism_type (description)
                VALUES (:description)
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={"description": contact_mechanism_type.description})
            logger.info(f"Created contact_mechanism_type: id={result['id']}")
            return ContactMechanismTypeOut(**result)
        except Exception as e:
            logger.error(f"Error creating contact_mechanism_type: {str(e)}")
            raise

async def get_contact_mechanism_type(contact_mechanism_type_id: int) -> Optional[ContactMechanismTypeOut]:
    query = """
        SELECT id, description
        FROM contact_mechanism_type
        WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": contact_mechanism_type_id})
    if not result:
        logger.warning(f"Contact_mechanism_type not found: id={contact_mechanism_type_id}")
        return None
    logger.info(f"Retrieved contact_mechanism_type: id={result['id']}")
    return ContactMechanismTypeOut(**result)

async def get_all_contact_mechanism_types() -> List[ContactMechanismTypeOut]:
    query = """
        SELECT id, description
        FROM contact_mechanism_type
        ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} contact_mechanism_types")
    return [ContactMechanismTypeOut(**result) for result in results]

async def update_contact_mechanism_type(contact_mechanism_type_id: int, contact_mechanism_type: ContactMechanismTypeUpdate) -> Optional[ContactMechanismTypeOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE contact_mechanism_type
                SET description = COALESCE(:description, description)
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={
                "description": contact_mechanism_type.description,
                "id": contact_mechanism_type_id
            })
            if not result:
                logger.warning(f"Contact_mechanism_type not found for update: id={contact_mechanism_type_id}")
                return None
            logger.info(f"Updated contact_mechanism_type: id={contact_mechanism_type_id}")
            return ContactMechanismTypeOut(**result)
        except Exception as e:
            logger.error(f"Error updating contact_mechanism_type: {str(e)}")
            raise

async def delete_contact_mechanism_type(contact_mechanism_type_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM contact_mechanism_type
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": contact_mechanism_type_id})
            if not result:
                logger.warning(f"Contact_mechanism_type not found for deletion: id={contact_mechanism_type_id}")
                return False
            logger.info(f"Deleted contact_mechanism_type: id={contact_mechanism_type_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting contact_mechanism_type: {str(e)}")
            raise
```

```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.contact_mechanism_type import (
    create_contact_mechanism_type, get_contact_mechanism_type, get_all_contact_mechanism_types,
    update_contact_mechanism_type, delete_contact_mechanism_type
)
from app.schemas.contact_mechanism_type import ContactMechanismTypeCreate, ContactMechanismTypeUpdate, ContactMechanismTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/contactmechanismtypes", tags=["contactmechanismtypes"])

@router.post("/", response_model=ContactMechanismTypeOut)
async def create_contact_mechanism_type_endpoint(contact_mechanism_type: ContactMechanismTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_contact_mechanism_type(contact_mechanism_type)
    if not result:
        logger.warning(f"Failed to create contact_mechanism_type")
        raise HTTPException(status_code=400, detail="Failed to create contact_mechanism_type")
    logger.info(f"Created contact_mechanism_type: id={result.id}")
    return result

@router.get("/{contact_mechanism_type_id}", response_model=ContactMechanismTypeOut)
async def get_contact_mechanism_type_endpoint(contact_mechanism_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_contact_mechanism_type(contact_mechanism_type_id)
    if not result:
        logger.warning(f"Contact_mechanism_type not found: id={contact_mechanism_type_id}")
        raise HTTPException(status_code=404, detail="Contact_mechanism_type not found")
    logger.info(f"Retrieved contact_mechanism_type: id={result.id}")
    return result

@router.get("/", response_model=List[ContactMechanismTypeOut])
async def get_all_contact_mechanism_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_contact_mechanism_types()
    logger.info(f"Retrieved {len(results)} contact_mechanism_types")
    return results

@router.put("/{contact_mechanism_type_id}", response_model=ContactMechanismTypeOut)
async def update_contact_mechanism_type_endpoint(contact_mechanism_type_id: int, contact_mechanism_type: ContactMechanismTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_contact_mechanism_type(contact_mechanism_type_id, contact_mechanism_type)
    if not result:
        logger.warning(f"Contact_mechanism_type not found for update: id={contact_mechanism_type_id}")
        raise HTTPException(status_code=404, detail="Contact_mechanism_type not found")
    logger.info(f"Updated contact_mechanism_type: id={result.id}")
    return result

@router.delete("/{contact_mechanism_type_id}")
async def delete_contact_mechanism_type_endpoint(contact_mechanism_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_contact_mechanism_type(contact_mechanism_type_id)
    if not result:
        logger.warning(f"Contact_mechanism_type not found for deletion: id={contact_mechanism_type_id}")
        raise HTTPException(status_code=404, detail="Contact_mechanism_type not found")
    logger.info(f"Deleted contact_mechanism_type: id={contact_mechanism_type_id}")
    return {"message": "Contact_mechanism_type deleted"}
```

### 7. Communication Event Purpose Type

```python
from pydantic import BaseModel
from typing import Optional

class CommunicationEventPurposeTypeCreate(BaseModel):
    description: str

class CommunicationEventPurposeTypeUpdate(BaseModel):
    description: Optional[str] = None

class CommunicationEventPurposeTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True
```

```python
from typing import Optional, List
from app.config.database import database
import logging
from app.schemas.communication_event_purpose_type import CommunicationEventPurposeTypeCreate, CommunicationEventPurposeTypeUpdate, CommunicationEventPurposeTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_communication_event_purpose_type(communication_event_purpose_type: CommunicationEventPurposeTypeCreate) -> Optional[CommunicationEventPurposeTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO communication_event_purpose_type (description)
                VALUES (:description)
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={"description": communication_event_purpose_type.description})
            logger.info(f"Created communication_event_purpose_type: id={result['id']}")
            return CommunicationEventPurposeTypeOut(**result)
        except Exception as e:
            logger.error(f"Error creating communication_event_purpose_type: {str(e)}")
            raise

async def get_communication_event_purpose_type(communication_event_purpose_type_id: int) -> Optional[CommunicationEventPurposeTypeOut]:
    query = """
        SELECT id, description
        FROM communication_event_purpose_type
        WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": communication_event_purpose_type_id})
    if not result:
        logger.warning(f"Communication_event_purpose_type not found: id={communication_event_purpose_type_id}")
        return None
    logger.info(f"Retrieved communication_event_purpose_type: id={result['id']}")
    return CommunicationEventPurposeTypeOut(**result)

async def get_all_communication_event_purpose_types() -> List[CommunicationEventPurposeTypeOut]:
    query = """
        SELECT id, description
        FROM communication_event_purpose_type
        ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} communication_event_purpose_types")
    return [CommunicationEventPurposeTypeOut(**result) for result in results]

async def update_communication_event_purpose_type(communication_event_purpose_type_id: int, communication_event_purpose_type: CommunicationEventPurposeTypeUpdate) -> Optional[CommunicationEventPurposeTypeOut]:
    async with database.transaction():
        try:
            query = """
                UPDATE communication_event_purpose_type
                SET description = COALESCE(:description, description)
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values={
                "description": communication_event_purpose_type.description,
                "id": communication_event_purpose_type_id
            })
            if not result:
                logger.warning(f"Communication_event_purpose_type not found for update: id={communication_event_purpose_type_id}")
                return None
            logger.info(f"Updated communication_event_purpose_type: id={communication_event_purpose_type_id}")
            return CommunicationEventPurposeTypeOut(**result)
        except Exception as e:
            logger.error(f"Error updating communication_event_purpose_type: {str(e)}")
            raise

async def delete_communication_event_purpose_type(communication_event_purpose_type_id: int) -> bool:
    async with database.transaction():
        try:
            query = """
                DELETE FROM communication_event_purpose_type
                WHERE id = :id
                RETURNING id
            """
            result = await database.fetch_one(query=query, values={"id": communication_event_purpose_type_id})
            if not result:
                logger.warning(f"Communication_event_purpose_type not found for deletion: id={communication_event_purpose_type_id}")
                return False
            logger.info(f"Deleted communication_event_purpose_type: id={communication_event_purpose_type_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting communication_event_purpose_type: {str(e)}")
            raise
```

```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.communication_event_purpose_type import (
    create_communication_event_purpose_type, get_communication_event_purpose_type, get_all_communication_event_purpose_types,
    update_communication_event_purpose_type, delete_communication_event_purpose_type
)
from app.schemas.communication_event_purpose_type import CommunicationEventPurposeTypeCreate, CommunicationEventPurposeTypeUpdate, CommunicationEventPurposeTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/communicationeventpurposetypes", tags=["communicationeventpurposetypes"])

@router.post("/", response_model=CommunicationEventPurposeTypeOut)
async def create_communication_event_purpose_type_endpoint(communication_event_purpose_type: CommunicationEventPurposeTypeCreate, current_user: dict = Depends(get_current_user)):
    result = await create_communication_event_purpose_type(communication_event_purpose_type)
    if not result:
        logger.warning(f"Failed to create communication_event_purpose_type")
        raise HTTPException(status_code=400, detail="Failed to create communication_event_purpose_type")
    logger.info(f"Created communication_event_purpose_type: id={result.id}")
    return result

@router.get("/{communication_event_purpose_type_id}", response_model=CommunicationEventPurposeTypeOut)
async def get_communication_event_purpose_type_endpoint(communication_event_purpose_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_communication_event_purpose_type(communication_event_purpose_type_id)
    if not result:
        logger.warning(f"Communication_event_purpose_type not found: id={communication_event_purpose_type_id}")
        raise HTTPException(status_code=404, detail="Communication_event_purpose_type not found")
    logger.info(f"Retrieved communication_event_purpose_type: id={result.id}")
    return result

@router.get("/", response_model=List[CommunicationEventPurposeTypeOut])
async def get_all_communication_event_purpose_types_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_communication_event_purpose_types()
    logger.info(f"Retrieved {len(results)} communication_event_purpose_types")
    return results

@router.put("/{communication_event_purpose_type_id}", response_model=CommunicationEventPurposeTypeOut)
async def update_communication_event_purpose_type_endpoint(communication_event_purpose_type_id: int, communication_event_purpose_type: CommunicationEventPurposeTypeUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_communication_event_purpose_type(communication_event_purpose_type_id, communication_event_purpose_type)
    if not result:
        logger.warning(f"Communication_event_purpose_type not found for update: id={communication_event_purpose_type_id}")
        raise HTTPException(status_code=404, detail="Communication_event_purpose_type not found")
    logger.info(f"Updated communication_event_purpose_type: id={result.id}")
    return result

@router.delete("/{communication_event_purpose_type_id}")
async def delete_communication_event_purpose_type_endpoint(communication_event_purpose_type_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_communication_event_purpose_type(communication_event_purpose_type_id)
    if not result:
        logger.warning(f"Communication_event_purpose_type not found for deletion: id={communication_event_purpose_type_id}")
        raise HTTPException(status_code=404, detail="Communication_event_purpose_type not found")
    logger.info(f"Deleted communication_event_purpose_type: id={communication_event_purpose_type_id}")
    return {"message": "Communication_event_purpose_type deleted"}
```