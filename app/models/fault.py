"""
Fault Model
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Fault:
    """Fault model"""
    id: Optional[int] = None
    equipment_id: int = 0
    reported_by: int = 0
    fault_description: str = ""
    severity: str = "low"  # low, medium, high, critical
    status: str = "reported"  # reported, investigating, resolved, escalated
    reported_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Fault from dictionary"""
        return cls(
            id=data.get('id'),
            equipment_id=data.get('equipment_id', 0),
            reported_by=data.get('reported_by', 0),
            fault_description=data.get('fault_description', ''),
            severity=data.get('severity', 'low'),
            status=data.get('status', 'reported'),
            reported_at=datetime.fromisoformat(data['reported_at']) if data.get('reported_at') else None,
            resolved_at=datetime.fromisoformat(data['resolved_at']) if data.get('resolved_at') else None
        )
    
    def to_dict(self) -> dict:
        """Convert Fault to dictionary"""
        return {
            'id': self.id,
            'equipment_id': self.equipment_id,
            'reported_by': self.reported_by,
            'fault_description': self.fault_description,
            'severity': self.severity,
            'status': self.status,
            'reported_at': self.reported_at.isoformat() if self.reported_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }




