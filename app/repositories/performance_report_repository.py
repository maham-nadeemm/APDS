"""
Performance Report Repository (UC-04)
"""
from app.repositories.base_repository import BaseRepository
from app.models.performance_report import PerformanceReport

class PerformanceReportRepository(BaseRepository):
    """Repository for performance report data access"""
    
    def create(self, report: PerformanceReport) -> int:
        """Create new performance report"""
        query = """
            INSERT INTO performance_reports 
            (technician_id, report_period_start, report_period_end, report_type, 
             analysis, recommendations, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (
            report.technician_id,
            report.report_period_start.isoformat(),
            report.report_period_end.isoformat(),
            report.report_type,
            report.analysis,
            report.recommendations,
            report.status
        ))
        self.commit()
        return cursor.lastrowid
    
    def find_by_id(self, report_id: int) -> PerformanceReport:
        """Find performance report by ID"""
        query = "SELECT * FROM performance_reports WHERE id = ?"
        row = self.fetch_one(query, (report_id,))
        if row:
            data = self.dict_to_row(row)
            return PerformanceReport.from_dict(data)
        return None
    
    def find_by_technician(self, technician_id: int) -> list:
        """Find reports by technician"""
        query = """
            SELECT * FROM performance_reports 
            WHERE technician_id = ? 
            ORDER BY created_at DESC
        """
        rows = self.fetch_all(query, (technician_id,))
        return [PerformanceReport.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_by_status(self, status: str) -> list:
        """Find reports by status"""
        query = """
            SELECT * FROM performance_reports 
            WHERE status = ? 
            ORDER BY created_at DESC
        """
        rows = self.fetch_all(query, (status,))
        return [PerformanceReport.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_pending_approval(self) -> list:
        """Find reports pending approval"""
        query = """
            SELECT * FROM performance_reports 
            WHERE status = 'submitted' 
            ORDER BY submitted_at DESC
        """
        rows = self.fetch_all(query)
        return [PerformanceReport.from_dict(self.dict_to_row(row)) for row in rows]
    
    def update(self, report: PerformanceReport) -> bool:
        """Update performance report"""
        query = """
            UPDATE performance_reports 
            SET status = ?, submitted_at = ?, approved_by = ?, approved_at = ?
            WHERE id = ?
        """
        submitted_at = report.submitted_at.isoformat() if report.submitted_at else None
        approved_at = report.approved_at.isoformat() if report.approved_at else None
        self.execute_query(query, (
            report.status,
            submitted_at,
            report.approved_by,
            approved_at,
            report.id
        ))
        self.commit()
        return True




