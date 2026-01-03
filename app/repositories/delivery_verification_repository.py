"""
Delivery/Service Verification Repository (UC-13, UC-14, UC-15)
"""
from app.repositories.base_repository import BaseRepository
from app.models.delivery_verification import DeliveryServiceVerification

class DeliveryVerificationRepository(BaseRepository):
    """Repository for delivery/service verification data access"""
    
    def create(self, verification: DeliveryServiceVerification) -> int:
        """Create new verification"""
        query = """
            INSERT INTO delivery_service_verification 
            (vendor_id, equipment_id, verification_type, delivery_date, service_date,
             engineer_id, dgm_id, quality_assessment, compliance_status, 
             verification_status, supporting_documents)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        delivery_date = verification.delivery_date.isoformat() if verification.delivery_date else None
        service_date = verification.service_date.isoformat() if verification.service_date else None
        
        cursor = self.execute_query(query, (
            verification.vendor_id,
            verification.equipment_id,
            verification.verification_type,
            delivery_date,
            service_date,
            verification.engineer_id,
            verification.dgm_id,
            verification.quality_assessment,
            verification.compliance_status,
            verification.verification_status,
            verification.supporting_documents
        ))
        self.commit()
        return cursor.lastrowid
    
    def find_by_id(self, verification_id: int) -> DeliveryServiceVerification:
        """Find verification by ID"""
        query = "SELECT * FROM delivery_service_verification WHERE id = ?"
        row = self.fetch_one(query, (verification_id,))
        if row:
            data = self.dict_to_row(row)
            return DeliveryServiceVerification.from_dict(data)
        return None
    
    def find_by_vendor(self, vendor_id: int) -> list:
        """Find verifications by vendor"""
        query = """
            SELECT * FROM delivery_service_verification 
            WHERE vendor_id = ? 
            ORDER BY created_at DESC
        """
        rows = self.fetch_all(query, (vendor_id,))
        return [DeliveryServiceVerification.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_pending_verification(self) -> list:
        """Find pending verifications"""
        query = """
            SELECT * FROM delivery_service_verification 
            WHERE verification_status = 'pending' 
            ORDER BY created_at DESC
        """
        rows = self.fetch_all(query)
        return [DeliveryServiceVerification.from_dict(self.dict_to_row(row)) for row in rows]
    
    def update(self, verification: DeliveryServiceVerification) -> bool:
        """Update verification"""
        query = """
            UPDATE delivery_service_verification 
            SET verification_status = ?, verified_by = ?, verified_at = ?,
                compliance_status = ?, quality_assessment = ?
            WHERE id = ?
        """
        verified_at = verification.verified_at.isoformat() if verification.verified_at else None
        self.execute_query(query, (
            verification.verification_status,
            verification.verified_by,
            verified_at,
            verification.compliance_status,
            verification.quality_assessment,
            verification.id
        ))
        self.commit()
        return True




