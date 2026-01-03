# How to View the Database

## Database File Location

The database file is: **`operations_monitoring.db`** (located in the project root directory)

The database schema is defined in: **`app/database/db_connection.py`** (in the `_create_tables()` method)

## Viewing Options

### Option 1: DB Browser for SQLite (Recommended - Free GUI Tool)

1. Download and install DB Browser for SQLite from: https://sqlitebrowser.org/
2. Open DB Browser for SQLite
3. Click "Open Database"
4. Navigate to your project folder and select `operations_monitoring.db`
5. You can now:
   - Browse Data: View data in all tables
   - Database Structure: See the schema with relationships
   - Execute SQL: Run custom queries
   - View foreign key relationships visually

### Option 2: VS Code Extension

1. Install the "SQLite Viewer" extension in VS Code
2. Right-click on `operations_monitoring.db` in the file explorer
3. Select "Open Database" or "Open with SQLite Viewer"
4. Browse tables and run queries directly in VS Code

### Option 3: Command Line (sqlite3)

If you have SQLite installed:

```bash
sqlite3 operations_monitoring.db
```

Then run commands like:
```sql
-- List all tables
.tables

-- View schema of a specific table
.schema users

-- View all data in a table
SELECT * FROM users;

-- View table info
PRAGMA table_info(users);

-- View foreign keys
PRAGMA foreign_key_list(users);

-- Exit
.exit
```

### Option 4: Python Script

I've created a simple Python script (`view_database.py`) that you can run:

```bash
python view_database.py
```

This will display:
- All tables and their schemas
- Column definitions
- Foreign key relationships
- Row counts
- Sample data from each table

### Option 5: View Schema in Code

The complete database schema with all relationships is defined in:
**`app/database/db_connection.py`** (lines 28-323)

All table definitions including foreign keys are clearly documented there.

## Database Tables

The database contains the following tables:

1. **users** - User accounts and roles
2. **equipment** - Equipment inventory
3. **daily_monitoring** - Monitoring records
4. **faults** - Fault reports
5. **root_cause_analysis** - RCA records
6. **resolution_reports** - Resolution reports
7. **notifications** - User notifications
8. **escalations** - Escalation records
9. **performance_reports** - Performance reports (UC-04)
10. **technical_references** - Technical references (UC-07)
11. **documentation_packages** - Documentation packages (UC-09, UC-10)
12. **documentation_items** - Documentation items (UC-09, UC-10)
13. **vendors** - Vendor information (UC-15)
14. **delivery_service_verification** - Delivery/Service verifications (UC-13, UC-14, UC-15)
15. **data_reverification** - Data re-verification records (UC-05)
16. **audit_logs** - Audit trail

## Note

The database file will be automatically created when you first run the application (`python app.py`). If it doesn't exist yet, run the application once to create it.




