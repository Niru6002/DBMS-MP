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
('Community Foundation', 'hello@commfound.org', '789 Community Rd', '555-0103', 'Foundation');
