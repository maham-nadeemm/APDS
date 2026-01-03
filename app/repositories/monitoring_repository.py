"""
Monitoring Repository
"""
from app.repositories.base_repository import BaseRepository
from app.models.monitoring import DailyMonitoring
from datetime import date

class MonitoringRepository(BaseRepository):
    """Repository for monitoring data access"""
    
    def create(self, monitoring: DailyMonitoring) -> int:
        """Create new monitoring record"""
        try:
            query = """
                INSERT INTO daily_monitoring 
                (equipment_id, technician_id, monitoring_date, shift, voltage, current, 
                 power_factor, operational_status, observations)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor = self.execute_query(query, (
                monitoring.equipment_id,
                monitoring.technician_id,
                monitoring.monitoring_date.isoformat() if isinstance(monitoring.monitoring_date, date) else str(monitoring.monitoring_date),
                monitoring.shift,
                monitoring.voltage,
                monitoring.current,
                monitoring.power_factor,
                monitoring.operational_status,
                monitoring.observations
            ))
            monitoring_id = cursor.lastrowid
            self.commit()
            return monitoring_id
        except Exception as e:
            # Re-raise with more context
            raise Exception(f"Failed to create monitoring record: {str(e)}. Equipment ID: {monitoring.equipment_id}, Technician ID: {monitoring.technician_id}")
    
    def find_by_id(self, monitoring_id: int) -> DailyMonitoring:
        """Find monitoring record by ID"""
        query = "SELECT * FROM daily_monitoring WHERE id = ?"
        row = self.fetch_one(query, (monitoring_id,))
        if row:
            data = self.dict_to_row(row)
            return DailyMonitoring.from_dict(data)
        return None
    
    def find_by_equipment(self, equipment_id: int, limit: int = 100) -> list:
        """Find monitoring records by equipment"""
        query = """
            SELECT * FROM daily_monitoring 
            WHERE equipment_id = ? 
            ORDER BY monitoring_date DESC 
            LIMIT ?
        """
        rows = self.fetch_all(query, (equipment_id, limit))
        return [DailyMonitoring.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_by_technician(self, technician_id: int, limit: int = 100) -> list:
        """Find monitoring records by technician"""
        query = """
            SELECT * FROM daily_monitoring 
            WHERE technician_id = ? 
            ORDER BY monitoring_date DESC 
            LIMIT ?
        """
        rows = self.fetch_all(query, (technician_id, limit))
        return [DailyMonitoring.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_by_date_range(self, start_date: date, end_date: date) -> list:
        """Find monitoring records by date range"""
        query = """
            SELECT * FROM daily_monitoring 
            WHERE monitoring_date BETWEEN ? AND ?
            ORDER BY monitoring_date DESC
        """
        rows = self.fetch_all(query, (start_date.isoformat(), end_date.isoformat()))
        return [DailyMonitoring.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_critical_status(self) -> list:
        """Find monitoring records with critical status"""
        query = """
            SELECT * FROM daily_monitoring 
            WHERE operational_status = 'critical'
            ORDER BY monitoring_date DESC
        """
        rows = self.fetch_all(query)
        return [DailyMonitoring.from_dict(self.dict_to_row(row)) for row in rows]
    
    def update(self, monitoring: DailyMonitoring) -> None:
        """Update monitoring record"""
        query = """
            UPDATE daily_monitoring 
            SET equipment_id = ?, monitoring_date = ?, shift = ?, 
                voltage = ?, current = ?, power_factor = ?, 
                operational_status = ?, observations = ?
            WHERE id = ?
        """
        self.execute_query(query, (
            monitoring.equipment_id,
            monitoring.monitoring_date.isoformat() if isinstance(monitoring.monitoring_date, date) else str(monitoring.monitoring_date),
            monitoring.shift,
            monitoring.voltage,
            monitoring.current,
            monitoring.power_factor,
            monitoring.operational_status,
            monitoring.observations,
            monitoring.id
        ))
        self.commit()
    
    def delete(self, monitoring_id: int) -> None:
        """Delete monitoring record"""
        query = "DELETE FROM daily_monitoring WHERE id = ?"
        self.execute_query(query, (monitoring_id,))
        self.commit()

