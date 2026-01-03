"""
Technical Reference Model (UC-07)
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class TechnicalReference:
    """Technical Reference model for drawings, manuals, history"""
    id: Optional[int] = None
    equipment_id: int = 0
    engineer_id: int = 0
    reference_type: str = "drawing"  # drawing, manual, history, specification
    document_name: str = ""
    document_version: Optional[str] = None
    findings: Optional[str] = None
    relevance: Optional[str] = None
    conclusions: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create TechnicalReference from dictionary"""
        return cls(
            id=data.get('id'),
            equipment_id=data.get('equipment_id', 0),
            engineer_id=data.get('engineer_id', 0),
            reference_type=data.get('reference_type', 'drawing'),
            document_name=data.get('document_name', ''),
            document_version=data.get('document_version'),
            findings=data.get('findings'),
            relevance=data.get('relevance'),
            conclusions=data.get('conclusions'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
    
    def to_dict(self) -> dict:
        """Convert TechnicalReference to dictionary"""
        return {
            'id': self.id,
            'equipment_id': self.equipment_id,
            'engineer_id': self.engineer_id,
            'reference_type': self.reference_type,
            'document_name': self.document_name,
            'document_version': self.document_version,
            'findings': self.findings,
            'relevance': self.relevance,
            'conclusions': self.conclusions,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }




