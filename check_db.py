import sqlite3
import os

db_path = 'operations_monitoring.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("DATABASE FILE INFORMATION")
    print("=" * 60)
    print(f"Path: {os.path.abspath(db_path)}")
    print(f"Size: {os.path.getsize(db_path):,} bytes ({os.path.getsize(db_path) / 1024:.2f} KB)")
    
    # Get table count
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Tables: {len(tables)}")
    
    # Get row counts
    print("\nRow Counts:")
    print("-" * 60)
    cursor.execute("SELECT COUNT(*) FROM users")
    print(f"Users: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM equipment")
    print(f"Equipment: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM faults")
    print(f"Faults: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM daily_monitoring")
    print(f"Daily Monitoring: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM root_cause_analysis")
    print(f"Root Cause Analysis: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM resolution_reports")
    print(f"Resolution Reports: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM notifications")
    print(f"Notifications: {cursor.fetchone()[0]}")
    
    conn.close()
    print("=" * 60)
else:
    print(f"Database file not found: {db_path}")




