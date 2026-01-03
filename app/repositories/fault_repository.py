"""
Fault Repository
"""
from app.repositories.base_repository import BaseRepository
from app.models.fault import Fault

class FaultRepository(BaseRepository):
    """Repository for fault data access"""
    
    def create(self, fault: Fault) -> int:
        """Create new fault"""
        try:
            query = """
                INSERT INTO faults (equipment_id, reported_by, fault_description, severity, status, reported_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            reported_at_str = fault.reported_at.isoformat() if fault.reported_at else None
            cursor = self.execute_query(query, (
                fault.equipment_id,
                fault.reported_by,
                fault.fault_description,
                fault.severity,
                fault.status,
                reported_at_str
            ))
            fault_id = cursor.lastrowid
            self.commit()
            return fault_id
        except Exception as e:
            # Re-raise with more context
            raise Exception(f"Failed to create fault: {str(e)}. Equipment ID: {fault.equipment_id}, Reported by: {fault.reported_by}")
    
    def find_by_id(self, fault_id: int) -> Fault:
        """Find fault by ID"""
        query = "SELECT * FROM faults WHERE id = ?"
        row = self.fetch_one(query, (fault_id,))
        if row:
            data = self.dict_to_row(row)
            return Fault.from_dict(data)
        return None
    
    def find_all(self, limit: int = 100) -> list:
        """Find all faults"""
        # Check total count first
        count_query = "SELECT COUNT(*) as count FROM faults"
        count_row = self.fetch_one(count_query)
        total_count = count_row['count'] if count_row else 0
        # Use COALESCE to handle NULL reported_at values - use id as fallback for ordering
        query = "SELECT * FROM faults ORDER BY COALESCE(reported_at, datetime('1970-01-01')) DESC, id DESC LIMIT ?"
        rows = self.fetch_all(query, (limit,))
        return [Fault.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_by_status(self, status: str) -> list:
        """Find faults by status"""
        query = "SELECT * FROM faults WHERE status = ? ORDER BY reported_at DESC"
        rows = self.fetch_all(query, (status,))
        return [Fault.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_by_equipment(self, equipment_id: int) -> list:
        """Find faults by equipment"""
        query = "SELECT * FROM faults WHERE equipment_id = ? ORDER BY reported_at DESC"
        rows = self.fetch_all(query, (equipment_id,))
        return [Fault.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_by_severity(self, severity: str) -> list:
        """Find faults by severity"""
        query = "SELECT * FROM faults WHERE severity = ? ORDER BY reported_at DESC"
        rows = self.fetch_all(query, (severity,))
        return [Fault.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_unresolved(self) -> list:
        """Find unresolved faults"""
        query = "SELECT * FROM faults WHERE status != 'resolved' ORDER BY reported_at DESC"
        rows = self.fetch_all(query)
        return [Fault.from_dict(self.dict_to_row(row)) for row in rows]
    
    def update(self, fault: Fault) -> bool:
        """Update fault"""
        query = """
            UPDATE faults 
            SET status = ?, resolved_at = ?
            WHERE id = ?
        """
        resolved_at = fault.resolved_at.isoformat() if fault.resolved_at else None
        self.execute_query(query, (fault.status, resolved_at, fault.id))
        self.commit()
        return True

