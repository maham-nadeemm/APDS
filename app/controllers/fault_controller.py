"""
Fault Controller
"""
from flask import session
from app.services.fault_service import FaultService
from app.patterns.factory import ServiceFactory

class FaultController:
    """Controller for fault operations"""
    
    def __init__(self):
        self.fault_service = ServiceFactory.create_fault_service()
    
    def report_fault(self, data: dict) -> dict:
        """Report a fault"""
        try:
            reported_by = session.get('user_id')
            if not reported_by:
                return {'success': False, 'message': 'Not authenticated'}
            
            fault = self.fault_service.report_fault(
                equipment_id=int(data.get('equipment_id')),
                reported_by=reported_by,
                fault_description=data.get('fault_description'),
                severity=data.get('severity', 'low')
            )
            
            return {
                'success': True,
                'message': 'Fault reported successfully',
                'data': fault.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_fault(self, fault_id: int) -> dict:
        """Get fault by ID"""
        try:
            fault = self.fault_service.get_fault_by_id(fault_id)
            if fault:
                return {
                    'success': True,
                    'data': fault.to_dict()
                }
            return {
                'success': False,
                'message': 'Fault not found'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_all_faults(self, limit: int = 100) -> dict:
        """Get all faults"""
        try:
            faults = self.fault_service.get_all_faults(limit)
            return {
                'success': True,
                'data': [fault.to_dict() for fault in faults]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_faults_by_status(self, status: str) -> dict:
        """Get faults by status"""
        try:
            faults = self.fault_service.get_faults_by_status(status)
            return {
                'success': True,
                'data': [fault.to_dict() for fault in faults]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def update_fault_status(self, fault_id: int, status: str) -> dict:
        """Update fault status"""
        try:
            # Validate status
            valid_statuses = ['reported', 'investigating', 'resolved', 'escalated']
            if status not in valid_statuses:
                return {
                    'success': False,
                    'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
                }
            
            fault = self.fault_service.update_fault_status(fault_id, status)
            return {
                'success': True,
                'message': f'Fault status updated to {status}',
                'data': fault.to_dict()
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error updating fault status: {str(e)}'
            }

