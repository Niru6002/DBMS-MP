# Grant Management System

A comprehensive database management system for managing grants, grantees, divisions, regions, topics, milestones, and beneficiaries using MySQL and Streamlit.

## Project Structure

```
DBMS MP/
├── app.py                 # Streamlit frontend application
├── db_operations.py       # Database operations and CRUD functions
├── schema.sql            # Database schema with table definitions
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Database Schema

The system includes the following entities:

1. **DIVISION** - Organizational divisions managing grants
2. **REGION** - Geographic regions
3. **TOPIC** - Grant topics and categories
4. **GRANTEE** - Organizations or individuals receiving grants
5. **GRANT_TABLE** - Main grant information
6. **GRANTBENEFICIARY** - Beneficiaries of grants
7. **TOTAL_MILESTONE** - Milestones for each grant
8. **GRANTEE_UNIVS** - Many-to-many relationship between grantees and grants
9. **GRANT_TOPIC** - Many-to-many relationship between grants and topics

## Setup Instructions

### Prerequisites

1. **Python 3.8+** installed on your system
2. **MySQL Server** installed and running
3. **Git** (optional, for cloning)

### Step 1: Install MySQL

If you don't have MySQL installed:

**Windows:**

- Download MySQL Installer from https://dev.mysql.com/downloads/installer/
- Run the installer and select "MySQL Server"
- Set a root password (or leave it blank for this project)
- Start the MySQL service

**Verify MySQL is running:**

```powershell
mysql --version
```

### Step 2: Install Python Dependencies

Open PowerShell in the project directory and run:

```powershell
pip install -r requirements.txt
```

This will install:

- `streamlit` - Web application framework
- `mysql-connector-python` - MySQL database connector
- `pandas` - Data manipulation library

### Step 3: Configure Database Connection

Open `db_operations.py` and update the database connection parameters if needed:

```python
def init_db():
    db = DatabaseConnection(
        host='localhost',
        user='root',
        password='',  # Add your MySQL root password here
        database='grant_management'
    )
```

**Important:** If your MySQL root user has a password, add it in the `password` field.

### Step 4: Run the Application

In PowerShell, navigate to the project directory and run:

```powershell
streamlit run app.py
```

The application will automatically:

- Create the database `grant_management` if it doesn't exist
- Open in your default browser at `http://localhost:8501`

### Step 5: Initialize Database Schema

Once the app is running:

1. Look at the sidebar
2. Expand **"Database Setup"**
3. Click **"Initialize Schema"** button

This will create all tables and insert sample data.

## Using the Application

### Navigation

The sidebar contains navigation to different entities:

- **Home** - Dashboard with statistics
- **Division** - Manage organizational divisions
- **Region** - Manage geographic regions
- **Topic** - Manage grant topics
- **Grantee** - Manage grantees
- **Grant** - Manage grants
- **Beneficiary** - Manage beneficiaries
- **Milestone** - Manage grant milestones
- **Grantee-Grant Link** - Link grantees to grants
- **Grant-Topic Link** - Link grants to topics

### CRUD Operations

Each entity page has 4 tabs:

1. **View All** - Display all records in a table
2. **Create** - Add new records
3. **Update** - Modify existing records
4. **Delete** - Remove records

## Troubleshooting

### Issue: "Access denied for user 'root'@'localhost'"

**Solution:** Update the password in `app.py`:

```python
db = DatabaseConnection(
    host='localhost',
    user='root',
    password='your_mysql_password',  # Add your password here
    database='grant_management'
)
```

### Issue: "Can't connect to MySQL server"

**Solution:**

1. Make sure MySQL service is running
2. In Windows Services, start "MySQL" service
3. Or run in PowerShell as Administrator:
   ```powershell
   net start MySQL
   ```

### Issue: "Port 8501 is already in use"

**Solution:**

1. Close any existing Streamlit applications
2. Or run on a different port:
   ```powershell
   streamlit run app.py --server.port 8502
   ```

### Issue: "schema.sql file not found"

**Solution:** Make sure you're running the command from the project directory where `schema.sql` is located.

## Features

### Dashboard

- Quick statistics on total grants, grantees, and milestones
- Overview of the system

### Complete CRUD Operations

- Create, Read, Update, Delete for all entities
- Form validation
- Success/error messages
- Data tables with full visibility

### Relationship Management

- Link grantees to grants with associated body information
- Link grants to topics for categorization
- View all relationships in tabular format

### Data Integrity

- Foreign key constraints
- Cascading deletes where appropriate
- SET NULL for optional relationships

## UI Features

- **Modern Design** - Clean and intuitive interface
- **Responsive Layout** - Wide layout for better data visibility
- **Color-coded Tabs** - Easy navigation between operations
- **Real-time Updates** - Instant data refresh after operations
- **Form Validation** - Required field indicators
- **Data Tables** - Full-width data display with pandas

## Sample Data

The schema includes sample data for:

- 3 Divisions (Research, Education, Community Development)
- 4 Regions (North America, Europe, Asia Pacific, Latin America)
- 4 Topics (STEM Education, Healthcare Research, etc.)
- 3 Grantees (University, Institute, Foundation)

## Security Note

**Important:** This is a development/educational project. For production use:

- Use environment variables for database credentials
- Implement user authentication
- Add input sanitization
- Use parameterized queries (already implemented)
- Enable SSL for database connections

## Database Operations

The `db_operations.py` file provides classes for each entity:

- `DivisionOperations`
- `RegionOperations`
- `TopicOperations`
- `GranteeOperations`
- `GrantOperations`
- `GrantBeneficiaryOperations`
- `MilestoneOperations`
- `GranteeUnivsOperations`
- `GrantTopicOperations`

Each class includes methods:

- `create()` - Insert new record
- `read_all()` - Get all records as DataFrame
- `read_by_id()` - Get specific record
- `update()` - Modify existing record
- `delete()` - Remove record

## Tips

1. **Always initialize the schema first** before adding data
2. **Create entities in order**: Division → Region → Topic → Grantee → Grant → Milestone
3. **Use the relationships tabs** to link grants with grantees and topics
4. **Check the View All tab** to see your data after each operation
5. **The database persists** - your data will be saved between sessions

## Support

For issues or questions:

1. Check the Troubleshooting section
2. Verify MySQL is running
3. Check database credentials
4. Review error messages in the Streamlit interface

## License

This is an educational project for DBMS coursework.

---

**Happy Grant Managing!**
