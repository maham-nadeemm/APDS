"""
Simple script to view database schema and data
Run: python view_database.py
"""
import sqlite3
import os
from tabulate import tabulate

def view_database():
    """View database schema and data"""
    db_path = os.path.join(os.path.dirname(__file__), 'operations_monitoring.db')
    
    if not os.path.exists(db_path):
        print(f"Database file not found at: {db_path}")
        print("The database will be created when you first run the application.")
        return
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("=" * 80)
    print("DATABASE SCHEMA - ALL TABLES")
    print("=" * 80)
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    if not tables:
        print("No tables found in database.")
        return
    
    for table in tables:
        table_name = table['name']
        print(f"\n{'=' * 80}")
        print(f"TABLE: {table_name}")
        print(f"{'=' * 80}")
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print("\nColumns:")
        headers = ["CID", "Name", "Type", "Not Null", "Default", "PK"]
        rows = [[col[0], col[1], col[2], col[3], col[4], col[5]] for col in columns]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        
        # Get foreign keys
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        foreign_keys = cursor.fetchall()
        if foreign_keys:
            print("\nForeign Keys:")
            for fk in foreign_keys:
                print(f"  {fk[3]} -> {fk[2]}.{fk[4]}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
        count = cursor.fetchone()
        print(f"\nRow Count: {count['count']}")
        
        # Show sample data (first 5 rows)
        if count['count'] > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
            rows = cursor.fetchall()
            if rows:
                print("\nSample Data (first 5 rows):")
                # Get column names
                col_names = [description[0] for description in cursor.description]
                data_rows = []
                for row in rows:
                    data_rows.append([str(row[col])[:50] if row[col] is not None else 'NULL' for col in col_names])
                print(tabulate(data_rows, headers=col_names, tablefmt="grid", maxcolwidths=[30]*len(col_names)))
    
    print(f"\n{'=' * 80}")
    print("Database file location:", db_path)
    print("=" * 80)
    
    conn.close()

if __name__ == '__main__':
    try:
        view_database()
    except ImportError:
        print("tabulate module not found. Installing...")
        os.system("pip install tabulate")
        view_database()

