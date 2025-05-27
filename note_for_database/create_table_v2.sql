-- Drop and create table for party types with CASCADE
DROP TABLE IF EXISTS party_type;
CREATE TABLE party_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for party types
    description VARCHAR(128)            -- Description of the party type (e.g., "Person", "Organization")
);

-- Drop and create table for generic party
DROP TABLE IF EXISTS party;
CREATE TABLE party (
    id SERIAL PRIMARY KEY              -- Unique identifier for each party
);

-- Drop and create junction table for party classification
DROP TABLE IF EXISTS party_classification;
CREATE TABLE party_classification (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each classification
    fromdate DATE,                      -- Start date of the classification
    thrudate DATE,                      -- End date of the classification (NULL if still active)
    party_id INT REFERENCES party(id) ON DELETE CASCADE,  -- Foreign key linking to the party
    party_type_id INT REFERENCES party_type(id) ON DELETE CASCADE -- Foreign key linking to the party type
);

-- Drop and create table for organization-specific classifications
DROP TABLE IF EXISTS organization_classification;
CREATE TABLE organization_classification (
    id SERIAL PRIMARY KEY REFERENCES party_classification(id) ON DELETE CASCADE -- Unique identifier for organization classifications
);

-- Drop and create lookup table for minority types
DROP TABLE IF EXISTS minority_type;
CREATE TABLE minority_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for minority types
    name_en VARCHAR(128),               -- English name of the minority type
    name_th VARCHAR(128)                -- Thai name of the minority type
);

-- Drop and create lookup table for industry types
DROP TABLE IF EXISTS industry_type;
CREATE TABLE industry_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for industry types
    naics_code VARCHAR(64),             -- NAICS code (e.g., "541511" for custom software development)
    description VARCHAR(128)            -- Description of the industry
);

-- Drop and create lookup table for employee count ranges
DROP TABLE IF EXISTS employee_count_range;
CREATE TABLE employee_count_range (
    id SERIAL PRIMARY KEY,              -- Unique identifier for employee count ranges
    description VARCHAR(128)            -- Description of the range
);

-- Drop and create table to classify organizations by minority type
DROP TABLE IF EXISTS classify_by_minority;
CREATE TABLE classify_by_minority (
    id SERIAL PRIMARY KEY REFERENCES organization_classification(id) ON DELETE CASCADE, -- Links to organization_classification
    minority_type_id INT REFERENCES minority_type(id) ON DELETE CASCADE                 -- Foreign key to minority_type
);

-- Drop and create table to classify organizations by industry
DROP TABLE IF EXISTS classify_by_industry;
CREATE TABLE classify_by_industry (
    id SERIAL PRIMARY KEY REFERENCES organization_classification(id) ON DELETE CASCADE, -- Links to organization_classification
    industry_type_id INT REFERENCES industry_type(id) ON DELETE CASCADE                 -- Foreign key to industry_type
);

-- Drop and create table to classify organizations by size
DROP TABLE IF EXISTS classify_by_size;
CREATE TABLE classify_by_size (
    id SERIAL PRIMARY KEY REFERENCES organization_classification(id) ON DELETE CASCADE, -- Links to organization_classification
    employee_count_range_id INT REFERENCES employee_count_range(id) ON DELETE CASCADE   -- Foreign key to employee_count_range
);

-- Drop and create table for individuals
DROP TABLE IF EXISTS person;
CREATE TABLE person (
    id SERIAL PRIMARY KEY REFERENCES party(id) ON DELETE CASCADE, -- Links to the party table
    socialsecuritynumber VARCHAR(64),           -- Social security number (or equivalent ID)
    birthdate DATE,                             -- Date of birth
    mothermaidenname VARCHAR(128),              -- Mother's maiden name
    totalyearworkexperience INT,                -- Total years of work experience
    comment VARCHAR(128)                        -- Additional comments about the person
);

-- Drop and create table for person-specific classifications
DROP TABLE IF EXISTS person_classification;
CREATE TABLE person_classification (
    id SERIAL PRIMARY KEY REFERENCES party_classification(id) ON DELETE CASCADE -- Links to party_classification
);

-- Drop and create lookup table for ethnicity
DROP TABLE IF EXISTS ethnicity;
CREATE TABLE ethnicity (
    id SERIAL PRIMARY KEY,              -- Unique identifier for ethnicity
    name_en VARCHAR(128),               -- English name of the ethnicity
    name_th VARCHAR(128)                -- Thai name of the ethnicity
);

-- Drop and create lookup table for income ranges
DROP TABLE IF EXISTS income_range;
CREATE TABLE income_range (
    id SERIAL PRIMARY KEY,              -- Unique identifier for income ranges
    description VARCHAR(128)            -- Description of the income range
);

-- Drop and create table to classify people by ethnicity
DROP TABLE IF EXISTS classify_by_eeoc;
CREATE TABLE classify_by_eeoc (
    id SERIAL PRIMARY KEY REFERENCES person_classification(id) ON DELETE CASCADE, -- Links to person_classification
    ethnicity_id INT REFERENCES ethnicity(id) ON DELETE CASCADE                   -- Foreign key to ethnicity
);

-- Drop and create table to classify people by income
DROP TABLE IF EXISTS classify_by_income;
CREATE TABLE classify_by_income (
    id SERIAL PRIMARY KEY REFERENCES person_classification(id) ON DELETE CASCADE, -- Links to person_classification
    income_range_id INT REFERENCES income_range(id) ON DELETE CASCADE             -- Foreign key to income_range
);

-- Drop and create lookup table for marital status types
DROP TABLE IF EXISTS maritalstatustype;
CREATE TABLE maritalstatustype (
    id SERIAL PRIMARY KEY,              -- Unique identifier for marital status types
    description VARCHAR(128)            -- Description of the marital status
);

-- Drop and create table to track marital status
DROP TABLE IF EXISTS maritalstatus;
CREATE TABLE maritalstatus (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each marital status record
    fromdate DATE,                      -- Start date of the marital status
    thrudate DATE,                      -- End date of the marital status (NULL if still active)
    person_id INT REFERENCES person(id) ON DELETE CASCADE, -- Foreign key linking to person
    maritalstatustype_id INT REFERENCES maritalstatustype(id) ON DELETE CASCADE -- Foreign key to marital status type
);

-- Drop and create lookup table for physical characteristic types
DROP TABLE IF EXISTS physicalcharacteristictype;
CREATE TABLE physicalcharacteristictype (
    id SERIAL PRIMARY KEY,              -- Unique identifier for physical characteristic types
    description VARCHAR(128)            -- Description of the characteristic
);

-- Drop and create table to track physical characteristics
DROP TABLE IF EXISTS physicalcharacteristic;
CREATE TABLE physicalcharacteristic (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each characteristic record
    fromdate DATE,                      -- Start date of the characteristic
    thrudate DATE,                      -- End date of the characteristic (NULL if still active)
    val INT,                            -- Value of the characteristic
    person_id INT REFERENCES person(id) ON DELETE CASCADE, -- Foreign key linking to person
    physicalcharacteristictype_id INT REFERENCES physicalcharacteristictype(id) ON DELETE CASCADE -- Foreign key to characteristic type
);

-- Drop and create lookup table for person name types
DROP TABLE IF EXISTS personnametype;
CREATE TABLE personnametype (
    id SERIAL PRIMARY KEY,              -- Unique identifier for name types
    description VARCHAR(128)            -- Description of the name type
);

-- Drop and create table to track person names
DROP TABLE IF EXISTS personname;
CREATE TABLE personname (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each name record
    fromdate DATE,                      -- Start date of the name
    thrudate DATE,                      -- End date of the name (NULL if still active)
    person_id INT REFERENCES person(id) ON DELETE CASCADE, -- Foreign key linking to person
    personnametype_id INT REFERENCES personnametype(id) ON DELETE CASCADE, -- Foreign key to name type
    name VARCHAR(128)                   -- The name
);

-- Drop and create lookup table for countries
DROP TABLE IF EXISTS country;
CREATE TABLE country (
    id SERIAL PRIMARY KEY,              -- Unique identifier for countries
    isocode VARCHAR(2),                 -- ISO 3166-1 alpha-2 code (e.g., "US", "TH")
    name_en VARCHAR(128),               -- English name of the country
    name_th VARCHAR(128)                -- Thai name of the country
);

-- Drop and create table to track citizenship
DROP TABLE IF EXISTS citizenship;
CREATE TABLE citizenship (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each citizenship record
    fromdate DATE,                      -- Start date of citizenship
    thrudate DATE,                      -- End date of citizenship (NULL if still active)
    person_id INT REFERENCES person(id) ON DELETE CASCADE, -- Foreign key linking to person
    country_id INT REFERENCES country(id) ON DELETE CASCADE -- Foreign key to country
);

-- Drop and create table to track passports
DROP TABLE IF EXISTS passport;
CREATE TABLE passport (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each passport
    passportnumber VARCHAR(64),         -- Passport number
    fromdate DATE,                      -- Issuance date of the passport
    thrudate DATE,                      -- Expiry date of the passport
    citizenship_id INT REFERENCES citizenship(id) ON DELETE CASCADE -- Foreign key linking to citizenship
);

-- Drop and create table for organizations
DROP TABLE IF EXISTS organization;
CREATE TABLE organization (
    id SERIAL PRIMARY KEY REFERENCES party(id) ON DELETE CASCADE, -- Links to the party table
    name_en VARCHAR(128),                       -- English name of the organization
    name_th VARCHAR(128)                        -- Thai name of the organization
);

-- Drop and create table for legal organizations
DROP TABLE IF EXISTS legal_organization;
CREATE TABLE legal_organization (
    id SERIAL PRIMARY KEY REFERENCES organization(id) ON DELETE CASCADE, -- Links to organization
    federal_tax_id_number VARCHAR(64)                  -- Federal tax ID (e.g., EIN in the US)
);

-- Drop and create table for informal organizations
DROP TABLE IF EXISTS informal_organization;
CREATE TABLE informal_organization (
    id SERIAL PRIMARY KEY REFERENCES organization(id) ON DELETE CASCADE -- Links to organization
);

-------------------------------------------- เส้นเเบ่ง --------------------------------------------
-- layer 3


-- Drop and create lookup table for role types
DROP TABLE IF EXISTS role_type;
CREATE TABLE role_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for role types
    description VARCHAR(128)            -- Description of the role type
);

-- Drop and create junction table for party roles
DROP TABLE IF EXISTS party_role;
CREATE TABLE party_role (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each party-role association
    fromdate DATE,                      -- Start date of the role
    thrudate DATE,                      -- End date of the role (NULL if still active)
    party_id INT REFERENCES party(id) ON DELETE CASCADE, -- Foreign key linking to the party
    role_type_id INT REFERENCES role_type(id) ON DELETE CASCADE -- Foreign key linking to the role type
);

-- Drop and create lookup table for party relationship types
DROP TABLE IF EXISTS party_relationship_type;
CREATE TABLE party_relationship_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for relationship types
    description VARCHAR(128)            -- Description of the relationship type
);

-- Drop and create lookup table for priority types
DROP TABLE IF EXISTS priority_type;
CREATE TABLE priority_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for priority types
    description VARCHAR(128)            -- Description of the priority type
);

-- Drop and create lookup table for party relationship status types
DROP TABLE IF EXISTS party_relationship_status_type;
CREATE TABLE party_relationship_status_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for relationship status types
    description VARCHAR(128)            -- Description of the status type
);

-- Drop and create table for party relationships
DROP TABLE IF EXISTS party_relationship;
CREATE TABLE party_relationship (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each relationship
    from_date DATE,                     -- Start date of the relationship
    thru_date DATE,                     -- End date of the relationship (NULL if still active)
    comment VARCHAR(128),               -- Additional comments about the relationship
    from_party_role_id INT REFERENCES party_role(id) ON DELETE CASCADE, -- Foreign key linking to the "from" party role
    to_party_role_id INT REFERENCES party_role(id) ON DELETE CASCADE,   -- Foreign key linking to the "to" party role
    party_relationship_type_id INT REFERENCES party_relationship_type(id) ON DELETE CASCADE, -- Foreign key linking to relationship type
    priority_type_id INT REFERENCES priority_type(id) ON DELETE CASCADE, -- Foreign key linking to priority type
    party_relationship_status_type_id INT REFERENCES party_relationship_status_type(id) ON DELETE CASCADE -- Foreign key linking to status type
);

-- Drop and create lookup table for contact mechanism types
DROP TABLE IF EXISTS contact_mechanism_type;
CREATE TABLE contact_mechanism_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for contact mechanism types
    description VARCHAR(128)            -- Description of the contact mechanism type
);

-- Drop and create lookup table for communication event status types
DROP TABLE IF EXISTS communication_event_status_type;
CREATE TABLE communication_event_status_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for communication event status types
    description VARCHAR(128)            -- Description of the status type
);

-- Drop and create table for communication events
DROP TABLE IF EXISTS communication_event;
CREATE TABLE communication_event (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each communication event
    datetime_start TIMESTAMP,           -- Start date and time of the communication event
    datetime_end TIMESTAMP,             -- End date and time of the communication event
    note VARCHAR(128),                 -- Additional notes about the event
    contact_mechanism_type_id INT REFERENCES contact_mechanism_type(id) ON DELETE CASCADE, -- Foreign key linking to contact mechanism type
    communication_event_status_type_id INT REFERENCES communication_event_status_type(id) ON DELETE CASCADE, -- Foreign key linking to status type
    party_relationship_id INT REFERENCES party_relationship(id) ON DELETE CASCADE -- Foreign key linking to party relationship
);

-- Drop and create lookup table for communication event purpose types
DROP TABLE IF EXISTS communication_event_purpose_type;
CREATE TABLE communication_event_purpose_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for communication event purpose types
    description VARCHAR(128)            -- Description of the purpose type
);

-- Drop and create junction table for communication event purposes
DROP TABLE IF EXISTS communication_event_purpose;
CREATE TABLE communication_event_purpose (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each purpose association
    communication_event_id INT REFERENCES communication_event(id) ON DELETE CASCADE, -- Foreign key linking to communication event
    communication_event_purpose_type_id INT REFERENCES communication_event_purpose_type(id) ON DELETE CASCADE -- Foreign key linking to purpose type
);