-- Super-type table to define different types of parties (e.g., person, organization)
CREATE TABLE party_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for party types
    description VARCHAR(128)            -- Description of the party type (e.g., "Person", "Organization")
);

-- Super-type table representing a generic party (could be a person or organization)
CREATE TABLE party (
    id SERIAL PRIMARY KEY              -- Unique identifier for each party
);

-- Junction table to classify a party into one or more types over time
CREATE TABLE party_classification (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each classification
    fromdate DATE,                      -- Start date of the classification
    thrudate DATE,                      -- End date of the classification (NULL if still active)
    party_id INT REFERENCES party(id),  -- Foreign key linking to the party
    party_type_id INT REFERENCES party_type(id) -- Foreign key linking to the party type
);

-- Super-type table for organization-specific classifications
CREATE TABLE organization_classification (
    id SERIAL PRIMARY KEY REFERENCES party_classification(id)               -- Unique identifier for organization classifications
);

-- Lookup table for minority types (e.g., "Women-Owned", "Veteran-Owned")
CREATE TABLE minority_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for minority types
    name_en VARCHAR(128),               -- English name of the minority type
    name_th VARCHAR(128)                -- Thai name of the minority type
);

-- Lookup table for industry types based on NAICS codes
CREATE TABLE industry_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for industry types
    naics_code VARCHAR(64),             -- NAICS code (e.g., "541511" for custom software development)
    description VARCHAR(128)            -- Description of the industry
);

-- Lookup table for employee count ranges (e.g., "1-10", "11-50")
CREATE TABLE employee_count_range (
    id SERIAL PRIMARY KEY,              -- Unique identifier for employee count ranges
    description VARCHAR(128)            -- Description of the range
);

-- Subtype of organization_classification: Classifies organizations by minority type
CREATE TABLE classify_by_minority (
    id SERIAL PRIMARY KEY REFERENCES organization_classification(id), -- Links to organization_classification
    minority_type_id INT REFERENCES minority_type(id)                 -- Foreign key to minority_type
);

-- Subtype of organization_classification: Classifies organizations by industry
CREATE TABLE classify_by_industry (
    id SERIAL PRIMARY KEY REFERENCES organization_classification(id), -- Links to organization_classification
    industry_type_id INT REFERENCES industry_type(id)                 -- Foreign key to industry_type
);

-- Subtype of organization_classification: Classifies organizations by size
CREATE TABLE classify_by_size (
    id SERIAL PRIMARY KEY REFERENCES organization_classification(id), -- Links to organization_classification
    employee_count_range_id INT REFERENCES employee_count_range(id)   -- Foreign key to employee_count_range
);

-- Subtype of party: Represents individuals
CREATE TABLE person (
    id SERIAL PRIMARY KEY REFERENCES party(id), -- Links to the party table
    socialsecuritynumber VARCHAR(64),           -- Social security number (or equivalent ID)
    birthdate DATE,                             -- Date of birth
    mothermaidenname VARCHAR(128),              -- Mother's maiden name
    totalyearworkexperience INT,                -- Total years of work experience
    comment VARCHAR(128)                        -- Additional comments about the person
);

-- Super-type table for person-specific classifications
CREATE TABLE person_classification (
    id SERIAL PRIMARY KEY REFERENCES party_classification(id) -- Links to organization_classification (seems incorrect; see note)
);

-- Lookup table for ethnicity (e.g., "Asian", "Caucasian")
CREATE TABLE ethnicity (
    id SERIAL PRIMARY KEY,              -- Unique identifier for ethnicity
    name_en VARCHAR(128),               -- English name of the ethnicity
    name_th VARCHAR(128)                -- Thai name of the ethnicity
);

-- Lookup table for income ranges (e.g., "$0-$50K", "$50K-$100K")
CREATE TABLE income_range (
    id SERIAL PRIMARY KEY,              -- Unique identifier for income ranges
    description VARCHAR(128)            -- Description of the income range
);

-- Subtype of person_classification: Classifies people by ethnicity
CREATE TABLE classify_by_eeoc (
    id SERIAL PRIMARY KEY REFERENCES person_classification(id), -- Links to person_classification
    ethnicity_id INT REFERENCES ethnicity(id)                   -- Foreign key to ethnicity
);

-- Subtype of person_classification: Classifies people by income
CREATE TABLE classify_by_income (
    id SERIAL PRIMARY KEY REFERENCES person_classification(id), -- Links to person_classification
    income_range_id INT REFERENCES income_range(id)             -- Foreign key to income_range
);

-- Lookup table for marital status types (e.g., "Single", "Married")
CREATE TABLE maritalstatustype (
    id SERIAL PRIMARY KEY,              -- Unique identifier for marital status types
    description VARCHAR(128)            -- Description of the marital status
);

-- Table to track a person's marital status over time
CREATE TABLE maritalstatus (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each marital status record
    fromdate DATE,                      -- Start date of the marital status
    thrudate DATE,                      -- End date of the marital status (NULL if still active)
    person_id INT REFERENCES person(id), -- Foreign key linking to person
    maritalstatustype_id INT REFERENCES maritalstatustype(id) -- Foreign key to marital status type
);

-- Lookup table for physical characteristic types (e.g., "Height", "Weight")
CREATE TABLE physicalcharacteristictype (
    id SERIAL PRIMARY KEY,              -- Unique identifier for physical characteristic types
    description VARCHAR(128)            -- Description of the characteristic
);

-- Table to track a person's physical characteristics over time
CREATE TABLE physicalcharacteristic (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each characteristic record
    fromdate DATE,                      -- Start date of the characteristic
    thrudate DATE,                      -- End date of the characteristic (NULL if still active)
    val INT,                      -- value of the characteristic
    person_id INT REFERENCES person(id), -- Foreign key linking to person
    physicalcharacteristictype_id INT REFERENCES physicalcharacteristictype(id) -- Foreign key to characteristic type
);

-- Lookup table for person name types (e.g., "Legal Name", "Nickname")
CREATE TABLE personnametype (
    id SERIAL PRIMARY KEY,              -- Unique identifier for name types
    description VARCHAR(128)            -- Description of the name type
);

-- Table to track a person's names over time
CREATE TABLE personname (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each name record
    fromdate DATE,                      -- Start date of the name
    thrudate DATE,                      -- End date of the name (NULL if still active)
    person_id INT REFERENCES person(id), -- Foreign key linking to person
    personnametype_id INT REFERENCES personnametype(id), -- Foreign key to name type
    name VARCHAR(128)                   -- The name
);

-- Lookup table for countries
CREATE TABLE country (
    id SERIAL PRIMARY KEY,              -- Unique identifier for countries
    isocode VARCHAR(2),                 -- ISO 3166-1 alpha-2 code (e.g., "US", "TH")
    name_en VARCHAR(128),               -- English name of the country
    name_th VARCHAR(128)                -- Thai name of the country
);

-- Table to track a person's citizenship over time
CREATE TABLE citizenship (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each citizenship record
    fromdate DATE,                      -- Start date of citizenship
    thrudate DATE,                      -- End date of citizenship (NULL if still active)
    person_id INT REFERENCES person(id), -- Foreign key linking to person
    country_id INT REFERENCES country(id) -- Foreign key to country
);

-- Table to track passports linked to citizenship
CREATE TABLE passport (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each passport
    passportnumber VARCHAR(64),         -- Passport number
    fromdate DATE,                      -- Issuance date of the passport
    thrudate DATE,                      -- Expiry date of the passport
    citizenship_id INT REFERENCES citizenship(id) -- Foreign key linking to citizenship
);

-- Subtype of party: Represents organizations
CREATE TABLE organization (
    id SERIAL PRIMARY KEY REFERENCES party(id), -- Links to the party table
    name_en VARCHAR(128),                       -- English name of the organization
    name_th VARCHAR(128)                        -- Thai name of the organization (Note: "varchat" was corrected to "varchar")
);

-- Subtype of organization: Represents legal organizations
CREATE TABLE legal_organization (
    id SERIAL PRIMARY KEY REFERENCES organization(id), -- Links to organization
    federal_tax_id_number VARCHAR(64)                  -- Federal tax ID (e.g., EIN in the US)
);

-- Subtype of organization: Represents informal organizations (e.g., clubs, groups)
CREATE TABLE informal_organization (
    id SERIAL PRIMARY KEY REFERENCES organization(id) -- Links to organization
);


------------------------------------------------------------------------------------------------------------------

-- Lookup table for role types (e.g., "Employee", "Customer", "Supplier")
CREATE TABLE role_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for role types
    description VARCHAR(128)            -- Description of the role type
);

-- Junction table to link a party to a role over time
CREATE TABLE party_role (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each party-role association
    fromdate DATE,                      -- Start date of the role
    thrudate DATE,                      -- End date of the role (NULL if still active)
    party_id INT REFERENCES party(id),  -- Foreign key linking to the party
    role_type_id INT REFERENCES role_type(id) -- Foreign key linking to the role type
);

-- Lookup table for party relationship types (e.g., "Parent-Child", "Employer-Employee")
CREATE TABLE party_relationship_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for relationship types
    description VARCHAR(128)            -- Description of the relationship type
);

-- Lookup table for priority types (e.g., "High", "Medium", "Low")
CREATE TABLE priority_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for priority types
    description VARCHAR(128)            -- Description of the priority type
);

-- Lookup table for party relationship status types (e.g., "Active", "Inactive")
CREATE TABLE party_relationship_status_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for relationship status types
    description VARCHAR(128)            -- Description of the status type
);

-- Table to represent relationships between two party roles
CREATE TABLE party_relationship (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each relationship
    from_date DATE,                     -- Start date of the relationship
    thru_date DATE,                     -- End date of the relationship (NULL if still active)
    comment VARCHAR(128),               -- Additional comments about the relationship
    from_party_role_id INT REFERENCES party_role(id), -- Foreign key linking to the "from" party role
    to_party_role_id INT REFERENCES party_role(id),   -- Foreign key linking to the "to" party role
    party_relationship_type_id INT REFERENCES party_relationship_type(id), -- Foreign key linking to relationship type
    priority_type_id INT REFERENCES priority_type(id), -- Foreign key linking to priority type
    party_relationship_status_type_id INT REFERENCES party_relationship_status_type(id) -- Foreign key linking to status type
);

-- Lookup table for contact mechanism types (e.g., "Email", "Phone", "Address")
CREATE TABLE contact_mechanism_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for contact mechanism types
    description VARCHAR(128)            -- Description of the contact mechanism type
);

-- Lookup table for communication event status types (e.g., "Scheduled", "Completed")
CREATE TABLE communication_event_status_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for communication event status types
    description VARCHAR(128)            -- Description of the status type
);

-- Table to represent communication events (e.g., emails, calls, meetings)
CREATE TABLE communication_event (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each communication event
    datetime_start TIMESTAMP,           -- Start date and time of the communication event
    datetime_end TIMESTAMP,             -- End date and time of the communication event
    note VARCHAR(128),                 -- Additional notes about the event
    contact_mechanism_type_id INT REFERENCES contact_mechanism_type(id), -- Foreign key linking to contact mechanism type
    communication_event_status_type_id INT REFERENCES communication_event_status_type(id) -- Foreign key linking to status type
    party_relationship_id INT REFERENCES party_relationship(id) -- Foreign key linking to party relationship
);

-- Lookup table for communication event purpose types (e.g., "Sales", "Support")
CREATE TABLE communication_event_purpose_type (
    id SERIAL PRIMARY KEY,              -- Unique identifier for communication event purpose types
    description VARCHAR(128)            -- Description of the purpose type
);

-- Junction table to link communication events to their purposes
CREATE TABLE communication_event_purpose (
    id SERIAL PRIMARY KEY,              -- Unique identifier for each purpose association
    communication_event_id INT REFERENCES communication_event(id), -- Foreign key linking to communication event
    communication_event_purpose_type_id INT REFERENCES communication_event_purpose_type(id) -- Foreign key linking to purpose type
);