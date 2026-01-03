"""
Entity Relationship Diagram View
Shows visual representation of database relationships
"""
import sqlite3
import os

def view_er_diagram():
    """View Entity Relationship Diagram"""
    db_path = os.path.join(os.path.dirname(__file__), 'operations_monitoring.db')
    
    if not os.path.exists(db_path):
        print(f"Database file not found at: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("=" * 80)
    print("ENTITY RELATIONSHIP DIAGRAM")
    print("=" * 80)
    
    # Core entities
    print("\n" + "=" * 80)
    print("CORE ENTITIES")
    print("=" * 80)
    
    print("""
    +-------------+
    |    USERS    |
    |  (id, PK)   |
    |  username   |
    |  role       |
    |  full_name  |
    +------+------+
           |
           | (referenced by)
           |
    +------+------------------------------------------------------+
    |                                                              |
    v              v              v              v                v
+---------+  +----------+  +--------+  +------------+  +----------+
| FAULTS  |  |MONITORING|  |  RCA   |  |  REPORTS   |  |NOTIFICA- |
|         |  |          |  |        |  |            |  |  TIONS   |
|(id, PK) |  |(id, PK)  |  |(id,PK) |  |(id, PK)    |  |(id, PK)  |
|equip_id |  |equip_id  |  |fault_id|  |fault_id    |  |user_id   |
|reported_|  |technician|  |analyzed|  |prepared_by |  |          |
|by       |  |_id       |  |_by     |  |            |  |          |
+----+----+  +----------+  +--------+  +------------+  +----------+
     |
     | (referenced by)
     |
     v
+-----------------+
| DOCUMENTATION   |
| PACKAGES        |
| (id, PK)        |
| fault_id        |
| engineer_id     |
+-----------------+
    """)
    
    print("\n" + "=" * 80)
    print("EQUIPMENT RELATIONSHIPS")
    print("=" * 80)
    
    print("""
    +--------------+
    |  EQUIPMENT   |
    |  (id, PK)    |
    |  code        |
    |  name        |
    |  status      |
    +------+-------+
           |
           | (referenced by)
           |
    +------+----------------------+
    |                             |
    v                             v
+---------+              +---------------+
| FAULTS  |              |  MONITORING   |
|equip_id |              |  equipment_id |
+---------+              +---------------+
    """)
    
    # Get actual relationship counts
    print("\n" + "=" * 80)
    print("RELATIONSHIP STATISTICS")
    print("=" * 80)
    
    # Users -> Faults
    cursor.execute("SELECT COUNT(*) FROM faults WHERE reported_by IS NOT NULL")
    user_faults = cursor.fetchone()[0]
    
    # Users -> Monitoring
    cursor.execute("SELECT COUNT(*) FROM daily_monitoring WHERE technician_id IS NOT NULL")
    user_monitoring = cursor.fetchone()[0]
    
    # Equipment -> Faults
    cursor.execute("SELECT COUNT(*) FROM faults WHERE equipment_id IS NOT NULL")
    equip_faults = cursor.fetchone()[0]
    
    # Equipment -> Monitoring
    cursor.execute("SELECT COUNT(*) FROM daily_monitoring WHERE equipment_id IS NOT NULL")
    equip_monitoring = cursor.fetchone()[0]
    
    # Faults -> RCA
    cursor.execute("SELECT COUNT(*) FROM root_cause_analysis WHERE fault_id IS NOT NULL")
    fault_rca = cursor.fetchone()[0]
    
    # Faults -> Reports
    cursor.execute("SELECT COUNT(*) FROM resolution_reports WHERE fault_id IS NOT NULL")
    fault_reports = cursor.fetchone()[0]
    
    print(f"\nUsers -> Faults: {user_faults} relationships")
    print(f"Users -> Monitoring: {user_monitoring} relationships")
    print(f"Equipment -> Faults: {equip_faults} relationships")
    print(f"Equipment -> Monitoring: {equip_monitoring} relationships")
    print(f"Faults -> Root Cause Analysis: {fault_rca} relationships")
    print(f"Faults -> Resolution Reports: {fault_reports} relationships")
    
    # Show complete relationship chain example
    print("\n" + "=" * 80)
    print("COMPLETE RELATIONSHIP CHAIN EXAMPLE")
    print("=" * 80)
    
    cursor.execute("""
        SELECT 
            u.username as user,
            e.equipment_code,
            e.equipment_name,
            f.id as fault_id,
            f.fault_description,
            f.severity,
            rca.id as rca_id,
            rca.root_cause,
            rr.id as report_id,
            rr.status as report_status
        FROM faults f
        LEFT JOIN users u ON f.reported_by = u.id
        LEFT JOIN equipment e ON f.equipment_id = e.id
        LEFT JOIN root_cause_analysis rca ON f.id = rca.fault_id
        LEFT JOIN resolution_reports rr ON f.id = rr.fault_id
        ORDER BY f.id DESC
        LIMIT 3
    """)
    
    chains = cursor.fetchall()
    if chains:
        print("\nExample: User -> Equipment -> Fault -> RCA -> Report")
        print("-" * 80)
        for i, chain in enumerate(chains, 1):
            print(f"\nChain {i}:")
            print(f"  User: {chain[0] or 'N/A'}")
            print(f"  Equipment: {chain[1]} - {chain[2]}")
            print(f"  Fault #{chain[3]}: {chain[4][:50] if chain[4] else 'N/A'}... (Severity: {chain[5]})")
            print(f"  RCA #{chain[6] or 'N/A'}: {chain[7][:40] if chain[7] else 'N/A'}...")
            print(f"  Report #{chain[8] or 'N/A'}: Status = {chain[9] or 'N/A'}")
    
    conn.close()
    print("\n" + "=" * 80)

if __name__ == '__main__':
    view_er_diagram()

