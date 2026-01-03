"""
Report Repository
"""
from app.repositories.base_repository import BaseRepository
from app.models.report import ResolutionReport

class ReportRepository(BaseRepository):
    """Repository for resolution report data access"""
    
    def create(self, report: ResolutionReport) -> int:
        """Create new report"""
        query = """
            INSERT INTO resolution_reports 
            (fault_id, rca_id, prepared_by, resolution_description, actions_taken, 
             preventive_measures, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (
            report.fault_id,
            report.rca_id,
            report.prepared_by,
            report.resolution_description,
            report.actions_taken,
            report.preventive_measures,
            report.status
        ))
        self.commit()
        return cursor.lastrowid
    
    def find_by_id(self, report_id: int) -> ResolutionReport:
        """Find report by ID"""
        query = "SELECT * FROM resolution_reports WHERE id = ?"
        row = self.fetch_one(query, (report_id,))
        if row:
            data = self.dict_to_row(row)
            return ResolutionReport.from_dict(data)
        return None
    
    def find_by_fault(self, fault_id: int) -> ResolutionReport:
        """Find report by fault ID"""
        query = "SELECT * FROM resolution_reports WHERE fault_id = ?"
        row = self.fetch_one(query, (fault_id,))
        if row:
            data = self.dict_to_row(row)
            return ResolutionReport.from_dict(data)
        return None
    
    def find_by_status(self, status: str) -> list:
        """Find reports by status"""
        query = "SELECT * FROM resolution_reports WHERE status = ? ORDER BY created_at DESC"
        rows = self.fetch_all(query, (status,))
        return [ResolutionReport.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_by_preparer(self, user_id: int) -> list:
        """Find reports by preparer"""
        query = "SELECT * FROM resolution_reports WHERE prepared_by = ? ORDER BY created_at DESC"
        rows = self.fetch_all(query, (user_id,))
        return [ResolutionReport.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_pending_approval(self) -> list:
        """Find reports pending approval"""
        query = "SELECT * FROM resolution_reports WHERE status = 'pending_approval' ORDER BY created_at DESC"
        rows = self.fetch_all(query)
        return [ResolutionReport.from_dict(self.dict_to_row(row)) for row in rows]
    
    def update(self, report: ResolutionReport) -> bool:
        """Update report"""
        query = """
            UPDATE resolution_reports 
            SET status = ?, approved_by = ?, approved_at = ?
            WHERE id = ?
        """
        approved_at = report.approved_at.isoformat() if report.approved_at else None
        self.execute_query(query, (
            report.status,
            report.approved_by,
            approved_at,
            report.id
        ))
        self.commit()
        return True
