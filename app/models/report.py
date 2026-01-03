"""
Resolution Report Model
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ResolutionReport:
    """Resolution Report model"""
    id: Optional[int] = None
    fault_id: int = 0
    rca_id: Optional[int] = None
    prepared_by: int = 0
    resolution_description: str = ""
    actions_taken: str = ""
    preventive_measures: Optional[str] = None
    status: str = "draft"  # draft, pending_approval, approved, rejected
    created_at: Optional[datetime] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create ResolutionReport from dictionary"""
        return cls(
            id=data.get('id'),
            fault_id=data.get('fault_id', 0),
            rca_id=data.get('rca_id'),
            prepared_by=data.get('prepared_by', 0),
            resolution_description=data.get('resolution_description', ''),
            actions_taken=data.get('actions_taken', ''),
            preventive_measures=data.get('preventive_measures'),
            status=data.get('status', 'draft'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            approved_by=data.get('approved_by'),
            approved_at=datetime.fromisoformat(data['approved_at']) if data.get('approved_at') else None
        )
    
    def to_dict(self) -> dict:
        """Convert ResolutionReport to dictionary"""
        return {
            'id': self.id,
            'fault_id': self.fault_id,
            'rca_id': self.rca_id,
            'prepared_by': self.prepared_by,
            'resolution_description': self.resolution_description,
            'actions_taken': self.actions_taken,
            'preventive_measures': self.preventive_measures,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None
        }




