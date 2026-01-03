"""
Performance Report Controller (UC-04)
"""
from datetime import date
from flask import session
from app.patterns.factory import ServiceFactory

class PerformanceReportController:
    """Controller for performance report operations"""
    
    def __init__(self):
        self.report_service = ServiceFactory.create_performance_report_service()
    
    def create_draft_report(self, data: dict) -> dict:
        """Create draft performance report"""
        try:
            technician_id = session.get('user_id')
            if not technician_id:
                return {'success': False, 'message': 'Not authenticated'}
            
            report = self.report_service.create_draft_report(
                technician_id=technician_id,
                period_start=date.fromisoformat(data.get('report_period_start')),
                period_end=date.fromisoformat(data.get('report_period_end')),
                report_type=data.get('report_type', 'weekly'),
                analysis=data.get('analysis'),
                recommendations=data.get('recommendations')
            )
            
            return {
                'success': True,
                'message': 'Draft report created',
                'data': report.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def compile_report_data(self, data: dict) -> dict:
        """Compile monitoring data for report"""
        try:
            technician_id = session.get('user_id')
            if not technician_id:
                return {'success': False, 'message': 'Not authenticated'}
            
            compiled_data = self.report_service.compile_report_data(
                technician_id=technician_id,
                period_start=date.fromisoformat(data.get('period_start')),
                period_end=date.fromisoformat(data.get('period_end'))
            )
            
            return {
                'success': True,
                'data': compiled_data
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def submit_for_approval(self, report_id: int) -> dict:
        """Submit report for approval"""
        try:
            report = self.report_service.submit_for_approval(report_id)
            return {
                'success': True,
                'message': 'Report submitted for approval',
                'data': report.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def approve_report(self, report_id: int) -> dict:
        """Approve report"""
        try:
            approved_by = session.get('user_id')
            if not approved_by:
                return {'success': False, 'message': 'Not authenticated'}
            
            report = self.report_service.approve_report(report_id, approved_by)
            return {
                'success': True,
                'message': 'Report approved',
                'data': report.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_technician_reports(self) -> dict:
        """Get technician's reports"""
        try:
            technician_id = session.get('user_id')
            if not technician_id:
                return {'success': False, 'message': 'Not authenticated'}
            
            reports = self.report_service.get_technician_reports(technician_id)
            return {
                'success': True,
                'data': [r.to_dict() for r in reports]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_pending_approval(self) -> dict:
        """Get pending approval reports"""
        try:
            reports = self.report_service.get_pending_approval_reports()
            return {
                'success': True,
                'data': [r.to_dict() for r in reports]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

