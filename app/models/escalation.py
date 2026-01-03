"""
Escalation Model
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Escalation:
    """Escalation model"""
    id: Optional[int] = None
    fault_id: int = 0
    escalated_from: int = 0
    escalated_to: int = 0
    escalation_reason: str = ""
    escalation_level: int = 1
    status: str = "pending"  # pending, acknowledged, resolved
    escalated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Escalation from dictionary"""
        return cls(
            id=data.get('id'),
            fault_id=data.get('fault_id', 0),
            escalated_from=data.get('escalated_from', 0),
            escalated_to=data.get('escalated_to', 0),
            escalation_reason=data.get('escalation_reason', ''),
            escalation_level=data.get('escalation_level', 1),
            status=data.get('status', 'pending'),
            escalated_at=datetime.fromisoformat(data['escalated_at']) if data.get('escalated_at') else None,
            resolved_at=datetime.fromisoformat(data['resolved_at']) if data.get('resolved_at') else None
        )
    
    def to_dict(self) -> dict:
        """Convert Escalation to dictionary"""
        return {
            'id': self.id,
            'fault_id': self.fault_id,
            'escalated_from': self.escalated_from,
            'escalated_to': self.escalated_to,
            'escalation_reason': self.escalation_reason,
            'escalation_level': self.escalation_level,
            'status': self.status,
            'escalated_at': self.escalated_at.isoformat() if self.escalated_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }




