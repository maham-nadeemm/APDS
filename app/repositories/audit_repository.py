"""
Audit Repository
"""
from app.repositories.base_repository import BaseRepository
from app.models.audit_log import AuditLog
import json

class AuditRepository(BaseRepository):
    """Repository for audit log data access"""
    
    def create(self, audit_log: AuditLog) -> int:
        """Create new audit log with retry logic"""
        import time
        query = """
            INSERT INTO audit_logs 
            (user_id, action, entity_type, entity_id, old_values, new_values, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        old_vals = json.dumps(audit_log.old_values) if audit_log.old_values else None
        new_vals = json.dumps(audit_log.new_values) if audit_log.new_values else None
        
        max_retries = 5
        for attempt in range(max_retries):
            try:
                cursor = self.execute_query(query, (
                    audit_log.user_id,
                    audit_log.action,
                    audit_log.entity_type,
                    audit_log.entity_id,
                    old_vals,
                    new_vals,
                    audit_log.ip_address,
                    audit_log.user_agent
                ))
                self.commit()
                return cursor.lastrowid
            except Exception as e:
                if "database is locked" in str(e).lower() and attempt < max_retries - 1:
                    # Wait with exponential backoff
                    wait_time = (2 ** attempt) * 0.05  # 0.05s, 0.1s, 0.2s, 0.4s, 0.8s
                    time.sleep(wait_time)
                    continue
                else:
                    # If it's the last attempt or a different error, raise it
                    raise
    
    def find_by_id(self, log_id: int) -> AuditLog:
        """Find audit log by ID"""
        query = "SELECT * FROM audit_logs WHERE id = ?"
        row = self.fetch_one(query, (log_id,))
        if row:
            data = self.dict_to_row(row)
            if data.get('old_values'):
                data['old_values'] = json.loads(data['old_values'])
            if data.get('new_values'):
                data['new_values'] = json.loads(data['new_values'])
            return AuditLog.from_dict(data)
        return None
    
    def find_by_user(self, user_id: int, limit: int = 100) -> list:
        """Find audit logs by user"""
        query = "SELECT * FROM audit_logs WHERE user_id = ? ORDER BY created_at DESC LIMIT ?"
        rows = self.fetch_all(query, (user_id, limit))
        logs = []
        for row in rows:
            data = self.dict_to_row(row)
            if data.get('old_values'):
                data['old_values'] = json.loads(data['old_values'])
            if data.get('new_values'):
                data['new_values'] = json.loads(data['new_values'])
            logs.append(AuditLog.from_dict(data))
        return logs
    
    def find_by_entity(self, entity_type: str, entity_id: int) -> list:
        """Find audit logs by entity"""
        query = "SELECT * FROM audit_logs WHERE entity_type = ? AND entity_id = ? ORDER BY created_at DESC"
        rows = self.fetch_all(query, (entity_type, entity_id))
        logs = []
        for row in rows:
            data = self.dict_to_row(row)
            if data.get('old_values'):
                data['old_values'] = json.loads(data['old_values'])
            if data.get('new_values'):
                data['new_values'] = json.loads(data['new_values'])
            logs.append(AuditLog.from_dict(data))
        return logs


