"""
Data Re-verification Repository (UC-05)
"""
from app.repositories.base_repository import BaseRepository
from app.models.data_reverification import DataReverification

class DataReverificationRepository(BaseRepository):
    """Repository for data re-verification access"""
    
    def create(self, reverification: DataReverification) -> int:
        """Create new re-verification"""
        query = """
            INSERT INTO data_reverification 
            (original_monitoring_id, technician_id, engineer_id, verification_date,
             original_voltage, original_current, original_power_factor,
             new_voltage, new_current, new_power_factor,
             variance_voltage, variance_current, variance_power_factor,
             tolerance_levels, comparison_results, status, engineer_approval)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (
            reverification.original_monitoring_id,
            reverification.technician_id,
            reverification.engineer_id,
            reverification.verification_date.isoformat(),
            reverification.original_voltage,
            reverification.original_current,
            reverification.original_power_factor,
            reverification.new_voltage,
            reverification.new_current,
            reverification.new_power_factor,
            reverification.variance_voltage,
            reverification.variance_current,
            reverification.variance_power_factor,
            reverification.tolerance_levels,
            reverification.comparison_results,
            reverification.status,
            1 if reverification.engineer_approval else 0
        ))
        self.commit()
        return cursor.lastrowid
    
    def find_by_id(self, reverification_id: int) -> DataReverification:
        """Find re-verification by ID"""
        query = "SELECT * FROM data_reverification WHERE id = ?"
        row = self.fetch_one(query, (reverification_id,))
        if row:
            data = self.dict_to_row(row)
            return DataReverification.from_dict(data)
        return None
    
    def find_by_technician(self, technician_id: int) -> list:
        """Find re-verifications by technician"""
        query = """
            SELECT * FROM data_reverification 
            WHERE technician_id = ? 
            ORDER BY verification_date DESC
        """
        rows = self.fetch_all(query, (technician_id,))
        return [DataReverification.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_pending_approval(self) -> list:
        """Find re-verifications pending engineer approval"""
        query = """
            SELECT * FROM data_reverification 
            WHERE status = 'pending' OR (status = 'discrepancy' AND engineer_approval = 0)
            ORDER BY verification_date DESC
        """
        rows = self.fetch_all(query)
        return [DataReverification.from_dict(self.dict_to_row(row)) for row in rows]
    
    def update(self, reverification: DataReverification) -> bool:
        """Update re-verification"""
        query = """
            UPDATE data_reverification 
            SET status = ?, engineer_approval = ?, comparison_results = ?
            WHERE id = ?
        """
        self.execute_query(query, (
            reverification.status,
            1 if reverification.engineer_approval else 0,
            reverification.comparison_results,
            reverification.id
        ))
        self.commit()
        return True




