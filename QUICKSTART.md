# Quick Start Guide

Get your Grant Management System running in 5 minutes!

## Option 1: Automated Setup (Recommended)

Run the setup script in PowerShell:

```powershell
.\setup.ps1
```

This will:

- Check Python and MySQL installation
- Install all dependencies
- Configure database settings
- Start the application

## Option 2: Manual Setup

### Step 1: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 2: Configure Database

Edit `app.py` line 30 and add your MySQL password:

```python
db = DatabaseConnection(
    host='localhost',
    user='root',
    password='root@123',  # ← Add your password
    database='grant_management'
)
```

### Step 3: Run Application

```powershell
streamlit run app.py
```

### Step 4: Initialize Database

1. Open http://localhost:8501 in your browser
2. In the sidebar, expand **"Database Setup"**
3. Click **"Initialize Schema"** button
4. Wait for success message

## Using the Application

### Create Your First Grant

1. **Create a Division** (e.g., "Research Division")

   - Go to Division → Create tab
   - Enter name and description
   - Click "Create"

2. **Create a Region** (e.g., "North America")

   - Go to Region → Create tab
   - Enter region name
   - Click "Create"

3. **Create a Grantee** (e.g., "University of Science")

   - Go to Grantee → Create tab
   - Fill in name, email, address, phone
   - Select grantee type
   - Click "Create"

4. **Create a Grant**

   - Go to Grant → Create tab
   - Enter purpose, dates, duration, amount
   - Select region and division
   - Click "Create"

5. **Add Milestones**
   - Go to Milestone → Create tab
   - Select the grant
   - Enter milestone details
   - Set due date and completion %
   - Click "Create"

### Link Entities

**Link Grantee to Grant:**

1. Go to Grantee-Grant Link → Create Link
2. Select grantee and grant
3. Enter associated body (optional)
4. Click "Create Link"

**Link Grant to Topic:**

1. First create a topic in Topic
2. Go to Grant-Topic Link → Create Link
3. Select grant and topic
4. Click "Create Link"

## Common Operations

### View All Records

- Navigate to any entity
- Click **View All** tab
- See all records in a table

### Update a Record

- Navigate to entity
- Click **Update** tab
- Select record from dropdown
- Modify fields
- Click "Update"

### Delete a Record

- Navigate to entity
- Click **Delete** tab
- Select record to delete
- Click "Delete" button
- Confirm action

## Tips

1. **Sample Data**: The schema includes sample data for divisions, regions, topics, and grantees
2. **Refresh**: Page automatically refreshes after each operation
3. **Validation**: Required fields are marked with \*
4. **Relationships**: Create parent entities before child entities (e.g., Grant before Milestone)
5. **Dashboard**: Check Home for quick statistics

## Troubleshooting

**Application won't start?**

- Ensure MySQL is running: `net start MySQL` (as Administrator)
- Check if port 8501 is free
- Verify Python dependencies are installed

**Can't connect to database?**

- Check MySQL service is running
- Verify username/password in app.py
- Ensure MySQL is on port 3306 (default)

**Schema initialization fails?**

- Make sure schema.sql is in the same directory
- Check MySQL user has CREATE DATABASE permission
- Try running schema.sql manually in MySQL Workbench

## Need Help?

Check the full README.md for detailed documentation and troubleshooting.

---

**Ready to manage grants like a pro!**
