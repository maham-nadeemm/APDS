"""
Vendor Model (UC-15)
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Vendor:
    """Vendor model"""
    id: Optional[int] = None
    vendor_name: str = ""
    contact_info: Optional[str] = None
    material_list: Optional[str] = None
    vendor_code: str = ""
    is_active: bool = True
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Vendor from dictionary"""
        return cls(
            id=data.get('id'),
            vendor_name=data.get('vendor_name', ''),
            contact_info=data.get('contact_info'),
            material_list=data.get('material_list'),
            vendor_code=data.get('vendor_code', ''),
            is_active=bool(data.get('is_active', True)),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
    
    def to_dict(self) -> dict:
        """Convert Vendor to dictionary"""
        return {
            'id': self.id,
            'vendor_name': self.vendor_name,
            'contact_info': self.contact_info,
            'material_list': self.material_list,
            'vendor_code': self.vendor_code,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }




