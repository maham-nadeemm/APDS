"""
Database Connection Singleton Pattern
"""
import sqlite3
import os
import time
from typing import Optional

class DatabaseConnection:
    """
    Singleton pattern for database connection management
    Ensures only one database connection instance exists
    """
    _instance: Optional['DatabaseConnection'] = None
    _connection: Optional[sqlite3.Connection] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._connection is None:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'operations_monitoring.db')

            # Check if database file exists and is accessible
            if os.path.exists(db_path):
                # Check if file is locked by another process
                if not self._check_database_accessible(db_path):
                    print("=" * 80)
                    print("WARNING: Database file appears to be locked by another process!")
                    print("=" * 80)
                    print("Please close any of the following that might be using the database:")
                    print("  - DB Browser for SQLite")
                    print("  - Another instance of this application")
                    print("  - Any other SQLite tools")
                    print("=" * 80)
                    print("Attempting to connect with retry logic...")
                    print("")

            # Add timeout to handle database locks (30 seconds)
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    self._connection = sqlite3.connect(db_path, check_same_thread=False, timeout=30.0)
                    self._connection.row_factory = sqlite3.Row
                    break
                except sqlite3.OperationalError as e:
                    if "database is locked" in str(e).lower() and attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 0.5  # 0.5s, 1s, 1.5s
                        print(f"Database locked, retrying in {wait_time} seconds... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise

            # Set busy timeout FIRST before any other operations
            try:
                self._connection.execute("PRAGMA busy_timeout = 30000")
            except sqlite3.OperationalError:
                pass  # If database is locked, continue anyway

            # Enable WAL mode for better concurrency (with error handling)
            try:
                self._connection.execute("PRAGMA journal_mode = WAL")
                self._connection.commit()
            except sqlite3.OperationalError as e:
                # If database is locked, try to continue with default journal mode
                if "database is locked" in str(e).lower():
                    print(f"Warning: Could not set WAL mode (database may be locked): {e}")
                    print("Continuing with default journal mode...")
                # Try to get current journal mode
                try:
                    result = self._connection.execute("PRAGMA journal_mode").fetchone()
                    if result:
                        print(f"Current journal mode: {result[0]}")
                except:
                    pass

            # Enable foreign key constraints
            try:
                self._connection.execute("PRAGMA foreign_keys = ON")
            except sqlite3.OperationalError:
                pass  # Continue even if this fails

            # Create tables (with error handling)
            try:
                self._create_tables()
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e).lower():
                    print(f"Warning: Database is locked during table creation. Some tables may not be created.")
                    print("Please close any other applications using the database and restart the application.")
                else:
                    raise

    def _check_database_accessible(self, db_path: str) -> bool:
        """Check if database file is accessible (not locked)"""
        try:
            # Try to open the file in append mode to check if it's locked
            test_conn = sqlite3.connect(db_path, timeout=1.0)
            test_conn.close()
            return True
        except sqlite3.OperationalError:
            return False
        except Exception:
            return True  # If it's a different error, assume it's accessible

    def _create_tables(self):
        """Create all database tables"""
        cursor = self._connection.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('technician', 'engineer', 'dm', 'dgm', 'vendor')),
                full_name TEXT NOT NULL,
                department TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        """)

        # Equipment table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipment_code TEXT UNIQUE NOT NULL,
                equipment_name TEXT NOT NULL,
                equipment_type TEXT NOT NULL,
                location TEXT NOT NULL,
                status TEXT DEFAULT 'operational' CHECK(status IN ('operational', 'maintenance', 'faulty', 'decommissioned')),
                last_maintenance_date DATE,
                next_maintenance_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Daily Monitoring table (APDS: Voltage, Current, Power Factor)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS daily_monitoring (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipment_id INTEGER NULL,
                technician_id INTEGER NULL,
                monitoring_date DATE NOT NULL,
                shift TEXT CHECK(shift IN ('morning', 'afternoon', 'night')),
                voltage REAL,
                current REAL,
                power_factor REAL,
                operational_status TEXT NOT NULL CHECK(operational_status IN ('normal', 'warning', 'critical')),
                observations TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (equipment_id) REFERENCES equipment(id),
                FOREIGN KEY (technician_id) REFERENCES users(id)
            )
        """
        )

        # Faults table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faults (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipment_id INTEGER NOT NULL,
                reported_by INTEGER NOT NULL,
                fault_description TEXT NOT NULL,
                severity TEXT NOT NULL CHECK(severity IN ('low', 'medium', 'high', 'critical')),
                status TEXT DEFAULT 'reported' CHECK(status IN ('reported', 'investigating', 'resolved', 'escalated')),
                reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP,
                FOREIGN KEY (equipment_id) REFERENCES equipment(id),
                FOREIGN KEY (reported_by) REFERENCES users(id)
            )
        """)

        # Root Cause Analysis table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS root_cause_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fault_id INTEGER NOT NULL,
                analyzed_by INTEGER NOT NULL,
                root_cause TEXT NOT NULL,
                contributing_factors TEXT,
                analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (fault_id) REFERENCES faults(id),
                FOREIGN KEY (analyzed_by) REFERENCES users(id)
            )
        """)

        # Resolution Reports table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resolution_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fault_id INTEGER NOT NULL,
                rca_id INTEGER,
                prepared_by INTEGER NOT NULL,
                resolution_description TEXT NOT NULL,
                actions_taken TEXT NOT NULL,
                preventive_measures TEXT,
                status TEXT DEFAULT 'draft' CHECK(status IN ('draft', 'pending_approval', 'approved', 'rejected')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                approved_by INTEGER,
                approved_at TIMESTAMP,
                FOREIGN KEY (fault_id) REFERENCES faults(id),
                FOREIGN KEY (rca_id) REFERENCES root_cause_analysis(id),
                FOREIGN KEY (prepared_by) REFERENCES users(id),
                FOREIGN KEY (approved_by) REFERENCES users(id)
            )
        """)

        # Notifications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                notification_type TEXT NOT NULL CHECK(notification_type IN ('info', 'warning', 'error', 'success', 'escalation')),
                is_read INTEGER DEFAULT 0,
                related_entity_type TEXT,
                related_entity_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Escalations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS escalations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fault_id INTEGER NOT NULL,
                escalated_from INTEGER NOT NULL,
                escalated_to INTEGER NOT NULL,
                escalation_reason TEXT NOT NULL,
                escalation_level INTEGER DEFAULT 1,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'acknowledged', 'resolved')),
                escalated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP,
                FOREIGN KEY (fault_id) REFERENCES faults(id),
                FOREIGN KEY (escalated_from) REFERENCES users(id),
                FOREIGN KEY (escalated_to) REFERENCES users(id)
            )
        """)

        # Performance Reports table (UC-04)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                technician_id INTEGER NOT NULL,
                report_period_start DATE NOT NULL,
                report_period_end DATE NOT NULL,
                report_type TEXT CHECK(report_type IN ('weekly', 'monthly', 'custom')),
                analysis TEXT,
                recommendations TEXT,
                status TEXT DEFAULT 'draft' CHECK(status IN ('draft', 'submitted', 'approved', 'rejected')),
                submitted_at TIMESTAMP,
                approved_by INTEGER,
                approved_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (technician_id) REFERENCES users(id),
                FOREIGN KEY (approved_by) REFERENCES users(id)
            )
        """)

        # Technical References table (UC-07)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS technical_references (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipment_id INTEGER NOT NULL,
                engineer_id INTEGER NOT NULL,
                reference_type TEXT CHECK(reference_type IN ('drawing', 'manual', 'history', 'specification')),
                document_name TEXT NOT NULL,
                document_version TEXT,
                findings TEXT,
                relevance TEXT,
                conclusions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (equipment_id) REFERENCES equipment(id),
                FOREIGN KEY (engineer_id) REFERENCES users(id)
            )
        """)

        # Documentation Packages table (UC-09, UC-10)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documentation_packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fault_id INTEGER NOT NULL,
                engineer_id INTEGER NOT NULL,
                package_name TEXT NOT NULL,
                documentation_type TEXT,
                status TEXT DEFAULT 'in_progress' CHECK(status IN ('in_progress', 'completed', 'submitted', 'approved')),
                completion_date TIMESTAMP,
                submitted_at TIMESTAMP,
                approved_by INTEGER,
                approved_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (fault_id) REFERENCES faults(id),
                FOREIGN KEY (engineer_id) REFERENCES users(id),
                FOREIGN KEY (approved_by) REFERENCES users(id)
            )
        """)

        # Documentation Items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documentation_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                package_id INTEGER NOT NULL,
                document_name TEXT NOT NULL,
                document_type TEXT,
                content TEXT,
                version TEXT,
                status TEXT DEFAULT 'draft' CHECK(status IN ('draft', 'completed', 'approved')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (package_id) REFERENCES documentation_packages(id)
            )
        """)

        # Vendors table (UC-15)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vendor_name TEXT NOT NULL,
                contact_info TEXT,
                material_list TEXT,
                vendor_code TEXT UNIQUE,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Delivery/Service Verification table (UC-13, UC-14, UC-15)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS delivery_service_verification (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vendor_id INTEGER,
                equipment_id INTEGER,
                verification_type TEXT CHECK(verification_type IN ('delivery', 'service')),
                delivery_date DATE,
                service_date DATE,
                engineer_id INTEGER,
                dgm_id INTEGER,
                quality_assessment TEXT,
                compliance_status TEXT CHECK(compliance_status IN ('pending', 'compliant', 'non_compliant', 'requires_action')),
                verification_status TEXT DEFAULT 'pending' CHECK(verification_status IN ('pending', 'verified', 'rejected')),
                verified_by INTEGER,
                verified_at TIMESTAMP,
                supporting_documents TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vendor_id) REFERENCES vendors(id),
                FOREIGN KEY (equipment_id) REFERENCES equipment(id),
                FOREIGN KEY (engineer_id) REFERENCES users(id),
                FOREIGN KEY (dgm_id) REFERENCES users(id),
                FOREIGN KEY (verified_by) REFERENCES users(id)
            )
        """)

        # Data Re-verification table (UC-05)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_reverification (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_monitoring_id INTEGER NOT NULL,
                technician_id INTEGER NOT NULL,
                engineer_id INTEGER,
                verification_date DATE NOT NULL,
                original_voltage REAL,
                original_current REAL,
                original_power_factor REAL,
                new_voltage REAL,
                new_current REAL,
                new_power_factor REAL,
                variance_voltage REAL,
                variance_current REAL,
                variance_power_factor REAL,
                tolerance_levels TEXT,
                comparison_results TEXT,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'verified', 'discrepancy', 'resolved')),
                engineer_approval INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (original_monitoring_id) REFERENCES daily_monitoring(id),
                FOREIGN KEY (technician_id) REFERENCES users(id),
                FOREIGN KEY (engineer_id) REFERENCES users(id)
            )
        """)

        # Audit Log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                entity_id INTEGER,
                old_values TEXT,
                new_values TEXT,
                ip_address TEXT,
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        try:
            self._connection.commit()
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e).lower():
                print(f"Warning: Could not commit table creation (database is locked): {e}")
                # Try to commit again after a short delay
                import time
                time.sleep(0.1)
                try:
                    self._connection.commit()
                except:
                    pass
            else:
                raise

    def get_connection(self):
        """Get database connection"""
        return self._connection

    def init_app(self, app):
        """Initialize with Flask app"""
        pass

    def close(self):
        """Close database connection"""
        if self._connection:
            self._connection.close()
            self._connection = None
