"""
Delivery/Service Verification Service (UC-13, UC-14)
"""
from datetime import datetime, date
from app.repositories.delivery_verification_repository import DeliveryVerificationRepository
from app.repositories.vendor_repository import VendorRepository
from app.repositories.equipment_repository import EquipmentRepository
from app.models.delivery_verification import DeliveryServiceVerification

class DeliveryVerificationService:
    """Service for delivery/service verification operations"""
    
    def __init__(self, verification_repository: DeliveryVerificationRepository,
                 vendor_repository: VendorRepository,
                 equipment_repository: EquipmentRepository):
        self.verification_repository = verification_repository
        self.vendor_repository = vendor_repository
        self.equipment_repository = equipment_repository
    
    def create_verification(self, vendor_id: int, equipment_id: int,
                           verification_type: str, engineer_id: int,
                           delivery_date: date = None, service_date: date = None,
                           quality_assessment: str = None,
                           supporting_documents: str = None) -> DeliveryServiceVerification:
        """Create delivery/service verification"""
        # Validate vendor exists
        vendor = self.vendor_repository.find_by_id(vendor_id)
        if not vendor:
            raise ValueError("Vendor not found")
        
        # Validate equipment exists
        equipment = self.equipment_repository.find_by_id(equipment_id)
        if not equipment:
            raise ValueError("Equipment not found")
        
        if verification_type not in ["delivery", "service"]:
            raise ValueError("Verification type must be 'delivery' or 'service'")
        
        if verification_type == "delivery" and not delivery_date:
            raise ValueError("Delivery date is required for delivery verification")
        
        if verification_type == "service" and not service_date:
            raise ValueError("Service date is required for service verification")
        
        verification = DeliveryServiceVerification(
            vendor_id=vendor_id,
            equipment_id=equipment_id,
            verification_type=verification_type,
            delivery_date=delivery_date,
            service_date=service_date,
            engineer_id=engineer_id,
            quality_assessment=quality_assessment,
            compliance_status="pending",
            verification_status="pending",
            supporting_documents=supporting_documents,
            created_at=datetime.now()
        )
        
        verification_id = self.verification_repository.create(verification)
        verification.id = verification_id
        return verification
    
    def update_verification(self, verification_id: int, quality_assessment: str = None,
                           compliance_status: str = None,
                           supporting_documents: str = None) -> DeliveryServiceVerification:
        """Update verification"""
        verification = self.verification_repository.find_by_id(verification_id)
        if not verification:
            raise ValueError("Verification not found")
        
        if verification.verification_status != "pending":
            raise ValueError("Cannot update verified verification")
        
        if quality_assessment is not None:
            verification.quality_assessment = quality_assessment
        if compliance_status is not None:
            if compliance_status not in ["pending", "compliant", "non_compliant", "requires_action"]:
                raise ValueError("Invalid compliance status")
            verification.compliance_status = compliance_status
        if supporting_documents is not None:
            verification.supporting_documents = supporting_documents
        
        self.verification_repository.update(verification)
        return verification
    
    def verify(self, verification_id: int, verified_by: int,
               verification_status: str, compliance_status: str = None) -> DeliveryServiceVerification:
        """Verify delivery/service (by DGM)"""
        verification = self.verification_repository.find_by_id(verification_id)
        if not verification:
            raise ValueError("Verification not found")
        
        if verification_status not in ["verified", "rejected"]:
            raise ValueError("Verification status must be 'verified' or 'rejected'")
        
        verification.verification_status = verification_status
        verification.verified_by = verified_by
        verification.verified_at = datetime.now()
        
        if compliance_status:
            verification.compliance_status = compliance_status
        
        self.verification_repository.update(verification)
        return verification
    
    def get_verification_by_id(self, verification_id: int) -> DeliveryServiceVerification:
        """Get verification by ID"""
        return self.verification_repository.find_by_id(verification_id)
    
    def get_verifications_by_vendor(self, vendor_id: int) -> list:
        """Get verifications by vendor"""
        return self.verification_repository.find_by_vendor(vendor_id)
    
    def get_pending_verifications(self) -> list:
        """Get pending verifications"""
        return self.verification_repository.find_pending_verification()




