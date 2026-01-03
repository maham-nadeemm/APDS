"""
View Database with Relational Information
Shows foreign key relationships and connected data
"""
import sqlite3
import os
from tabulate import tabulate
from collections import defaultdict

def view_database_relations():
    """View database with relational information"""
    db_path = os.path.join(os.path.dirname(__file__), 'operations_monitoring.db')
    
    if not os.path.exists(db_path):
        print(f"Database file not found at: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("=" * 80)
    print("DATABASE RELATIONAL VIEW")
    print("=" * 80)
    
    # Get all foreign key relationships
    print("\n" + "=" * 80)
    print("FOREIGN KEY RELATIONSHIPS")
    print("=" * 80)
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    relationships = defaultdict(list)
    
    for table in tables:
        table_name = table['name']
        if table_name == 'sqlite_sequence':
            continue
        
        # Get foreign keys for each table
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        fks = cursor.fetchall()
        
        if fks:
            print(f"\n{table_name}:")
            for fk in fks:
                from_col = fk[3]  # Column in this table
                to_table = fk[2]   # Referenced table
                to_col = fk[4]     # Referenced column
                relationships[table_name].append({
                    'from_column': from_col,
                    'to_table': to_table,
                    'to_column': to_col
                })
                print(f"  {from_col} -> {to_table}.{to_col}")
    
    # Show data with relationships
    print("\n" + "=" * 80)
    print("RELATIONAL DATA VIEW")
    print("=" * 80)
    
    # Users and their related data
    print("\n" + "-" * 80)
    print("USERS AND THEIR ACTIVITIES")
    print("-" * 80)
    
    cursor.execute("""
        SELECT u.id, u.username, u.role, u.full_name,
               (SELECT COUNT(*) FROM faults WHERE reported_by = u.id) as faults_reported,
               (SELECT COUNT(*) FROM daily_monitoring WHERE technician_id = u.id) as monitoring_records,
               (SELECT COUNT(*) FROM root_cause_analysis WHERE analyzed_by = u.id) as rca_created,
               (SELECT COUNT(*) FROM resolution_reports WHERE prepared_by = u.id) as reports_prepared
        FROM users u
        ORDER BY u.id
    """)
    users_data = cursor.fetchall()
    if users_data:
        headers = ["ID", "Username", "Role", "Full Name", "Faults Reported", 
                  "Monitoring Records", "RCA Created", "Reports Prepared"]
        rows = [[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]] 
                for row in users_data]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    # Equipment and related data
    print("\n" + "-" * 80)
    print("EQUIPMENT AND RELATED RECORDS")
    print("-" * 80)
    
    cursor.execute("""
        SELECT e.id, e.equipment_code, e.equipment_name, e.status,
               (SELECT COUNT(*) FROM faults WHERE equipment_id = e.id) as fault_count,
               (SELECT COUNT(*) FROM daily_monitoring WHERE equipment_id = e.id) as monitoring_count
        FROM equipment e
        ORDER BY e.id
    """)
    equipment_data = cursor.fetchall()
    if equipment_data:
        headers = ["ID", "Code", "Name", "Status", "Faults", "Monitoring Records"]
        rows = [[row[0], row[1], row[2], row[3], row[4], row[5]] for row in equipment_data]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    # Faults with related data
    print("\n" + "-" * 80)
    print("FAULTS WITH RELATED INFORMATION")
    print("-" * 80)
    
    cursor.execute("""
        SELECT f.id, f.equipment_id, e.equipment_name, 
               u.username as reported_by_user, f.severity, f.status,
               f.reported_at,
               (SELECT COUNT(*) FROM root_cause_analysis WHERE fault_id = f.id) as rca_count,
               (SELECT COUNT(*) FROM resolution_reports WHERE fault_id = f.id) as report_count
        FROM faults f
        LEFT JOIN equipment e ON f.equipment_id = e.id
        LEFT JOIN users u ON f.reported_by = u.id
        ORDER BY f.id DESC
        LIMIT 10
    """)
    faults_data = cursor.fetchall()
    if faults_data:
        headers = ["Fault ID", "Equipment ID", "Equipment Name", "Reported By", 
                  "Severity", "Status", "Reported At", "RCA Count", "Report Count"]
        rows = []
        for row in faults_data:
            reported_at = row[6][:10] if row[6] else '-'
            rows.append([row[0], row[1], row[2] or '-', row[3] or '-', 
                        row[4], row[5], reported_at, row[7], row[8]])
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print("No faults found")
    
    # Monitoring records with equipment and user info
    print("\n" + "-" * 80)
    print("MONITORING RECORDS WITH EQUIPMENT AND TECHNICIAN")
    print("-" * 80)
    
    cursor.execute("""
        SELECT m.id, m.monitoring_date, m.shift, 
               e.equipment_code, e.equipment_name,
               u.username as technician, m.voltage, m.current, m.power_factor,
               m.operational_status
        FROM daily_monitoring m
        LEFT JOIN equipment e ON m.equipment_id = e.id
        LEFT JOIN users u ON m.technician_id = u.id
        ORDER BY m.id DESC
        LIMIT 10
    """)
    monitoring_data = cursor.fetchall()
    if monitoring_data:
        headers = ["ID", "Date", "Shift", "Equipment Code", "Equipment Name", 
                  "Technician", "Voltage", "Current", "Power Factor", "Status"]
        rows = []
        for row in monitoring_data:
            date_str = row[1][:10] if row[1] else '-'
            rows.append([row[0], date_str, row[2] or '-', row[3] or '-', row[4] or '-',
                        row[5] or '-', row[6] or '-', row[7] or '-', row[8] or '-', row[9]])
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print("No monitoring records found")
    
    # Root Cause Analysis with fault and user info
    print("\n" + "-" * 80)
    print("ROOT CAUSE ANALYSIS WITH FAULT AND ANALYST")
    print("-" * 80)
    
    cursor.execute("""
        SELECT rca.id, rca.fault_id, f.fault_description,
               u.username as analyzed_by, rca.root_cause, rca.analysis_date
        FROM root_cause_analysis rca
        LEFT JOIN faults f ON rca.fault_id = f.id
        LEFT JOIN users u ON rca.analyzed_by = u.id
        ORDER BY rca.id DESC
        LIMIT 10
    """)
    rca_data = cursor.fetchall()
    if rca_data:
        headers = ["RCA ID", "Fault ID", "Fault Description", "Analyzed By", 
                  "Root Cause", "Analysis Date"]
        rows = []
        for row in rca_data:
            desc = (row[2][:40] + '...') if row[2] and len(row[2]) > 40 else (row[2] or '-')
            root_cause = (row[4][:30] + '...') if row[4] and len(row[4]) > 30 else (row[4] or '-')
            date_str = row[5][:10] if row[5] else '-'
            rows.append([row[0], row[1] or '-', desc, row[3] or '-', root_cause, date_str])
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print("No RCA records found")
    
    # Resolution Reports with fault and user info
    print("\n" + "-" * 80)
    print("RESOLUTION REPORTS WITH FAULT AND PREPARER")
    print("-" * 80)
    
    cursor.execute("""
        SELECT rr.id, rr.fault_id, f.fault_description,
               u.username as prepared_by, rr.status, rr.created_at
        FROM resolution_reports rr
        LEFT JOIN faults f ON rr.fault_id = f.id
        LEFT JOIN users u ON rr.prepared_by = u.id
        ORDER BY rr.id DESC
        LIMIT 10
    """)
    reports_data = cursor.fetchall()
    if reports_data:
        headers = ["Report ID", "Fault ID", "Fault Description", "Prepared By", 
                  "Status", "Created At"]
        rows = []
        for row in reports_data:
            desc = (row[2][:40] + '...') if row[2] and len(row[2]) > 40 else (row[2] or '-')
            date_str = row[5][:10] if row[5] else '-'
            rows.append([row[0], row[1] or '-', desc, row[3] or '-', row[4], date_str])
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print("No resolution reports found")
    
    # Entity Relationship Summary
    print("\n" + "=" * 80)
    print("ENTITY RELATIONSHIP SUMMARY")
    print("=" * 80)
    
    print("\nCore Entities:")
    print("  Users (id) -> Referenced by: faults, monitoring, rca, reports, etc.")
    print("  Equipment (id) -> Referenced by: faults, monitoring, technical_references")
    print("  Faults (id) -> Referenced by: rca, reports, documentation_packages, escalations")
    print("  Daily Monitoring (id) -> Referenced by: data_reverification")
    
    print("\nRelationship Flow:")
    print("  User -> Equipment -> Monitoring/Faults")
    print("  Fault -> Root Cause Analysis -> Resolution Report")
    print("  Fault -> Documentation Package")
    print("  Monitoring -> Data Re-verification")
    
    conn.close()
    print("\n" + "=" * 80)
    print("Database file location:", db_path)
    print("=" * 80)

if __name__ == '__main__':
    try:
        view_database_relations()
    except ImportError:
        print("tabulate module not found. Installing...")
        os.system("pip install tabulate")
        view_database_relations()




