"""
Delivery/Service Verification Model (UC-13, UC-14, UC-15)
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

@dataclass
class DeliveryServiceVerification:
    """Delivery/Service Verification model"""
    id: Optional[int] = None
    vendor_id: Optional[int] = None
    equipment_id: Optional[int] = None
    verification_type: str = "delivery"  # delivery, service
    delivery_date: Optional[date] = None
    service_date: Optional[date] = None
    engineer_id: Optional[int] = None
    dgm_id: Optional[int] = None
    quality_assessment: Optional[str] = None
    compliance_status: str = "pending"  # pending, compliant, non_compliant, requires_action
    verification_status: str = "pending"  # pending, verified, rejected
    verified_by: Optional[int] = None
    verified_at: Optional[datetime] = None
    supporting_documents: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create DeliveryServiceVerification from dictionary"""
        return cls(
            id=data.get('id'),
            vendor_id=data.get('vendor_id'),
            equipment_id=data.get('equipment_id'),
            verification_type=data.get('verification_type', 'delivery'),
            delivery_date=datetime.fromisoformat(data['delivery_date']).date() if data.get('delivery_date') else None,
            service_date=datetime.fromisoformat(data['service_date']).date() if data.get('service_date') else None,
            engineer_id=data.get('engineer_id'),
            dgm_id=data.get('dgm_id'),
            quality_assessment=data.get('quality_assessment'),
            compliance_status=data.get('compliance_status', 'pending'),
            verification_status=data.get('verification_status', 'pending'),
            verified_by=data.get('verified_by'),
            verified_at=datetime.fromisoformat(data['verified_at']) if data.get('verified_at') else None,
            supporting_documents=data.get('supporting_documents'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
    
    def to_dict(self) -> dict:
        """Convert DeliveryServiceVerification to dictionary"""
        return {
            'id': self.id,
            'vendor_id': self.vendor_id,
            'equipment_id': self.equipment_id,
            'verification_type': self.verification_type,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'service_date': self.service_date.isoformat() if self.service_date else None,
            'engineer_id': self.engineer_id,
            'dgm_id': self.dgm_id,
            'quality_assessment': self.quality_assessment,
            'compliance_status': self.compliance_status,
            'verification_status': self.verification_status,
            'verified_by': self.verified_by,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'supporting_documents': self.supporting_documents,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }




