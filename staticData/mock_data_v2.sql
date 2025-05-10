-- 1. Insert into independent tables (lookup tables and top-level supertypes)
INSERT INTO party_type (description) VALUES
('Person'),
('Organization'),
('Government Entity'),
('Non-Profit');

-- 2. Insert into party (supertype of person, organization)
INSERT INTO party (partytype_id) VALUES
(1), -- Person
(2), -- Organization
(2), -- Organization (expired later)
(3), -- Government Entity
(4); -- Non-Profit

-- 3. Insert into party_classification (depends on party and party_type)
INSERT INTO party_classification (fromdate, thrudate, party_id, party_type_id) VALUES
('2023-01-01', NULL, 1, 1), -- Person
('2023-01-01', NULL, 2, 2), -- Organization
('2022-06-01', '2023-05-31', 3, 2), -- Organization (expired)
('2024-01-01', NULL, 4, 3), -- Government Entity
('2023-03-01', NULL, 5, 4); -- Non-Profit

-- 4. Insert into organization_classification (supertype of classify_by_minority, classify_by_industry, classify_by_size)
INSERT INTO organization_classification (id) VALUES
(1), -- For classify_by_minority
(2), -- For classify_by_minority
(3), -- For classify_by_industry
(4), -- For classify_by_industry
(5); -- For classify_by_size

-- 5. Insert into lookup tables for organization_classification subtypes
INSERT INTO minority_type (name_en, name_th) VALUES
('Women-Owned', 'เป็นเจ้าของโดยผู้หญิง'),
('Veteran-Owned', 'เป็นเจ้าของโดยทหารผ่านศึก'),
('Minority-Owned', 'เป็นเจ้าของโดยชนกลุ่มน้อย'),
('Disabled-Owned', 'เป็นเจ้าของโดยผู้พิการ');

INSERT INTO industry_type (naics_code, description) VALUES
('541511', 'Custom Software Development'),
('722511', 'Full-Service Restaurants'),
('621111', 'Physician Offices'),
('111998', 'Organic Farming');

INSERT INTO employee_count_range (description) VALUES
('1-10'),
('11-50'),
('51-200'),
('201-1000');

-- 6. Insert into organization_classification subtypes (using ids from organization_classification)
INSERT INTO classify_by_minority (id, minority_type_id) VALUES
(1, 1), -- Women-Owned
(2, 2); -- Veteran-Owned

INSERT INTO classify_by_industry (id, industry_type_id) VALUES
(3, 1), -- Software Development
(4, 2); -- Restaurants

INSERT INTO classify_by_size (id, employee_count_range_id) VALUES
(5, 1); -- 1-10 employees

-- 7. Insert into person (subtype of party, using party ids 1 and 3)
INSERT INTO person (id, socialsecuritynumber, birthdate, mothermaidenname, totalyearworkexperience, comment) VALUES
(1, '123-45-6789', '1990-05-15', 'Smith', 10, 'Software Engineer'),
(3, '987-65-4321', '1985-09-22', 'Johnson', 15, 'Manager');

-- 8. Insert into person_classification (supertype of classify_by_eeoc, classify_by_income)
-- Note: This references organization_classification(id), which might be a design error; should be independent?
INSERT INTO person_classification (id) VALUES
(1), -- For classify_by_eeoc
(2); -- For classify_by_income

-- 9. Insert into lookup tables for person_classification
INSERT INTO ethnicity (name_en, name_th) VALUES
('Asian', 'เอเชีย'),
('Caucasian', 'คอเคเซียน'),
('Hispanic', 'ฮิสแปนิก'),
('African', 'แอฟริกัน');

INSERT INTO income_range (description) VALUES
('$0-$50K'),
('$50K-$100K'),
('$100K-$200K'),
('$200K+');

-- 10. Insert into person_classification subtypes (using ids from person_classification)
INSERT INTO classify_by_eeoc (id, ethnicity_id) VALUES
(1, 1); -- Asian

INSERT INTO classify_by_income (id, income_range_id) VALUES
(2, 2); -- $50K-$100K

-- 11. Insert into lookup tables for person-related data
INSERT INTO maritalstatustype (description) VALUES
('Single'),
('Married'),
('Divorced'),
('Widowed');

-- 12. Insert into maritalstatus (depends on person and maritalstatustype)
INSERT INTO maritalstatus (fromdate, thrudate, person_id, maritalstatustype_id) VALUES
('2015-01-01', NULL, 1, 2), -- Married
('2010-01-01', '2018-12-31', 3, 2); -- Married, then divorced

-- 13. Insert into physicalcharacteristictype (independent)
INSERT INTO physicalcharacteristictype (description) VALUES
('Height'),
('Weight'),
('Eye Color'),
('Hair Color');

-- 14. Insert into physicalcharacteristic (depends on person and physicalcharacteristictype)
INSERT INTO physicalcharacteristic (fromdate, thrudate, person_id, physicalcharacteristictype_id) VALUES
('2023-01-01', NULL, 1, 1), -- Height
('2023-01-01', NULL, 1, 2); -- Weight

-- 15. Insert into personnametype (independent)
INSERT INTO personnametype (description) VALUES
('Legal Name'),
('Nickname'),
('Maiden Name'),
('Professional Name');

-- 16. Insert into personname (depends on person and personnametype)
INSERT INTO personname (fromdate, thrudate, person_id, personnametype_id) VALUES
('1990-05-15', NULL, 1, 1), -- Legal Name
('2010-01-01', NULL, 1, 2); -- Nickname

-- 17. Insert into country (independent)
INSERT INTO country (isocode, name_en, name_th) VALUES
('US', 'United States', 'สหรัฐอเมริกา'),
('TH', 'Thailand', 'ประเทศไทย'),
('JP', 'Japan', 'ญี่ปุ่น'),
('UK', 'United Kingdom', 'สหราชอาณาจักร');

-- 18. Insert into citizenship (depends on person and country)
INSERT INTO citizenship (fromdate, thrudate, person_id, country_id) VALUES
('1990-05-15', NULL, 1, 2), -- Thai citizenship
('1985-09-22', NULL, 3, 1); -- US citizenship

-- 19. Insert into passport (depends on citizenship)
INSERT INTO passport (passportnumber, fromdate, thrudate, citizenship_id) VALUES
('TH1234567', '2020-01-01', '2030-01-01', 1),
('US9876543', '2019-06-01', '2029-06-01', 2);

-- 20. Insert into organization (subtype of party, using party ids 2, 4, 5)
INSERT INTO organization (id, name_en, name_th) VALUES
(2, 'TechCorp', 'เทคคอร์ป'),
(4, 'GovAgency', 'หน่วยงานรัฐ'),
(5, 'NonProfitOrg', 'องค์กรไม่แสวงผลกำไร');

-- 21. Insert into legal_organization (subtype of organization, using organization id 2)
INSERT INTO legal_organization (id, federal_tax_id_number) VALUES
(2, '12-3456789');

-- 22. Insert into informal_organization (subtype of organization, using organization id 5)
INSERT INTO informal_organization (id) VALUES
(5); -- Non-Profit from earlier