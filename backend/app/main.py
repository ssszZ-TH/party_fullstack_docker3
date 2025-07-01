from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import database
from app.controllers.auth.auth import router as auth_router
from app.controllers.citizenship import router as citizenship_router
from app.controllers.classify_by_eeoc import router as classify_by_eeoc_router
from app.controllers.classify_by_income import router as classify_by_income_router
from app.controllers.classify_by_industry import router as classify_by_industry_router
from app.controllers.classify_by_minority import router as classify_by_minority_router
from app.controllers.classify_by_size import router as classify_by_size_router
from app.controllers.corporation import router as corporation_router
from app.controllers.country import router as country_router
from app.controllers.employee_count_range import router as employee_count_range_router
from app.controllers.ethnicity import router as ethnicity_router
from app.controllers.family import router as family_router
from app.controllers.gender_type import router as gender_type_router
from app.controllers.government_agency import router as government_agency_router
from app.controllers.income_range import router as income_range_router
from app.controllers.industry_type import router as industry_type_router
from app.controllers.informal_organization import router as informal_organization_router
from app.controllers.legal_organization import router as legal_organization_router
from app.controllers.marital_status import router as marital_status_router
from app.controllers.marital_status_type import router as marital_status_type_router
from app.controllers.minority_type import router as minority_type_router
from app.controllers.other_informal_organization import router as other_informal_organization_router
from app.controllers.party_type import router as party_type_router
from app.controllers.passport import router as passport_router
from app.controllers.person import router as person_router
from app.controllers.person_name import router as person_name_router
from app.controllers.person_name_type import router as person_name_type_router
from app.controllers.physical_characteristic import router as physical_characteristic_router
from app.controllers.physical_characteristic_type import router as physical_characteristic_type_router
from app.controllers.team import router as team_router
from app.controllers.users.user import router as user_router
from app.controllers.role_type import router as role_type_router
from app.controllers.party_relationship_type import router as party_relationship_type_router
from app.controllers.party_relationship_status_type import router as party_relationship_status_type_router
from app.controllers.priority_type import router as priority_type_router
from app.controllers.communication_event_status_type import router as communication_event_status_type_router
from app.controllers.contact_mechanism_type import router as contact_mechanism_type_router
from app.controllers.communication_event_purpose_type import router as communication_event_purpose_type_router

# โหลด .env ก่อน import อื่นๆ
load_dotenv()

app = FastAPI()

# CORS สำหรับ frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# รวม routers
app.include_router(auth_router)
app.include_router(citizenship_router)
app.include_router(classify_by_eeoc_router)
app.include_router(classify_by_income_router)
app.include_router(classify_by_industry_router)
app.include_router(classify_by_minority_router)
app.include_router(classify_by_size_router)
app.include_router(corporation_router)
app.include_router(country_router)
app.include_router(employee_count_range_router)
app.include_router(ethnicity_router)
app.include_router(family_router)
app.include_router(gender_type_router)
app.include_router(government_agency_router)
app.include_router(income_range_router)
app.include_router(industry_type_router)
app.include_router(informal_organization_router)
app.include_router(legal_organization_router)
app.include_router(marital_status_router)
app.include_router(marital_status_type_router)
app.include_router(minority_type_router)
app.include_router(other_informal_organization_router)
app.include_router(party_type_router)
app.include_router(passport_router)
app.include_router(person_router)
app.include_router(person_name_router)
app.include_router(person_name_type_router)
app.include_router(physical_characteristic_router)
app.include_router(physical_characteristic_type_router)
app.include_router(team_router)
app.include_router(user_router)
app.include_router(role_type_router)
app.include_router(party_relationship_type_router)
app.include_router(party_relationship_status_type_router)
app.include_router(priority_type_router)
app.include_router(communication_event_status_type_router)
app.include_router(contact_mechanism_type_router)
app.include_router(communication_event_purpose_type_router)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return {"message": "FastAPI Backend","github":"https://github.com/ssszZ-TH/party_fullstack_docker3"}