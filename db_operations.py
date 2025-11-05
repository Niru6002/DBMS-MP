import mysql.connector
from mysql.connector import Error
import pandas as pd
from typing import List, Dict, Optional, Tuple
from datetime import datetime

class DatabaseConnection:
    """Handle MySQL database connection and operations"""
    
    def __init__(self, host='localhost', user='root', password='', database='grant_management'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                return True, "Connected to MySQL database"
        except Error as e:
            return False, f"Error: {str(e)}"
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query: str, params: tuple = None) -> Tuple[bool, str]:
        """Execute INSERT, UPDATE, DELETE queries"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            cursor.close()
            return True, "Query executed successfully"
        except Error as e:
            return False, f"Error: {str(e)}"
    
    def fetch_query(self, query: str, params: tuple = None) -> Tuple[bool, any]:
        """Execute SELECT queries and return results"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return True, result
        except Error as e:
            return False, f"Error: {str(e)}"
    
    def create_database(self) -> Tuple[bool, str]:
        """Create the database if it doesn't exist"""
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.close()
            conn.close()
            return True, f"Database {self.database} created/verified"
        except Error as e:
            return False, f"Error: {str(e)}"
    
    def initialize_schema(self, schema_file: str = 'schema.sql') -> Tuple[bool, str]:
        """Execute schema.sql file to create tables"""
        try:
            with open(schema_file, 'r') as file:
                sql_script = file.read()
            
            # Split by semicolons and execute each statement
            statements = sql_script.split(';')
            cursor = self.connection.cursor()
            
            for statement in statements:
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)
            
            self.connection.commit()
            cursor.close()
            return True, "Schema initialized successfully"
        except Error as e:
            return False, f"Error: {str(e)}"
        except FileNotFoundError:
            return False, "schema.sql file not found"

# ==================== DIVISION OPERATIONS ====================
class DivisionOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, name: str, description: str = None) -> Tuple[bool, str]:
        query = "INSERT INTO DIVISION (name, description) VALUES (%s, %s)"
        return self.db.execute_query(query, (name, description))
    
    def read_all(self) -> pd.DataFrame:
        success, result = self.db.fetch_query("SELECT * FROM DIVISION")
        return pd.DataFrame(result) if success else pd.DataFrame()
    
    def read_by_id(self, division_id: int) -> Dict:
        success, result = self.db.fetch_query(
            "SELECT * FROM DIVISION WHERE division_id = %s", (division_id,)
        )
        return result[0] if success and result else {}
    
    def update(self, division_id: int, name: str, description: str = None) -> Tuple[bool, str]:
        query = "UPDATE DIVISION SET name = %s, description = %s WHERE division_id = %s"
        return self.db.execute_query(query, (name, description, division_id))
    
    def delete(self, division_id: int) -> Tuple[bool, str]:
        query = "DELETE FROM DIVISION WHERE division_id = %s"
        return self.db.execute_query(query, (division_id,))

# ==================== REGION OPERATIONS ====================
class RegionOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, name: str) -> Tuple[bool, str]:
        query = "INSERT INTO REGION (name) VALUES (%s)"
        return self.db.execute_query(query, (name,))
    
    def read_all(self) -> pd.DataFrame:
        success, result = self.db.fetch_query("SELECT * FROM REGION")
        return pd.DataFrame(result) if success else pd.DataFrame()
    
    def read_by_id(self, region_id: int) -> Dict:
        success, result = self.db.fetch_query(
            "SELECT * FROM REGION WHERE region_id = %s", (region_id,)
        )
        return result[0] if success and result else {}
    
    def update(self, region_id: int, name: str) -> Tuple[bool, str]:
        query = "UPDATE REGION SET name = %s WHERE region_id = %s"
        return self.db.execute_query(query, (name, region_id))
    
    def delete(self, region_id: int) -> Tuple[bool, str]:
        query = "DELETE FROM REGION WHERE region_id = %s"
        return self.db.execute_query(query, (region_id,))

# ==================== TOPIC OPERATIONS ====================
class TopicOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, name: str, category: str = None) -> Tuple[bool, str]:
        query = "INSERT INTO TOPIC (name, category) VALUES (%s, %s)"
        return self.db.execute_query(query, (name, category))
    
    def read_all(self) -> pd.DataFrame:
        success, result = self.db.fetch_query("SELECT * FROM TOPIC")
        return pd.DataFrame(result) if success else pd.DataFrame()
    
    def read_by_id(self, topic_id: int) -> Dict:
        success, result = self.db.fetch_query(
            "SELECT * FROM TOPIC WHERE topic_id = %s", (topic_id,)
        )
        return result[0] if success and result else {}
    
    def update(self, topic_id: int, name: str, category: str = None) -> Tuple[bool, str]:
        query = "UPDATE TOPIC SET name = %s, category = %s WHERE topic_id = %s"
        return self.db.execute_query(query, (name, category, topic_id))
    
    def delete(self, topic_id: int) -> Tuple[bool, str]:
        query = "DELETE FROM TOPIC WHERE topic_id = %s"
        return self.db.execute_query(query, (topic_id,))

# ==================== GRANTEE OPERATIONS ====================
class GranteeOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, name: str, email: str = None, addr: str = None, 
               phone: str = None, grantee_type: str = None) -> Tuple[bool, str]:
        query = "INSERT INTO GRANTEE (name, email, addr, phone, grantee_type) VALUES (%s, %s, %s, %s, %s)"
        return self.db.execute_query(query, (name, email, addr, phone, grantee_type))
    
    def read_all(self) -> pd.DataFrame:
        success, result = self.db.fetch_query("SELECT * FROM GRANTEE")
        return pd.DataFrame(result) if success else pd.DataFrame()
    
    def read_by_id(self, grantee_id: int) -> Dict:
        success, result = self.db.fetch_query(
            "SELECT * FROM GRANTEE WHERE grantee_id = %s", (grantee_id,)
        )
        return result[0] if success and result else {}
    
    def update(self, grantee_id: int, name: str, email: str = None, 
               addr: str = None, phone: str = None, grantee_type: str = None) -> Tuple[bool, str]:
        query = """UPDATE GRANTEE SET name = %s, email = %s, addr = %s, 
                   phone = %s, grantee_type = %s WHERE grantee_id = %s"""
        return self.db.execute_query(query, (name, email, addr, phone, grantee_type, grantee_id))
    
    def delete(self, grantee_id: int) -> Tuple[bool, str]:
        query = "DELETE FROM GRANTEE WHERE grantee_id = %s"
        return self.db.execute_query(query, (grantee_id,))

# ==================== GRANT OPERATIONS ====================
class GrantOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, purpose: str, date_awarded, duration: int, 
               close_date, start_date, amount: float, 
               region_id: int = None, division_id: int = None) -> Tuple[bool, str]:
        query = """INSERT INTO GRANT_TABLE (purpose, date_awarded, duration, close_date, 
                   start_date, amount, region_id, division_id) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        return self.db.execute_query(query, (purpose, date_awarded, duration, close_date, 
                                              start_date, amount, region_id, division_id))
    
    def read_all(self) -> pd.DataFrame:
        query = """SELECT g.*, r.name as region_name, d.name as division_name 
                   FROM GRANT_TABLE g 
                   LEFT JOIN REGION r ON g.region_id = r.region_id
                   LEFT JOIN DIVISION d ON g.division_id = d.division_id"""
        success, result = self.db.fetch_query(query)
        return pd.DataFrame(result) if success else pd.DataFrame()
    
    def read_by_id(self, grant_id: int) -> Dict:
        success, result = self.db.fetch_query(
            "SELECT * FROM GRANT_TABLE WHERE grant_id = %s", (grant_id,)
        )
        return result[0] if success and result else {}
    
    def update(self, grant_id: int, purpose: str, date_awarded, 
               duration: int, close_date, start_date, 
               amount: float, region_id: int = None, division_id: int = None) -> Tuple[bool, str]:
        query = """UPDATE GRANT_TABLE SET purpose = %s, date_awarded = %s, duration = %s, 
                   close_date = %s, start_date = %s, amount = %s, region_id = %s, 
                   division_id = %s WHERE grant_id = %s"""
        return self.db.execute_query(query, (purpose, date_awarded, duration, close_date, 
                                              start_date, amount, region_id, division_id, grant_id))
    
    def delete(self, grant_id: int) -> Tuple[bool, str]:
        query = "DELETE FROM GRANT_TABLE WHERE grant_id = %s"
        return self.db.execute_query(query, (grant_id,))

# ==================== GRANTBENEFICIARY OPERATIONS ====================
class GrantBeneficiaryOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, grantee_id: int, institution: str, 
               description: str = None, county_of_institute: str = None) -> Tuple[bool, str]:
        query = """INSERT INTO GRANTBENEFICIARY (grantee_id, institution, description, county_of_institute) 
                   VALUES (%s, %s, %s, %s)"""
        return self.db.execute_query(query, (grantee_id, institution, description, county_of_institute))
    
    def read_all(self) -> pd.DataFrame:
        query = """SELECT gb.*, g.name as grantee_name 
                   FROM GRANTBENEFICIARY gb 
                   LEFT JOIN GRANTEE g ON gb.grantee_id = g.grantee_id"""
        success, result = self.db.fetch_query(query)
        return pd.DataFrame(result) if success else pd.DataFrame()
    
    def read_by_id(self, beneficiary_id: int) -> Dict:
        success, result = self.db.fetch_query(
            "SELECT * FROM GRANTBENEFICIARY WHERE beneficiary_id = %s", (beneficiary_id,)
        )
        return result[0] if success and result else {}
    
    def update(self, beneficiary_id: int, grantee_id: int, institution: str, 
               description: str = None, county_of_institute: str = None) -> Tuple[bool, str]:
        query = """UPDATE GRANTBENEFICIARY SET grantee_id = %s, institution = %s, 
                   description = %s, county_of_institute = %s WHERE beneficiary_id = %s"""
        return self.db.execute_query(query, (grantee_id, institution, description, 
                                              county_of_institute, beneficiary_id))
    
    def delete(self, beneficiary_id: int) -> Tuple[bool, str]:
        query = "DELETE FROM GRANTBENEFICIARY WHERE beneficiary_id = %s"
        return self.db.execute_query(query, (beneficiary_id,))

# ==================== MILESTONE OPERATIONS ====================
class MilestoneOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, grant_id: int, milestone_desc: str, 
               due_date, completion: int = 0) -> Tuple[bool, str]:
        query = """INSERT INTO TOTAL_MILESTONE (grant_id, milestone_desc, due_date, completion) 
                   VALUES (%s, %s, %s, %s)"""
        return self.db.execute_query(query, (grant_id, milestone_desc, due_date, completion))
    
    def read_all(self) -> pd.DataFrame:
        query = """SELECT m.*, g.purpose as grant_purpose 
                   FROM TOTAL_MILESTONE m 
                   LEFT JOIN GRANT_TABLE g ON m.grant_id = g.grant_id"""
        success, result = self.db.fetch_query(query)
        return pd.DataFrame(result) if success else pd.DataFrame()
    
    def read_by_id(self, milestone_id: int) -> Dict:
        success, result = self.db.fetch_query(
            "SELECT * FROM TOTAL_MILESTONE WHERE milestone_id = %s", (milestone_id,)
        )
        return result[0] if success and result else {}
    
    def read_by_grant(self, grant_id: int) -> pd.DataFrame:
        success, result = self.db.fetch_query(
            "SELECT * FROM TOTAL_MILESTONE WHERE grant_id = %s", (grant_id,)
        )
        return pd.DataFrame(result) if success else pd.DataFrame()
    
    def update(self, milestone_id: int, grant_id: int, milestone_desc: str, 
               due_date, completion: int) -> Tuple[bool, str]:
        query = """UPDATE TOTAL_MILESTONE SET grant_id = %s, milestone_desc = %s, 
                   due_date = %s, completion = %s WHERE milestone_id = %s"""
        return self.db.execute_query(query, (grant_id, milestone_desc, due_date, 
                                              completion, milestone_id))
    
    def delete(self, milestone_id: int) -> Tuple[bool, str]:
        query = "DELETE FROM TOTAL_MILESTONE WHERE milestone_id = %s"
        return self.db.execute_query(query, (milestone_id,))

# ==================== GRANTEE_UNIVS OPERATIONS ====================
class GranteeUnivsOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, grantee_id: int, grant_id: int, associated_body: str = None) -> Tuple[bool, str]:
        query = "INSERT INTO GRANTEE_UNIVS (grantee_id, grant_id, associated_body) VALUES (%s, %s, %s)"
        return self.db.execute_query(query, (grantee_id, grant_id, associated_body))
    
    def read_all(self) -> pd.DataFrame:
        query = """SELECT gu.*, g.name as grantee_name, gt.purpose as grant_purpose 
                   FROM GRANTEE_UNIVS gu
                   LEFT JOIN GRANTEE g ON gu.grantee_id = g.grantee_id
                   LEFT JOIN GRANT_TABLE gt ON gu.grant_id = gt.grant_id"""
        success, result = self.db.fetch_query(query)
        return pd.DataFrame(result) if success else pd.DataFrame()
    
    def read_by_grantee(self, grantee_id: int) -> pd.DataFrame:
        query = """SELECT gu.*, gt.purpose, gt.amount 
                   FROM GRANTEE_UNIVS gu
                   LEFT JOIN GRANT_TABLE gt ON gu.grant_id = gt.grant_id
                   WHERE gu.grantee_id = %s"""
        success, result = self.db.fetch_query(query, (grantee_id,))
        return pd.DataFrame(result) if success else pd.DataFrame()
    
    def update(self, grantee_id: int, grant_id: int, associated_body: str = None) -> Tuple[bool, str]:
        query = "UPDATE GRANTEE_UNIVS SET associated_body = %s WHERE grantee_id = %s AND grant_id = %s"
        return self.db.execute_query(query, (associated_body, grantee_id, grant_id))
    
    def delete(self, grantee_id: int, grant_id: int) -> Tuple[bool, str]:
        query = "DELETE FROM GRANTEE_UNIVS WHERE grantee_id = %s AND grant_id = %s"
        return self.db.execute_query(query, (grantee_id, grant_id))

# ==================== GRANT_TOPIC OPERATIONS ====================
class GrantTopicOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, grant_id: int, topic_id: int) -> Tuple[bool, str]:
        query = "INSERT INTO GRANT_TOPIC (grant_id, topic_id) VALUES (%s, %s)"
        return self.db.execute_query(query, (grant_id, topic_id))
    
    def read_all(self) -> pd.DataFrame:
        query = """SELECT gt_rel.*, g.purpose as grant_purpose, t.name as topic_name 
                   FROM GRANT_TOPIC gt_rel
                   LEFT JOIN GRANT_TABLE g ON gt_rel.grant_id = g.grant_id
                   LEFT JOIN TOPIC t ON gt_rel.topic_id = t.topic_id"""
        success, result = self.db.fetch_query(query)
        return pd.DataFrame(result) if success else pd.DataFrame()
    
    def read_by_grant(self, grant_id: int) -> pd.DataFrame:
        query = """SELECT t.* FROM GRANT_TOPIC gt
                   JOIN TOPIC t ON gt.topic_id = t.topic_id
                   WHERE gt.grant_id = %s"""
        success, result = self.db.fetch_query(query, (grant_id,))
        return pd.DataFrame(result) if success else pd.DataFrame()
    
    def delete(self, grant_id: int, topic_id: int) -> Tuple[bool, str]:
        query = "DELETE FROM GRANT_TOPIC WHERE grant_id = %s AND topic_id = %s"
        return self.db.execute_query(query, (grant_id, topic_id))
