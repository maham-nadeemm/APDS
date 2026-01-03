"""
Escalation Repository
"""
from app.repositories.base_repository import BaseRepository
from app.models.escalation import Escalation

class EscalationRepository(BaseRepository):
    """Repository for escalation data access"""
    
    def create(self, escalation: Escalation) -> int:
        """Create new escalation"""
        query = """
            INSERT INTO escalations 
            (fault_id, escalated_from, escalated_to, escalation_reason, escalation_level, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (
            escalation.fault_id,
            escalation.escalated_from,
            escalation.escalated_to,
            escalation.escalation_reason,
            escalation.escalation_level,
            escalation.status
        ))
        self.commit()
        return cursor.lastrowid
    
    def find_by_id(self, escalation_id: int) -> Escalation:
        """Find escalation by ID"""
        query = "SELECT * FROM escalations WHERE id = ?"
        row = self.fetch_one(query, (escalation_id,))
        if row:
            data = self.dict_to_row(row)
            return Escalation.from_dict(data)
        return None
    
    def find_by_fault(self, fault_id: int) -> list:
        """Find escalations by fault"""
        query = "SELECT * FROM escalations WHERE fault_id = ? ORDER BY escalated_at DESC"
        rows = self.fetch_all(query, (fault_id,))
        return [Escalation.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_by_user(self, user_id: int) -> list:
        """Find escalations for user"""
        query = """
            SELECT * FROM escalations 
            WHERE escalated_to = ? AND status = 'pending'
            ORDER BY escalated_at DESC
        """
        rows = self.fetch_all(query, (user_id,))
        return [Escalation.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_pending(self) -> list:
        """Find pending escalations"""
        query = "SELECT * FROM escalations WHERE status = 'pending' ORDER BY escalated_at DESC"
        rows = self.fetch_all(query)
        return [Escalation.from_dict(self.dict_to_row(row)) for row in rows]
    
    def update(self, escalation: Escalation) -> bool:
        """Update escalation"""
        query = """
            UPDATE escalations 
            SET status = ?, resolved_at = ?
            WHERE id = ?
        """
        resolved_at = escalation.resolved_at.isoformat() if escalation.resolved_at else None
        self.execute_query(query, (escalation.status, resolved_at, escalation.id))
        self.commit()
        return True




