"""
Simple Database Viewer - Opens and displays database in a readable format
"""
import sqlite3
import os
import sys

def view_database_simple():
    """Simple database viewer"""
    db_path = 'operations_monitoring.db'
    
    if not os.path.exists(db_path):
        print(f"ERROR: Database file not found: {db_path}")
        print(f"Current directory: {os.getcwd()}")
        return
    
    print("=" * 80)
    print(f"VIEWING DATABASE: {os.path.abspath(db_path)}")
    print("=" * 80)
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall() if row[0] != 'sqlite_sequence']
        
        print(f"\nFound {len(tables)} tables:")
        for table in tables:
            print(f"  - {table}")
        
        # Interactive menu
        while True:
            print("\n" + "=" * 80)
            print("DATABASE VIEWER MENU")
            print("=" * 80)
            print("1. View all tables and row counts")
            print("2. View specific table data")
            print("3. View users")
            print("4. View equipment")
            print("5. View faults")
            print("6. View monitoring records")
            print("7. View relationships")
            print("8. Export table to CSV")
            print("9. Exit")
            
            choice = input("\nEnter your choice (1-9): ").strip()
            
            if choice == '1':
                print("\n" + "-" * 80)
                print("TABLE ROW COUNTS")
                print("-" * 80)
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"{table:30} : {count:5} rows")
            
            elif choice == '2':
                print("\nAvailable tables:")
                for i, table in enumerate(tables, 1):
                    print(f"{i}. {table}")
                try:
                    table_idx = int(input("\nEnter table number: ")) - 1
                    if 0 <= table_idx < len(tables):
                        table_name = tables[table_idx]
                        cursor.execute(f"SELECT * FROM {table_name} LIMIT 20")
                        rows = cursor.fetchall()
                        if rows:
                            print(f"\n{table_name} (showing first 20 rows):")
                            print("-" * 80)
                            # Get column names
                            col_names = [description[0] for description in cursor.description]
                            print(" | ".join(col_names))
                            print("-" * 80)
                            for row in rows:
                                values = [str(row[col])[:30] if row[col] is not None else 'NULL' for col in col_names]
                                print(" | ".join(values))
                        else:
                            print(f"No data in {table_name}")
                    else:
                        print("Invalid table number")
                except ValueError:
                    print("Invalid input")
            
            elif choice == '3':
                cursor.execute("SELECT id, username, role, full_name, email FROM users")
                rows = cursor.fetchall()
                print("\nUSERS:")
                print("-" * 80)
                print(f"{'ID':<5} {'Username':<15} {'Role':<12} {'Full Name':<25} {'Email':<25}")
                print("-" * 80)
                for row in rows:
                    print(f"{row[0]:<5} {row[1]:<15} {row[2]:<12} {row[3]:<25} {row[4]:<25}")
            
            elif choice == '4':
                cursor.execute("SELECT id, equipment_code, equipment_name, equipment_type, location, status FROM equipment")
                rows = cursor.fetchall()
                print("\nEQUIPMENT:")
                print("-" * 80)
                print(f"{'ID':<5} {'Code':<10} {'Name':<30} {'Type':<15} {'Location':<20} {'Status':<12}")
                print("-" * 80)
                for row in rows:
                    print(f"{row[0]:<5} {row[1]:<10} {row[2][:28]:<30} {row[3]:<15} {row[4][:18]:<20} {row[5]:<12}")
            
            elif choice == '5':
                cursor.execute("""
                    SELECT f.id, f.equipment_id, e.equipment_name, u.username, 
                           f.fault_description, f.severity, f.status, f.reported_at
                    FROM faults f
                    LEFT JOIN equipment e ON f.equipment_id = e.id
                    LEFT JOIN users u ON f.reported_by = u.id
                    ORDER BY f.id DESC
                    LIMIT 20
                """)
                rows = cursor.fetchall()
                print("\nFAULTS:")
                print("-" * 80)
                for row in rows:
                    print(f"ID: {row[0]}")
                    print(f"  Equipment: {row[1]} - {row[2] or 'N/A'}")
                    print(f"  Reported by: {row[3] or 'N/A'}")
                    print(f"  Description: {row[4][:60] if row[4] else 'N/A'}...")
                    print(f"  Severity: {row[5]}, Status: {row[6]}")
                    print(f"  Reported at: {row[7] or 'N/A'}")
                    print("-" * 80)
            
            elif choice == '6':
                cursor.execute("""
                    SELECT m.id, m.monitoring_date, m.shift, e.equipment_code, 
                           u.username, m.voltage, m.current, m.power_factor, m.operational_status
                    FROM daily_monitoring m
                    LEFT JOIN equipment e ON m.equipment_id = e.id
                    LEFT JOIN users u ON m.technician_id = u.id
                    ORDER BY m.id DESC
                    LIMIT 20
                """)
                rows = cursor.fetchall()
                print("\nMONITORING RECORDS:")
                print("-" * 80)
                for row in rows:
                    print(f"ID: {row[0]}, Date: {row[1]}, Shift: {row[2] or 'N/A'}")
                    print(f"  Equipment: {row[3] or 'N/A'}, Technician: {row[4] or 'N/A'}")
                    print(f"  Voltage: {row[5] or 'N/A'}V, Current: {row[6] or 'N/A'}A, Power Factor: {row[7] or 'N/A'}")
                    print(f"  Status: {row[8]}")
                    print("-" * 80)
            
            elif choice == '7':
                print("\nRELATIONSHIPS:")
                print("-" * 80)
                # Users -> Faults
                cursor.execute("SELECT COUNT(*) FROM faults")
                print(f"Total Faults: {cursor.fetchone()[0]}")
                # Users -> Monitoring
                cursor.execute("SELECT COUNT(*) FROM daily_monitoring")
                print(f"Total Monitoring Records: {cursor.fetchone()[0]}")
                # Equipment -> Faults
                cursor.execute("SELECT COUNT(DISTINCT equipment_id) FROM faults")
                print(f"Equipment with Faults: {cursor.fetchone()[0]}")
                # Equipment -> Monitoring
                cursor.execute("SELECT COUNT(DISTINCT equipment_id) FROM daily_monitoring")
                print(f"Equipment with Monitoring: {cursor.fetchone()[0]}")
            
            elif choice == '8':
                print("\nAvailable tables:")
                for i, table in enumerate(tables, 1):
                    print(f"{i}. {table}")
                try:
                    table_idx = int(input("\nEnter table number to export: ")) - 1
                    if 0 <= table_idx < len(tables):
                        table_name = tables[table_idx]
                        csv_file = f"{table_name}.csv"
                        cursor.execute(f"SELECT * FROM {table_name}")
                        rows = cursor.fetchall()
                        col_names = [description[0] for description in cursor.description]
                        
                        with open(csv_file, 'w', encoding='utf-8') as f:
                            # Write header
                            f.write(','.join(col_names) + '\n')
                            # Write data
                            for row in rows:
                                values = [str(row[col]) if row[col] is not None else '' for col in col_names]
                                f.write(','.join(values) + '\n')
                        
                        print(f"Exported {len(rows)} rows to {csv_file}")
                    else:
                        print("Invalid table number")
                except Exception as e:
                    print(f"Error exporting: {e}")
            
            elif choice == '9':
                print("\nExiting...")
                break
            
            else:
                print("Invalid choice. Please enter 1-9.")
        
        conn.close()
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    view_database_simple()




