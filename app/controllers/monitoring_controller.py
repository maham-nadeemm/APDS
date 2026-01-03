"""
Monitoring Controller
"""
from datetime import date
from flask import session
from app.services.monitoring_service import MonitoringService
from app.patterns.factory import ServiceFactory

class MonitoringController:
    """Controller for monitoring operations"""
    
    def __init__(self):
        self.monitoring_service = ServiceFactory.create_monitoring_service()
    
    def create_monitoring(self, data: dict) -> dict:
        """Create monitoring record"""
        try:
            technician_id = session.get('user_id')
            if not technician_id:
                return {'success': False, 'message': 'Not authenticated. Please log in again.'}
            
            # Validate required fields
            if not data.get('equipment_id'):
                return {'success': False, 'message': 'Please select an equipment from the list.'}
            if not data.get('monitoring_date'):
                return {'success': False, 'message': 'Monitoring date is required.'}
            if not data.get('voltage') and data.get('voltage') != 0:
                return {'success': False, 'message': 'Voltage reading is required.'}
            if not data.get('current') and data.get('current') != 0:
                return {'success': False, 'message': 'Current reading is required.'}
            if not data.get('power_factor') and data.get('power_factor') != 0:
                return {'success': False, 'message': 'Power factor reading is required.'}
            
            monitoring = self.monitoring_service.create_monitoring_record(
                equipment_id=int(data.get('equipment_id')),
                technician_id=technician_id,
                monitoring_date=date.fromisoformat(data.get('monitoring_date')),
                shift=data.get('shift'),
                voltage=float(data.get('voltage')) if data.get('voltage') else None,
                current=float(data.get('current')) if data.get('current') else None,
                power_factor=float(data.get('power_factor')) if data.get('power_factor') else None,
                operational_status=data.get('operational_status', 'normal'),
                observations=data.get('observations')
            )
            
            return {
                'success': True,
                'message': 'Monitoring record created successfully',
                'data': monitoring.to_dict()
            }
        except ValueError as e:
            # User-friendly error messages
            return {
                'success': False,
                'message': str(e)
            }
        except Exception as e:
            # Generic error handling
            error_msg = str(e)
            if "foreign key" in error_msg.lower():
                if "equipment" in error_msg.lower():
                    error_msg = "Invalid equipment selected. Please select a valid equipment from the list."
                elif "user" in error_msg.lower() or "technician" in error_msg.lower():
                    error_msg = "Session expired. Please log in again."
                else:
                    error_msg = "Data validation failed. Please check all fields are correct."
            return {
                'success': False,
                'message': error_msg
            }
    
    def get_equipment_history(self, equipment_id: int, limit: int = 100) -> dict:
        """Get equipment monitoring history"""
        try:
            records = self.monitoring_service.get_equipment_monitoring_history(equipment_id, limit)
            return {
                'success': True,
                'data': [record.to_dict() for record in records]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_technician_history(self, limit: int = 100) -> dict:
        """Get technician monitoring history"""
        try:
            technician_id = session.get('user_id')
            if not technician_id:
                return {'success': False, 'message': 'Not authenticated'}
            
            records = self.monitoring_service.get_technician_monitoring_history(technician_id, limit)
            return {
                'success': True,
                'data': [record.to_dict() for record in records]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_critical_records(self) -> dict:
        """Get critical monitoring records"""
        try:
            records = self.monitoring_service.get_critical_monitoring_records()
            return {
                'success': True,
                'data': [record.to_dict() for record in records]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_monitoring(self, monitoring_id: int) -> dict:
        """Get a single monitoring record"""
        try:
            record = self.monitoring_service.get_monitoring_record(monitoring_id)
            if not record:
                return {'success': False, 'message': 'Monitoring record not found'}
            return {
                'success': True,
                'data': record.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def update_monitoring(self, monitoring_id: int, data: dict) -> dict:
        """Update monitoring record"""
        try:
            technician_id = session.get('user_id')
            if not technician_id:
                return {'success': False, 'message': 'Not authenticated. Please log in again.'}
            
            # Validate required fields
            if not data.get('equipment_id'):
                return {'success': False, 'message': 'Equipment is required'}
            if not data.get('monitoring_date'):
                return {'success': False, 'message': 'Monitoring date is required'}
            
            monitoring = self.monitoring_service.update_monitoring_record(
                monitoring_id=monitoring_id,
                equipment_id=int(data.get('equipment_id')),
                monitoring_date=date.fromisoformat(data.get('monitoring_date')),
                shift=data.get('shift'),
                voltage=float(data.get('voltage')) if data.get('voltage') else None,
                current=float(data.get('current')) if data.get('current') else None,
                power_factor=float(data.get('power_factor')) if data.get('power_factor') else None,
                operational_status=data.get('operational_status'),
                observations=data.get('observations')
            )
            
            return {
                'success': True,
                'message': 'Monitoring record updated successfully',
                'data': monitoring.to_dict()
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }
        except Exception as e:
            error_msg = str(e)
            if "foreign key" in error_msg.lower():
                if "equipment" in error_msg.lower():
                    error_msg = "Invalid equipment selected. Please select a valid equipment."
                else:
                    error_msg = "Data validation failed. Please check all fields."
            return {
                'success': False,
                'message': error_msg
            }
    
    def delete_monitoring(self, monitoring_id: int) -> dict:
        """Delete monitoring record"""
        try:
            technician_id = session.get('user_id')
            if not technician_id:
                return {'success': False, 'message': 'Not authenticated. Please log in again.'}
            
            self.monitoring_service.delete_monitoring_record(monitoring_id)
            return {
                'success': True,
                'message': 'Monitoring record deleted successfully'
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }
        except Exception as e:
            error_msg = str(e)
            if "foreign key" in error_msg.lower():
                error_msg = "Cannot delete this record because it is referenced by other data."
            return {
                'success': False,
                'message': error_msg
            }

