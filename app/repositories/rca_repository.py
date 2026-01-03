"""
RCA Repository
"""
from app.repositories.base_repository import BaseRepository
from app.models.rca import RootCauseAnalysis

class RCARepository(BaseRepository):
    """Repository for Root Cause Analysis data access"""
    
    def create(self, rca: RootCauseAnalysis) -> int:
        """Create new RCA"""
        query = """
            INSERT INTO root_cause_analysis (fault_id, analyzed_by, root_cause, contributing_factors)
            VALUES (?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (
            rca.fault_id,
            rca.analyzed_by,
            rca.root_cause,
            rca.contributing_factors
        ))
        self.commit()
        return cursor.lastrowid
    
    def find_by_id(self, rca_id: int) -> RootCauseAnalysis:
        """Find RCA by ID"""
        query = "SELECT * FROM root_cause_analysis WHERE id = ?"
        row = self.fetch_one(query, (rca_id,))
        if row:
            data = self.dict_to_row(row)
            return RootCauseAnalysis.from_dict(data)
        return None
    
    def find_by_fault(self, fault_id: int) -> RootCauseAnalysis:
        """Find RCA by fault ID"""
        query = "SELECT * FROM root_cause_analysis WHERE fault_id = ?"
        row = self.fetch_one(query, (fault_id,))
        if row:
            data = self.dict_to_row(row)
            return RootCauseAnalysis.from_dict(data)
        return None
    
    def find_all(self) -> list:
        """Find all RCAs"""
        query = "SELECT * FROM root_cause_analysis ORDER BY analysis_date DESC"
        rows = self.fetch_all(query)
        return [RootCauseAnalysis.from_dict(self.dict_to_row(row)) for row in rows]




