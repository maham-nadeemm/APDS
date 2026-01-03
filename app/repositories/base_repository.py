"""
Base Repository - Repository Pattern
"""
from abc import ABC
import sqlite3
from app.database.db_connection import DatabaseConnection

class BaseRepository(ABC):
    """Base repository with common database operations"""
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.conn = self.db.get_connection()
        # Ensure foreign keys are enabled on this connection
        if self.conn:
            try:
                self.conn.execute("PRAGMA foreign_keys = ON")
            except:
                pass
    
    def execute_query(self, query: str, params: tuple = None, retries: int = 3):
        """Execute a query and return cursor with retry logic for database locks"""
        import time
        import sqlite3
        
        for attempt in range(retries):
            try:
                cursor = self.conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return cursor
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e).lower() and attempt < retries - 1:
                    # Wait with exponential backoff
                    wait_time = (2 ** attempt) * 0.1  # 0.1s, 0.2s, 0.4s
                    time.sleep(wait_time)
                    continue
                else:
                    # Log the error for debugging
                    import traceback
                    error_msg = f"Database error in execute_query: {str(e)}\nQuery: {query}\nParams: {params}\nAttempt: {attempt + 1}\n{traceback.format_exc()}"
                    print(error_msg)
                    # Try to write to debug log if possible
                    try:
                        import json
                        import os
                        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor')
                        os.makedirs(log_dir, exist_ok=True)
                        with open(os.path.join(log_dir, 'db_errors.log'), 'a', encoding='utf-8') as f:
                            f.write(f"{error_msg}\n\n")
                    except:
                        pass
                    raise
            except sqlite3.IntegrityError as e:
                # Handle foreign key constraint violations
                error_str = str(e).lower()
                if "foreign key constraint failed" in error_str or "foreign key constraint" in error_str:
                    # Extract which foreign key failed
                    if "equipment_id" in error_str or "equipment" in error_str:
                        raise ValueError("Invalid equipment selected. Please select a valid equipment from the list.")
                    elif "technician_id" in error_str or "reported_by" in error_str or "user" in error_str:
                        raise ValueError("User session expired. Please log in again.")
                    else:
                        raise ValueError("Data validation failed. Please check that all required references are valid.")
                else:
                    raise ValueError(f"Data integrity error: {str(e)}")
            except Exception as e:
                # Log the error for debugging
                import traceback
                error_msg = f"Database error in execute_query: {str(e)}\nQuery: {query}\nParams: {params}\n{traceback.format_exc()}"
                print(error_msg)
                # Try to write to debug log if possible
                try:
                    import json
                    import os
                    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor')
                    os.makedirs(log_dir, exist_ok=True)
                    with open(os.path.join(log_dir, 'db_errors.log'), 'a', encoding='utf-8') as f:
                        f.write(f"{error_msg}\n\n")
                except:
                    pass
                raise
    
    def execute_many(self, query: str, params_list: list):
        """Execute query with multiple parameter sets"""
        cursor = self.conn.cursor()
        cursor.executemany(query, params_list)
        return cursor
    
    def commit(self, retries: int = 3):
        """Commit transaction with retry logic for database locks"""
        import time
        import sqlite3
        
        for attempt in range(retries):
            try:
                if self.conn is None:
                    raise Exception("Database connection is None")
                self.conn.commit()
                return
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e).lower() and attempt < retries - 1:
                    # Wait with exponential backoff
                    wait_time = (2 ** attempt) * 0.1  # 0.1s, 0.2s, 0.4s
                    time.sleep(wait_time)
                    continue
                else:
                    # Log the error for debugging
                    import traceback
                    import os
                    error_msg = f"Database commit error: {str(e)}\nAttempt: {attempt + 1}\n{traceback.format_exc()}"
                    print(error_msg)
                    # Try to write to debug log if possible
                    try:
                        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor')
                        os.makedirs(log_dir, exist_ok=True)
                        with open(os.path.join(log_dir, 'db_errors.log'), 'a', encoding='utf-8') as f:
                            f.write(f"{error_msg}\n\n")
                    except:
                        pass
                    raise
            except Exception as e:
                # Log the error for debugging
                import traceback
                import os
                error_msg = f"Database commit error: {str(e)}\n{traceback.format_exc()}"
                print(error_msg)
                # Try to write to debug log if possible
                try:
                    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor')
                    os.makedirs(log_dir, exist_ok=True)
                    with open(os.path.join(log_dir, 'db_errors.log'), 'a', encoding='utf-8') as f:
                        f.write(f"{error_msg}\n\n")
                except:
                    pass
                raise
    
    def fetch_one(self, query: str, params: tuple = None):
        """Fetch one row"""
        cursor = self.execute_query(query, params)
        return cursor.fetchone()
    
    def fetch_all(self, query: str, params: tuple = None):
        """Fetch all rows"""
        cursor = self.execute_query(query, params)
        return cursor.fetchall()
    
    def dict_to_row(self, row):
        """Convert SQLite row to dictionary"""
        if row:
            return dict(row)
        return None
    
    def rows_to_dicts(self, rows):
        """Convert multiple rows to list of dictionaries"""
        return [dict(row) for row in rows] if rows else []

