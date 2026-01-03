"""
Performance Report Service (UC-04)
"""
from datetime import date, datetime
from app.repositories.performance_report_repository import PerformanceReportRepository
from app.repositories.monitoring_repository import MonitoringRepository
from app.models.performance_report import PerformanceReport

class PerformanceReportService:
    """Service for performance report operations"""
    
    def __init__(self, report_repository: PerformanceReportRepository,
                 monitoring_repository: MonitoringRepository):
        self.report_repository = report_repository
        self.monitoring_repository = monitoring_repository
    
    def create_draft_report(self, technician_id: int, period_start: date,
                          period_end: date, report_type: str = "weekly",
                          analysis: str = None, recommendations: str = None) -> PerformanceReport:
        """Create draft performance report"""
        report = PerformanceReport(
            technician_id=technician_id,
            report_period_start=period_start,
            report_period_end=period_end,
            report_type=report_type,
            analysis=analysis,
            recommendations=recommendations,
            status="draft",
            created_at=datetime.now()
        )
        
        report_id = self.report_repository.create(report)
        report.id = report_id
        return report
    
    def compile_report_data(self, technician_id: int, period_start: date,
                           period_end: date) -> dict:
        """Compile monitoring data for report period"""
        # Get all monitoring records for the period
        all_records = self.monitoring_repository.find_by_technician(technician_id, limit=10000)
        
        # Filter by date range
        period_records = [
            r for r in all_records
            if period_start <= r.monitoring_date <= period_end
        ]
        
        # Calculate statistics
        total_readings = len(period_records)
        normal_count = sum(1 for r in period_records if r.operational_status == 'normal')
        warning_count = sum(1 for r in period_records if r.operational_status == 'warning')
        critical_count = sum(1 for r in period_records if r.operational_status == 'critical')
        
        avg_voltage = sum(r.voltage for r in period_records if r.voltage) / len([r for r in period_records if r.voltage]) if any(r.voltage for r in period_records) else 0
        avg_current = sum(r.current for r in period_records if r.current) / len([r for r in period_records if r.current]) if any(r.current for r in period_records) else 0
        avg_pf = sum(r.power_factor for r in period_records if r.power_factor) / len([r for r in period_records if r.power_factor]) if any(r.power_factor for r in period_records) else 0
        
        return {
            'total_readings': total_readings,
            'normal_count': normal_count,
            'warning_count': warning_count,
            'critical_count': critical_count,
            'avg_voltage': round(avg_voltage, 2),
            'avg_current': round(avg_current, 2),
            'avg_power_factor': round(avg_pf, 3),
            'records': [r.to_dict() for r in period_records]
        }
    
    def submit_for_approval(self, report_id: int) -> PerformanceReport:
        """Submit report for DM approval"""
        report = self.report_repository.find_by_id(report_id)
        if not report:
            raise ValueError("Report not found")
        
        if report.status != "draft":
            raise ValueError("Only draft reports can be submitted")
        
        report.status = "submitted"
        report.submitted_at = datetime.now()
        self.report_repository.update(report)
        return report
    
    def approve_report(self, report_id: int, approved_by: int) -> PerformanceReport:
        """Approve performance report"""
        report = self.report_repository.find_by_id(report_id)
        if not report:
            raise ValueError("Report not found")
        
        if report.status != "submitted":
            raise ValueError("Only submitted reports can be approved")
        
        report.status = "approved"
        report.approved_by = approved_by
        report.approved_at = datetime.now()
        self.report_repository.update(report)
        return report
    
    def get_report_by_id(self, report_id: int) -> PerformanceReport:
        """Get report by ID"""
        return self.report_repository.find_by_id(report_id)
    
    def get_technician_reports(self, technician_id: int) -> list:
        """Get all reports by technician"""
        return self.report_repository.find_by_technician(technician_id)
    
    def get_pending_approval_reports(self) -> list:
        """Get reports pending approval"""
        return self.report_repository.find_pending_approval()




