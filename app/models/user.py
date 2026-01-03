"""
User Model
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """User model representing system users"""
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    password_hash: str = ""
    role: str = ""  # technician, engineer, dm, dgm
    full_name: str = ""
    created_at: Optional[datetime] = None
    is_active: bool = True
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create User from dictionary"""
        return cls(
            id=data.get('id'),
            username=data.get('username', ''),
            email=data.get('email', ''),
            password_hash=data.get('password_hash', ''),
            role=data.get('role', ''),
            full_name=data.get('full_name', ''),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            is_active=bool(data.get('is_active', True))
        )
    
    def to_dict(self) -> dict:
        """Convert User to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }
    
    def has_permission(self, required_role: str) -> bool:
        """Check if user has required role permission"""
        role_hierarchy = {
            'technician': 1,
            'engineer': 2,
            'dm': 3,
            'dgm': 4
        }
        user_level = role_hierarchy.get(self.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        return user_level >= required_level




