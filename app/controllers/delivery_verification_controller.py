"""
Delivery/Service Verification Controller (UC-13, UC-14)
"""
from flask import session
from datetime import datetime, date
from app.patterns.factory import ServiceFactory

class DeliveryVerificationController:
    """Controller for delivery/service verification operations"""
    
    def __init__(self):
        self.verification_service = ServiceFactory.create_delivery_verification_service()
    
    def create_verification(self, data: dict) -> dict:
        """Create delivery/service verification"""
        try:
            engineer_id = session.get('user_id')
            if not engineer_id:
                return {'success': False, 'message': 'Not authenticated'}
            
            delivery_date = None
            service_date = None
            
            if data.get('delivery_date'):
                delivery_date = date.fromisoformat(data['delivery_date'])
            if data.get('service_date'):
                service_date = date.fromisoformat(data['service_date'])
            
            verification = self.verification_service.create_verification(
                vendor_id=int(data.get('vendor_id')),
                equipment_id=int(data.get('equipment_id')),
                verification_type=data.get('verification_type'),
                engineer_id=engineer_id,
                delivery_date=delivery_date,
                service_date=service_date,
                quality_assessment=data.get('quality_assessment'),
                supporting_documents=data.get('supporting_documents')
            )
            
            return {
                'success': True,
                'message': 'Verification created successfully',
                'data': verification.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def update_verification(self, verification_id: int, data: dict) -> dict:
        """Update verification"""
        try:
            verification = self.verification_service.update_verification(
                verification_id=verification_id,
                quality_assessment=data.get('quality_assessment'),
                compliance_status=data.get('compliance_status'),
                supporting_documents=data.get('supporting_documents')
            )
            
            return {
                'success': True,
                'message': 'Verification updated successfully',
                'data': verification.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def verify(self, verification_id: int, data: dict) -> dict:
        """Verify delivery/service (by DGM)"""
        try:
            verified_by = session.get('user_id')
            if not verified_by:
                return {'success': False, 'message': 'Not authenticated'}
            
            verification = self.verification_service.verify(
                verification_id=verification_id,
                verified_by=verified_by,
                verification_status=data.get('verification_status'),
                compliance_status=data.get('compliance_status')
            )
            
            return {
                'success': True,
                'message': 'Verification completed successfully',
                'data': verification.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_verification(self, verification_id: int) -> dict:
        """Get verification by ID"""
        try:
            verification = self.verification_service.get_verification_by_id(verification_id)
            if verification:
                return {
                    'success': True,
                    'data': verification.to_dict()
                }
            return {
                'success': False,
                'message': 'Verification not found'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_verifications_by_vendor(self, vendor_id: int) -> dict:
        """Get verifications by vendor"""
        try:
            verifications = self.verification_service.get_verifications_by_vendor(vendor_id)
            return {
                'success': True,
                'data': [v.to_dict() for v in verifications]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_pending_verifications(self) -> dict:
        """Get pending verifications"""
        try:
            verifications = self.verification_service.get_pending_verifications()
            return {
                'success': True,
                'data': [v.to_dict() for v in verifications]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

