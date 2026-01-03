"""
Notification Model
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Notification:
    """Notification model"""
    id: Optional[int] = None
    user_id: int = 0
    title: str = ""
    message: str = ""
    notification_type: str = "info"  # info, warning, error, success, escalation
    is_read: bool = False
    related_entity_type: Optional[str] = None
    related_entity_id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Notification from dictionary"""
        return cls(
            id=data.get('id'),
            user_id=data.get('user_id', 0),
            title=data.get('title', ''),
            message=data.get('message', ''),
            notification_type=data.get('notification_type', 'info'),
            is_read=bool(data.get('is_read', False)),
            related_entity_type=data.get('related_entity_type'),
            related_entity_id=data.get('related_entity_id'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
    
    def to_dict(self) -> dict:
        """Convert Notification to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'notification_type': self.notification_type,
            'is_read': self.is_read,
            'related_entity_type': self.related_entity_type,
            'related_entity_id': self.related_entity_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }




