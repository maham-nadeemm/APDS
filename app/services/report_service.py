"""
Report Service
"""
from app.repositories.report_repository import ReportRepository
from app.repositories.rca_repository import RCARepository
from app.repositories.fault_repository import FaultRepository
from app.models.report import ResolutionReport
from app.models.rca import RootCauseAnalysis
from datetime import datetime

class ReportService:
    """Service for report management"""
    
    def __init__(self, report_repository: ReportRepository,
                 rca_repository: RCARepository,
                 fault_repository: FaultRepository):
        self.report_repository = report_repository
        self.rca_repository = rca_repository
        self.fault_repository = fault_repository
    
    def create_draft_report(self, fault_id: int, prepared_by: int,
                          resolution_description: str, actions_taken: str,
                          preventive_measures: str = None,
                          rca_id: int = None) -> ResolutionReport:
        """Create a draft resolution report"""
        # Validate fault exists
        fault = self.fault_repository.find_by_id(fault_id)
        if not fault:
            raise ValueError("Fault not found")
        
        # Validate RCA if provided
        if rca_id:
            rca = self.rca_repository.find_by_id(rca_id)
            if not rca:
                raise ValueError("RCA not found")
        
        report = ResolutionReport(
            fault_id=fault_id,
            rca_id=rca_id,
            prepared_by=prepared_by,
            resolution_description=resolution_description,
            actions_taken=actions_taken,
            preventive_measures=preventive_measures,
            status="draft",
            created_at=datetime.now()
        )
        
        report_id = self.report_repository.create(report)
        report.id = report_id
        return report
    
    def submit_for_approval(self, report_id: int) -> ResolutionReport:
        """Submit report for approval"""
        report = self.report_repository.find_by_id(report_id)
        if not report:
            raise ValueError("Report not found")
        
        if report.status != "draft":
            raise ValueError("Only draft reports can be submitted for approval")
        
        report.status = "pending_approval"
        self.report_repository.update(report)
        return report
    
    def approve_report(self, report_id: int, approved_by: int) -> ResolutionReport:
        """Approve a report"""
        report = self.report_repository.find_by_id(report_id)
        if not report:
            raise ValueError("Report not found")
        
        if report.status != "pending_approval":
            raise ValueError("Only pending reports can be approved")
        
        report.status = "approved"
        report.approved_by = approved_by
        report.approved_at = datetime.now()
        self.report_repository.update(report)
        
        # Mark fault as resolved
        fault = self.fault_repository.find_by_id(report.fault_id)
        if fault:
            fault.status = "resolved"
            fault.resolved_at = datetime.now()
            self.fault_repository.update(fault)
        
        return report
    
    def reject_report(self, report_id: int) -> ResolutionReport:
        """Reject a report"""
        report = self.report_repository.find_by_id(report_id)
        if not report:
            raise ValueError("Report not found")
        
        report.status = "rejected"
        self.report_repository.update(report)
        return report
    
    def get_report_by_id(self, report_id: int) -> ResolutionReport:
        """Get report by ID"""
        return self.report_repository.find_by_id(report_id)
    
    def get_reports_by_status(self, status: str) -> list:
        """Get reports by status"""
        return self.report_repository.find_by_status(status)
    
    def get_pending_approval_reports(self) -> list:
        """Get reports pending approval"""
        return self.report_repository.find_pending_approval()
    
    def get_reports_by_preparer(self, user_id: int) -> list:
        """Get reports by preparer"""
        return self.report_repository.find_by_preparer(user_id)




