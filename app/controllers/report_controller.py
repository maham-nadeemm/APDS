"""
Report Controller
"""
from flask import session
from app.services.report_service import ReportService
from app.patterns.factory import ServiceFactory

class ReportController:
    """Controller for report operations"""
    
    def __init__(self):
        self.report_service = ServiceFactory.create_report_service()
        self.auth_service = ServiceFactory.create_auth_service()
    
    def create_draft_report(self, data: dict) -> dict:
        """Create draft report"""
        try:
            prepared_by = session.get('user_id')
            if not prepared_by:
                return {'success': False, 'message': 'Not authenticated'}
            
            report = self.report_service.create_draft_report(
                fault_id=int(data.get('fault_id')),
                prepared_by=prepared_by,
                resolution_description=data.get('resolution_description'),
                actions_taken=data.get('actions_taken'),
                preventive_measures=data.get('preventive_measures'),
                rca_id=int(data.get('rca_id')) if data.get('rca_id') else None
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
    
    def get_report(self, report_id: int) -> dict:
        """Get report by ID"""
        try:
            report = self.report_service.get_report_by_id(report_id)
            if report:
                return {
                    'success': True,
                    'data': report.to_dict()
                }
            return {
                'success': False,
                'message': 'Report not found'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_pending_approval(self) -> dict:
        """Get reports pending approval"""
        try:
            reports = self.report_service.get_pending_approval_reports()
            return {
                'success': True,
                'data': [report.to_dict() for report in reports]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_all_pending_reports(self) -> dict:
        """Get all pending reports (both regular and performance reports)"""
        try:
            from app.controllers.performance_report_controller import PerformanceReportController
            performance_report_controller = PerformanceReportController()
            
            # Get regular reports
            regular_reports = self.get_pending_approval()
            regular_data = regular_reports.get('data', []) if regular_reports.get('success') else []
            
            # Get performance reports
            performance_reports = performance_report_controller.get_pending_approval()
            performance_data = performance_reports.get('data', []) if performance_reports.get('success') else []
            
            # Combine and format reports
            all_reports = []


            print("REGULAR DATA", regular_data)
            print("PERFORMANCE DATA", performance_data)
            
            # Add regular reports with type indicator
            for report in regular_data:
                report['report_type'] = 'resolution'
                report['type_label'] = 'Resolution Report'
                all_reports.append(report)
            # Add performance reports with type indicator
            for report in performance_data:
                report['report_type'] = 'performance'
                report['type_label'] = 'Performance Report'
                user = self.auth_service.get_user_by_id(report.get('technician_id'))
                report['prepared_by'] = user.full_name if user else 'Unknown'
                all_reports.append(report)
            
            # Sort by created_at/submitted_at (most recent first)
            all_reports.sort(key=lambda x: x.get('submitted_at') or x.get('created_at') or '', reverse=True)
            
            return {
                'success': True,
                'data': all_reports
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }




