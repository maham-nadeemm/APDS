# How to View operations_monitoring.db File

SQLite database files (`.db`) are binary files and **cannot be opened directly** like text files. You need special tools to view them.

## Method 1: Use Python Scripts (Easiest)

### Quick View
```bash
python quick_view_db.py
```
Shows all important data in a readable format.

### Detailed Relational View
```bash
python view_database_relations.py
```
Shows data with relationships and joins.

### Full Schema View
```bash
python view_database.py
```
Shows complete database schema and all tables.

### Entity Relationship Diagram
```bash
python view_er_diagram.py
```
Shows visual ER diagrams.

## Method 2: Use DB Browser for SQLite (Recommended GUI Tool)

1. **Download DB Browser for SQLite** (Free):
   - Windows: https://sqlitebrowser.org/dl/
   - Or use: `winget install sqlitebrowser.sqlitebrowser`

2. **Open the database**:
   - Launch DB Browser for SQLite
   - Click "Open Database"
   - Navigate to: `C:\Users\S A Z\Desktop\NEW JUNIORS PROJECT\operations_monitoring.db`
   - Click Open

3. **Browse the database**:
   - Click "Browse Data" tab
   - Select any table from the dropdown
   - View, edit, and export data

## Method 3: Use Command Line (sqlite3)

If you have SQLite installed:

```bash
sqlite3 operations_monitoring.db
```

Then use SQL commands:
```sql
.tables                    -- List all tables
.schema                    -- Show schema
SELECT * FROM users;       -- View users table
SELECT * FROM equipment;   -- View equipment table
.quit                      -- Exit
```

## Method 4: Use VS Code Extension

1. Install "SQLite Viewer" extension in VS Code
2. Right-click on `operations_monitoring.db`
3. Select "Open Database"
4. Browse tables in the sidebar

## Method 5: Use Online Tools

1. Go to https://sqliteviewer.app/
2. Upload your `operations_monitoring.db` file
3. Browse tables online

## Quick Reference

| Method | Best For | Difficulty |
|--------|----------|------------|
| Python Scripts | Quick viewing, automation | Easy |
| DB Browser | Full GUI, editing | Easy |
| Command Line | Advanced users | Medium |
| VS Code Extension | Developers | Easy |
| Online Tools | Quick look, no install | Easy |

## Recommended: DB Browser for SQLite

For the best experience, download **DB Browser for SQLite** - it's free, easy to use, and provides a full GUI to:
- Browse all tables
- View relationships
- Edit data
- Run SQL queries
- Export to CSV/JSON
- View database structure

Download: https://sqlitebrowser.org/




