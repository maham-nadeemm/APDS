"""
Equipment Model
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

@dataclass
class Equipment:
    """Equipment model"""
    id: Optional[int] = None
    equipment_code: str = ""
    equipment_name: str = ""
    equipment_type: str = ""
    location: str = ""
    status: str = "operational"  # operational, maintenance, faulty, decommissioned
    last_maintenance_date: Optional[date] = None
    next_maintenance_date: Optional[date] = None
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Equipment from dictionary"""
        return cls(
            id=data.get('id'),
            equipment_code=data.get('equipment_code', ''),
            equipment_name=data.get('equipment_name', ''),
            equipment_type=data.get('equipment_type', ''),
            location=data.get('location', ''),
            status=data.get('status', 'operational'),
            last_maintenance_date=datetime.fromisoformat(data['last_maintenance_date']).date() if data.get('last_maintenance_date') else None,
            next_maintenance_date=datetime.fromisoformat(data['next_maintenance_date']).date() if data.get('next_maintenance_date') else None,
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
    
    def to_dict(self) -> dict:
        """Convert Equipment to dictionary"""
        return {
            'id': self.id,
            'equipment_code': self.equipment_code,
            'equipment_name': self.equipment_name,
            'equipment_type': self.equipment_type,
            'location': self.location,
            'status': self.status,
            'last_maintenance_date': self.last_maintenance_date.isoformat() if self.last_maintenance_date else None,
            'next_maintenance_date': self.next_maintenance_date.isoformat() if self.next_maintenance_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }




