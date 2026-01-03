"""
Data Re-verification Controller (UC-05)
"""
from flask import session
from app.patterns.factory import ServiceFactory

class DataReverificationController:
    """Controller for data re-verification operations"""
    
    def __init__(self):
        self.reverification_service = ServiceFactory.create_data_reverification_service()
    
    def create_reverification(self, data: dict) -> dict:
        """Create data re-verification"""
        try:
            technician_id = session.get('user_id')
            if not technician_id:
                return {'success': False, 'message': 'Not authenticated'}
            
            reverification = self.reverification_service.create_reverification(
                original_monitoring_id=int(data.get('original_monitoring_id')),
                technician_id=technician_id,
                new_voltage=float(data.get('new_voltage')),
                new_current=float(data.get('new_current')),
                new_power_factor=float(data.get('new_power_factor')),
                tolerance_levels=data.get('tolerance_levels')
            )
            
            return {
                'success': True,
                'message': 'Re-verification created successfully',
                'data': reverification.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def approve_reverification(self, reverification_id: int) -> dict:
        """Approve re-verification"""
        try:
            engineer_id = session.get('user_id')
            if not engineer_id:
                return {'success': False, 'message': 'Not authenticated'}
            
            reverification = self.reverification_service.approve_reverification(reverification_id, engineer_id)
            return {
                'success': True,
                'message': 'Re-verification approved',
                'data': reverification.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_reverification(self, reverification_id: int) -> dict:
        """Get re-verification by ID"""
        try:
            reverification = self.reverification_service.get_reverification_by_id(reverification_id)
            if reverification:
                return {
                    'success': True,
                    'data': reverification.to_dict()
                }
            return {
                'success': False,
                'message': 'Re-verification not found'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_technician_reverifications(self) -> dict:
        """Get technician's re-verifications"""
        try:
            technician_id = session.get('user_id')
            if not technician_id:
                return {'success': False, 'message': 'Not authenticated'}
            
            reverifications = self.reverification_service.get_technician_reverifications(technician_id)
            return {
                'success': True,
                'data': [r.to_dict() for r in reverifications]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_pending_approval(self) -> dict:
        """Get pending approval re-verifications"""
        try:
            reverifications = self.reverification_service.get_pending_approval()
            return {
                'success': True,
                'data': [r.to_dict() for r in reverifications]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

