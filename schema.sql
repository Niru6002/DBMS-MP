-- Grant Management System Database Schema
-- Drop existing tables if they exist
DROP TABLE IF EXISTS GRANTEE_UNIVS;
DROP TABLE IF EXISTS TOTAL_MILESTONE;
DROP TABLE IF EXISTS GRANT_TOPIC;
DROP TABLE IF EXISTS GRANTBENEFICIARY;
DROP TABLE IF EXISTS GRANT_TABLE;
DROP TABLE IF EXISTS GRANTEE;
DROP TABLE IF EXISTS TOPIC;
DROP TABLE IF EXISTS REGION;
DROP TABLE IF EXISTS DIVISION;

-- Create DIVISION table
CREATE TABLE DIVISION (
    division_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Create REGION table
CREATE TABLE REGION (
    region_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

-- Create TOPIC table
CREATE TABLE TOPIC (
    topic_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(100)
);

-- Create GRANTEE table
CREATE TABLE GRANTEE (
    grantee_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(100),
    addr VARCHAR(255),
    phone VARCHAR(20),
    grantee_type VARCHAR(50)
);

-- Create GRANT_TABLE (using GRANT_TABLE because GRANT is a reserved keyword)
CREATE TABLE GRANT_TABLE (
    grant_id INT PRIMARY KEY AUTO_INCREMENT,
    purpose TEXT,
    date_awarded DATE,
    duration INT,
    close_date DATE,
    start_date DATE,
    amount DECIMAL(15, 2),
    region_id INT,
    division_id INT,
    FOREIGN KEY (region_id) REFERENCES REGION(region_id) ON DELETE SET NULL,
    FOREIGN KEY (division_id) REFERENCES DIVISION(division_id) ON DELETE SET NULL
);

-- Create GRANTBENEFICIARY table
CREATE TABLE GRANTBENEFICIARY (
    beneficiary_id INT PRIMARY KEY AUTO_INCREMENT,
    grantee_id INT,
    institution VARCHAR(200),
    description TEXT,
    county_of_institute VARCHAR(100),
    FOREIGN KEY (grantee_id) REFERENCES GRANTEE(grantee_id) ON DELETE CASCADE
);

-- Create TOTAL_MILESTONE table
CREATE TABLE TOTAL_MILESTONE (
    milestone_id INT PRIMARY KEY AUTO_INCREMENT,
    grant_id INT,
    milestone_desc TEXT,
    due_date DATE,
    completion INT DEFAULT 0,
    FOREIGN KEY (grant_id) REFERENCES GRANT_TABLE(grant_id) ON DELETE CASCADE
);

-- Create GRANTEE_UNIVS junction table (many-to-many relationship between GRANTEE and GRANT)
CREATE TABLE GRANTEE_UNIVS (
    grantee_id INT,
    grant_id INT,
    associated_body VARCHAR(200),
    PRIMARY KEY (grantee_id, grant_id),
    FOREIGN KEY (grantee_id) REFERENCES GRANTEE(grantee_id) ON DELETE CASCADE,
    FOREIGN KEY (grant_id) REFERENCES GRANT_TABLE(grant_id) ON DELETE CASCADE
);

-- Create GRANT_TOPIC junction table (many-to-many relationship between GRANT and TOPIC)
CREATE TABLE GRANT_TOPIC (
    grant_id INT,
    topic_id INT,
    PRIMARY KEY (grant_id, topic_id),
    FOREIGN KEY (grant_id) REFERENCES GRANT_TABLE(grant_id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES TOPIC(topic_id) ON DELETE CASCADE
);

-- Insert sample data for DIVISION
INSERT INTO DIVISION (name, description) VALUES
('Research Division', 'Handles all research-related grants'),
('Education Division', 'Manages educational grants and programs'),
('Community Development', 'Focuses on community development initiatives');

-- Insert sample data for REGION
INSERT INTO REGION (name) VALUES
('North America'),
('Europe'),
('Asia Pacific'),
('Latin America');

-- Insert sample data for TOPIC
INSERT INTO TOPIC (name, category) VALUES
('STEM Education', 'Education'),
('Healthcare Research', 'Research'),
('Environmental Conservation', 'Environment'),
('Digital Literacy', 'Technology');

-- Insert sample data for GRANTEE
INSERT INTO GRANTEE (name, email, addr, phone, grantee_type) VALUES
('University of Science', 'contact@uos.edu', '123 University Ave', '555-0101', 'University'),
('Tech Institute', 'info@techinst.org', '456 Tech Street', '555-0102', 'Institute'),
('Community Foundation', 'hello@commfound.org', '789 Community Rd', '555-0103', 'Foundation'),
('Global Research Center', 'research@grc.edu', '321 Research Park', '555-0104', 'Institute'),
('Green Earth NGO', 'contact@greenearth.org', '555 Nature Way', '555-0105', 'NGO');

-- Insert sample data for GRANT_TABLE
INSERT INTO GRANT_TABLE (purpose, date_awarded, duration, close_date, start_date, amount, region_id, division_id) VALUES
('Advanced STEM Education Program for Underserved Communities', '2024-01-15', 24, '2026-01-15', '2024-02-01', 250000.00, 1, 2),
('Healthcare Innovation Research Initiative', '2024-03-20', 36, '2027-03-20', '2024-04-01', 500000.00, 2, 1),
('Environmental Conservation and Biodiversity Study', '2023-11-10', 18, '2025-05-10', '2023-12-01', 180000.00, 3, 1),
('Digital Literacy and Technology Access Program', '2024-05-05', 12, '2025-05-05', '2024-06-01', 120000.00, 1, 2),
('Community Health and Wellness Project', '2024-02-28', 24, '2026-02-28', '2024-03-15', 300000.00, 4, 3),
('Renewable Energy Research Grant', '2024-04-12', 30, '2026-10-12', '2024-05-01', 450000.00, 2, 1);

-- Insert sample data for GRANTBENEFICIARY
INSERT INTO GRANTBENEFICIARY (grantee_id, institution, description, county_of_institute) VALUES
(1, 'University of Science Main Campus', 'Primary research facility for STEM education programs', 'Kings County'),
(2, 'Tech Institute Downtown Branch', 'Technology training center for digital literacy programs', 'Queens County'),
(3, 'Community Foundation Health Center', 'Community health and wellness service provider', 'Bronx County'),
(4, 'Global Research Center Laboratory', 'Advanced research laboratory for environmental studies', 'Suffolk County'),
(5, 'Green Earth NGO Field Office', 'Field office for conservation projects', 'Nassau County');

-- Insert sample data for TOTAL_MILESTONE
INSERT INTO TOTAL_MILESTONE (grant_id, milestone_desc, due_date, completion) VALUES
(1, 'Complete curriculum development for STEM program', '2024-06-01', 100),
(1, 'Recruit and train 50 educators', '2024-09-01', 75),
(1, 'Launch pilot program in 5 schools', '2024-12-01', 50),
(2, 'Establish research partnerships with 3 hospitals', '2024-07-01', 100),
(2, 'Complete Phase 1 clinical trials', '2025-06-01', 60),
(2, 'Publish interim research findings', '2025-12-01', 30),
(3, 'Conduct initial biodiversity assessment', '2024-03-01', 100),
(3, 'Implement conservation measures in 10 sites', '2024-09-01', 80),
(3, 'Complete final environmental impact report', '2025-04-01', 40),
(4, 'Deploy technology infrastructure in 20 community centers', '2024-08-01', 90),
(4, 'Train 500 community members in digital skills', '2024-11-01', 70),
(5, 'Launch community health screening program', '2024-05-15', 85),
(5, 'Complete wellness workshops for 1000 participants', '2025-08-15', 45),
(6, 'Set up renewable energy research lab', '2024-08-01', 100),
(6, 'Complete feasibility study for 3 energy sources', '2025-11-01', 55);

-- Insert sample data for GRANTEE_UNIVS (Grantee-Grant Relationships)
INSERT INTO GRANTEE_UNIVS (grantee_id, grant_id, associated_body) VALUES
(1, 1, 'Department of Education'),
(2, 4, 'Technology Division'),
(3, 5, 'Health Services Department'),
(4, 2, 'Medical Research Board'),
(4, 6, 'Energy Research Council'),
(5, 3, 'Environmental Protection Agency'),
(1, 2, 'Science Research Department'),
(2, 1, 'Educational Technology Unit');

-- Insert sample data for GRANT_TOPIC (Grant-Topic Relationships)
INSERT INTO GRANT_TOPIC (grant_id, topic_id) VALUES
(1, 1),  -- STEM Education Program -> STEM Education
(2, 2),  -- Healthcare Innovation -> Healthcare Research
(3, 3),  -- Environmental Conservation -> Environmental Conservation
(4, 1),  -- Digital Literacy -> STEM Education
(4, 4),  -- Digital Literacy -> Digital Literacy
(5, 2),  -- Community Health -> Healthcare Research
(6, 3),  -- Renewable Energy -> Environmental Conservation
(1, 4);  -- STEM Education Program -> Digital Literacy
