-- Drop tables in reverse dependency order with CASCADE to handle foreign key constraints

-- Junction and leaf tables
DROP TABLE IF EXISTS communication_event_purpose CASCADE;
DROP TABLE IF EXISTS passport CASCADE;
DROP TABLE IF EXISTS maritalstatus CASCADE;
DROP TABLE IF EXISTS physicalcharacteristic CASCADE;
DROP TABLE IF EXISTS personname CASCADE;
DROP TABLE IF EXISTS citizenship CASCADE;
DROP TABLE IF EXISTS classify_by_eeoc CASCADE;
DROP TABLE IF EXISTS classify_by_income CASCADE;
DROP TABLE IF EXISTS classify_by_minority CASCADE;
DROP TABLE IF EXISTS classify_by_industry CASCADE;
DROP TABLE IF EXISTS classify_by_size CASCADE;
DROP TABLE IF EXISTS communication_event CASCADE;
DROP TABLE IF EXISTS party_relationship CASCADE;

-- Intermediate tables (including new subtype tables)
DROP TABLE IF EXISTS corporation CASCADE;
DROP TABLE IF EXISTS government_agency CASCADE;
DROP TABLE IF EXISTS team CASCADE;
DROP TABLE IF EXISTS family CASCADE;
DROP TABLE IF EXISTS other_informal_organization CASCADE;
DROP TABLE IF EXISTS person_classification CASCADE;
DROP TABLE IF EXISTS organization_classification CASCADE;
DROP TABLE IF EXISTS party_role CASCADE;
DROP TABLE IF EXISTS legal_organization CASCADE;
DROP TABLE IF EXISTS informal_organization CASCADE;
DROP TABLE IF EXISTS organization CASCADE;
DROP TABLE IF EXISTS person CASCADE;
DROP TABLE IF EXISTS party_classification CASCADE;

-- Lookup tables
DROP TABLE IF EXISTS communication_event_purpose_type CASCADE;
DROP TABLE IF EXISTS communication_event_status_type CASCADE;
DROP TABLE IF EXISTS contact_mechanism_type CASCADE;
DROP TABLE IF EXISTS party_relationship_status_type CASCADE;
DROP TABLE IF EXISTS priority_type CASCADE;
DROP TABLE IF EXISTS party_relationship_type CASCADE;
DROP TABLE IF EXISTS role_type CASCADE;
DROP TABLE IF EXISTS maritalstatustype CASCADE;
DROP TABLE IF EXISTS physicalcharacteristictype CASCADE;
DROP TABLE IF EXISTS personnametype CASCADE;
DROP TABLE IF EXISTS country CASCADE;
DROP TABLE IF EXISTS ethnicity CASCADE;
DROP TABLE IF EXISTS income_range CASCADE;
DROP TABLE IF EXISTS minority_type CASCADE;
DROP TABLE IF EXISTS industry_type CASCADE;
DROP TABLE IF EXISTS employee_count_range CASCADE;
DROP TABLE IF EXISTS gender_type CASCADE;

-- Root tables
DROP TABLE IF EXISTS party_type CASCADE;
DROP TABLE IF EXISTS party CASCADE;

-- Create tables in dependency order

-- Root tables
CREATE TABLE party (
    id SERIAL PRIMARY KEY              -- Unique identifier for each party
);

CREATE TABLE party_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for party types
    description VARCHAR(128)            -- Description of the party type (e.g., "Person", "Organization")
);

-- Lookup tables
CREATE TABLE communication_event_purpose_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for communication event purpose types
    description VARCHAR(128)            -- Description of the purpose type
);

CREATE TABLE communication_event_status_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for communication event status types
    description VARCHAR(128)            -- Description of the status type
);

CREATE TABLE contact_mechanism_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for contact mechanism types
    description VARCHAR(128)            -- Description of the contact mechanism type
);

CREATE TABLE party_relationship_status_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for relationship status types
    description VARCHAR(128)            -- Description of the status type
);

CREATE TABLE priority_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for priority types
    description VARCHAR(128)            -- Description of the priority type
);

CREATE TABLE party_relationship_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for relationship types
    description VARCHAR(128)            -- Description of the relationship type
);

CREATE TABLE role_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for role types
    description VARCHAR(128)            -- Description of the role type
);

CREATE TABLE maritalstatustype (
    id SERIAL PRIMARY KEY,              -- Unique identifier for marital status types
    description VARCHAR(128)            -- Description of the marital status
);

CREATE TABLE physicalcharacteristictype (
    id SERIAL PRIMARY KEY,              -- Unique identifier for physical characteristic types
    description VARCHAR(128)            -- Description of the characteristic
);

CREATE TABLE personnametype (
    id SERIAL PRIMARY KEY,              -- Unique identifier for name types
    description VARCHAR(128)            -- Description of the name type
);

CREATE TABLE country (
    id SERIAL PRIMARY KEY,              -- Unique identifier for countries
    isocode VARCHAR(2),                 -- ISO 3166-1 alpha-2 code (e.g., "US", "TH")
    name_en VARCHAR(128),               -- English name of the country
    name_th VARCHAR(128)                -- Thai name of the country
);

CREATE TABLE ethnicity (
    id SERIAL PRIMARY KEY,              -- Unique identifier for ethnicity
    name_en VARCHAR(128),               -- English name of the ethnicity
    name_th VARCHAR(128)                -- Thai name of the ethnicity
);

CREATE TABLE income_range (
    id SERIAL PRIMARY KEY,              -- Unique identifier for income ranges
    description VARCHAR(128)            -- Description of the income range
);

CREATE TABLE minority_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for minority types
    name_en VARCHAR(128),               -- English name of the minority type
    name_th VARCHAR(128)                -- Thai name of the minority type
);

CREATE TABLE industry_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for industry types
    naics_code VARCHAR(64),             -- NAICS code (e.g., "541511" for custom software development)
    description VARCHAR(128)            -- Description of the industry
);

CREATE TABLE employee_count_range (
    id SERIAL PRIMARY KEY,              -- Unique identifier for employee count ranges
    description VARCHAR(128)            -- Description of the range
);

CREATE TABLE gender_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for gender types
    description VARCHAR(128)            -- Description of the gender type (e.g., "Male", "Female", "Non-Binary")
);

-- Intermediate tables
CREATE TABLE party_classification (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each classification
    fromdate DATE,                      -- Start date of the classification
    thrudate DATE,                      -- End date of the classification (NULL if still active)
    party_id INT REFERENCES party(id) ON DELETE CASCADE,  -- Foreign key linking to the party
    party_type_id INT REFERENCES party_type(id) ON DELETE CASCADE -- Foreign key linking to the party type
);

CREATE TABLE person (
    id SERIAL PRIMARY KEY REFERENCES party(id) ON DELETE CASCADE, -- Links to the party table
    personal_id_number VARCHAR(64),           -- Personal ID number
    birthdate DATE,                             -- Date of birth
    mothermaidenname VARCHAR(128),              -- Mother's maiden name
    totalyearworkexperience INT,                -- Total years of work experience
    comment VARCHAR(128),                       -- Additional comments about the person
    gender_type_id INT REFERENCES gender_type(id) ON DELETE CASCADE -- Foreign key linking to gender type
);

CREATE TABLE organization (
    id SERIAL PRIMARY KEY REFERENCES party(id) ON DELETE CASCADE, -- Links to the party table
    name_en VARCHAR(128),                       -- English name of the organization
    name_th VARCHAR(128)                        -- Thai name of the organization
);

CREATE TABLE legal_organization (
    id SERIAL PRIMARY KEY REFERENCES organization(id) ON DELETE CASCADE, -- Links to organization
    federal_tax_id_number VARCHAR(64)                  -- Federal tax ID (e.g., EIN in the US)
);

CREATE TABLE corporation (
    id SERIAL PRIMARY KEY REFERENCES legal_organization(id) ON DELETE CASCADE -- Links to legal_organization
);

CREATE TABLE government_agency (
    id SERIAL PRIMARY KEY REFERENCES legal_organization(id) ON DELETE CASCADE -- Links to legal_organization
);

CREATE TABLE informal_organization (
    id SERIAL PRIMARY KEY REFERENCES organization(id) ON DELETE CASCADE -- Links to organization
);

CREATE TABLE team (
    id SERIAL PRIMARY KEY REFERENCES informal_organization(id) ON DELETE CASCADE -- Links to informal_organization
);

CREATE TABLE family (
    id SERIAL PRIMARY KEY REFERENCES informal_organization(id) ON DELETE CASCADE -- Links to informal_organization
);

CREATE TABLE other_informal_organization (
    id SERIAL PRIMARY KEY REFERENCES informal_organization(id) ON DELETE CASCADE -- Links to informal_organization
);

CREATE TABLE party_role (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each party-role association
    fromdate DATE,                      -- Start date of the role
    thrudate DATE,                      -- End date of the role (NULL if still active)
    party_id INT REFERENCES party(id) ON DELETE CASCADE, -- Foreign key linking to the party
    role_type_id INT REFERENCES role_type(id) ON DELETE CASCADE -- Foreign key linking to the role type
);

CREATE TABLE organization_classification (
    id SERIAL PRIMARY KEY REFERENCES party_classification(id) ON DELETE CASCADE -- Unique identifier for organization classifications
);

CREATE TABLE person_classification (
    id SERIAL PRIMARY KEY REFERENCES party_classification(id) ON DELETE CASCADE -- Links to party_classification
);

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

-- Leaf tables
CREATE TABLE communication_event (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each communication event
    datetime_start TIMESTAMP,           -- Start date and time of the communication event
    datetime_end TIMESTAMP,             -- End date and time of the communication event
    note VARCHAR(128),                 -- Additional notes about the event
    contact_mechanism_type_id INT REFERENCES contact_mechanism_type(id) ON DELETE CASCADE, -- Foreign key linking to contact mechanism type
    communication_event_status_type_id INT REFERENCES communication_event_status_type(id) ON DELETE CASCADE, -- Foreign key linking to status type
    party_relationship_id INT REFERENCES party_relationship(id) ON DELETE CASCADE -- Foreign key linking to party relationship
);

CREATE TABLE classify_by_size (
    id SERIAL PRIMARY KEY REFERENCES organization_classification(id) ON DELETE CASCADE, -- Links to organization_classification
    employee_count_range_id INT REFERENCES employee_count_range(id) ON DELETE CASCADE   -- Foreign key to employee_count_range
);

CREATE TABLE classify_by_industry (
    id SERIAL PRIMARY KEY REFERENCES organization_classification(id) ON DELETE CASCADE, -- Links to organization_classification
    industry_type_id INT REFERENCES industry_type(id) ON DELETE CASCADE                 -- Foreign key to industry_type
);

CREATE TABLE classify_by_minority (
    id SERIAL PRIMARY KEY REFERENCES organization_classification(id) ON DELETE CASCADE, -- Links to organization_classification
    minority_type_id INT REFERENCES minority_type(id) ON DELETE CASCADE                 -- Foreign key to minority_type
);

CREATE TABLE classify_by_income (
    id SERIAL PRIMARY KEY REFERENCES person_classification(id) ON DELETE CASCADE, -- Links to person_classification
    income_range_id INT REFERENCES income_range(id) ON DELETE CASCADE             -- Foreign key to income_range
);

CREATE TABLE classify_by_eeoc (
    id SERIAL PRIMARY KEY REFERENCES person_classification(id) ON DELETE CASCADE, -- Links to person_classification
    ethnicity_id INT REFERENCES ethnicity(id) ON DELETE CASCADE                   -- Foreign key to ethnicity
);

CREATE TABLE citizenship (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each citizenship record
    fromdate DATE,                      -- Start date of citizenship
    thrudate DATE,                      -- End date of citizenship (NULL if still active)
    person_id INT REFERENCES person(id) ON DELETE CASCADE, -- Foreign key linking to person
    country_id INT REFERENCES country(id) ON DELETE CASCADE -- Foreign key to country
);

CREATE TABLE personname (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each name record
    fromdate DATE,                      -- Start date of the name
    thrudate DATE,                      -- End date of the name (NULL if still active)
    person_id INT REFERENCES person(id) ON DELETE CASCADE, -- Foreign key linking to person
    personnametype_id INT REFERENCES personnametype(id) ON DELETE CASCADE, -- Foreign key to name type
    name VARCHAR(128)                   -- The name
);

CREATE TABLE physicalcharacteristic (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each characteristic record
    fromdate DATE,                      -- Start date of the characteristic
    thrudate DATE,                      -- End date of the characteristic (NULL if still active)
    val INT,                            -- Value of the characteristic
    person_id INT REFERENCES person(id) ON DELETE CASCADE, -- Foreign key linking to person
    physicalcharacteristictype_id INT REFERENCES physicalcharacteristictype(id) ON DELETE CASCADE -- Foreign key to characteristic type
);

CREATE TABLE maritalstatus (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each marital status record
    fromdate DATE,                      -- Start date of the marital status
    thrudate DATE,                      -- End date of the marital status (NULL if still active)
    person_id INT REFERENCES person(id) ON DELETE CASCADE, -- Foreign key linking to person
    maritalstatustype_id INT REFERENCES maritalstatustype(id) ON DELETE CASCADE -- Foreign key to marital status type
);

CREATE TABLE passport (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each passport
    passportnumber VARCHAR(64),         -- Passport number
    fromdate DATE,                      -- Issuance date of the passport
    thrudate DATE,                      -- Expiry date of the passport
    citizenship_id INT REFERENCES citizenship(id) ON DELETE CASCADE -- Foreign key linking to citizenship
);

CREATE TABLE communication_event_purpose (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each purpose association
    communication_event_id INT REFERENCES communication_event(id) ON DELETE CASCADE, -- Foreign key linking to communication event
    communication_event_purpose_type_id INT REFERENCES communication_event_purpose_type(id) ON DELETE CASCADE -- Foreign key linking to purpose type
);