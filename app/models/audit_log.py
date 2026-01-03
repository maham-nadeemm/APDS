"""
Audit Log Model
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class AuditLog:
    """Audit Log model"""
    id: Optional[int] = None
    user_id: Optional[int] = None
    action: str = ""
    entity_type: str = ""
    entity_id: Optional[int] = None
    old_values: Optional[str] = None
    new_values: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create AuditLog from dictionary"""
        return cls(
            id=data.get('id'),
            user_id=data.get('user_id'),
            action=data.get('action', ''),
            entity_type=data.get('entity_type', ''),
            entity_id=data.get('entity_id'),
            old_values=data.get('old_values'),
            new_values=data.get('new_values'),
            ip_address=data.get('ip_address'),
            user_agent=data.get('user_agent'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
    
    def to_dict(self) -> dict:
        """Convert AuditLog to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'old_values': self.old_values,
            'new_values': self.new_values,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }




