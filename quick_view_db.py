"""
Quick Database Viewer - Non-interactive, shows all important data
"""
import sqlite3
import os

def quick_view():
    """Quick view of database contents"""
    db_path = 'operations_monitoring.db'
    
    if not os.path.exists(db_path):
        print(f"ERROR: Database file not found: {db_path}")
        return
    
    print("=" * 80)
    print(f"QUICK VIEW: {os.path.abspath(db_path)}")
    print("=" * 80)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Table counts
    print("\nTABLE ROW COUNTS:")
    print("-" * 80)
    tables = ['users', 'equipment', 'faults', 'daily_monitoring', 'root_cause_analysis', 
              'resolution_reports', 'notifications', 'vendors']
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table:30} : {count:5} rows")
        except:
            pass
    
    # Users
    print("\n" + "=" * 80)
    print("USERS")
    print("=" * 80)
    cursor.execute("SELECT id, username, role, full_name, email FROM users")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Username: {row[1]}, Role: {row[2]}, Name: {row[3]}, Email: {row[4]}")
    
    # Equipment
    print("\n" + "=" * 80)
    print("EQUIPMENT")
    print("=" * 80)
    cursor.execute("SELECT id, equipment_code, equipment_name, status FROM equipment")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Code: {row[1]}, Name: {row[2]}, Status: {row[3]}")
    
    # Faults
    print("\n" + "=" * 80)
    print("FAULTS")
    print("=" * 80)
    cursor.execute("""
        SELECT f.id, e.equipment_code, u.username, f.fault_description, 
               f.severity, f.status, f.reported_at
        FROM faults f
        LEFT JOIN equipment e ON f.equipment_id = e.id
        LEFT JOIN users u ON f.reported_by = u.id
        ORDER BY f.id DESC
    """)
    for row in cursor.fetchall():
        desc = row[3][:50] + '...' if row[3] and len(row[3]) > 50 else (row[3] or 'N/A')
        print(f"ID: {row[0]}, Equipment: {row[1] or 'N/A'}, Reported by: {row[2] or 'N/A'}")
        print(f"  Description: {desc}")
        print(f"  Severity: {row[4]}, Status: {row[5]}, Date: {row[6] or 'N/A'}")
        print()
    
    # Monitoring
    print("=" * 80)
    print("MONITORING RECORDS")
    print("=" * 80)
    cursor.execute("""
        SELECT m.id, m.monitoring_date, e.equipment_code, u.username,
               m.voltage, m.current, m.power_factor, m.operational_status
        FROM daily_monitoring m
        LEFT JOIN equipment e ON m.equipment_id = e.id
        LEFT JOIN users u ON m.technician_id = u.id
        ORDER BY m.id DESC
    """)
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Date: {row[1]}, Equipment: {row[2] or 'N/A'}, Technician: {row[3] or 'N/A'}")
        print(f"  Voltage: {row[4] or 'N/A'}V, Current: {row[5] or 'N/A'}A, Power Factor: {row[6] or 'N/A'}, Status: {row[7]}")
        print()
    
    conn.close()
    print("=" * 80)
    print("To view more details, use:")
    print("  python view_database_relations.py  (for relational view)")
    print("  python view_database.py             (for full schema)")
    print("=" * 80)

if __name__ == '__main__':
    quick_view()




