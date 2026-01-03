"""
Monitoring Service
"""
from datetime import date
from app.repositories.monitoring_repository import MonitoringRepository
from app.repositories.equipment_repository import EquipmentRepository
from app.models.monitoring import DailyMonitoring
from app.models.equipment import Equipment

class MonitoringService:
    """Service for monitoring operations"""
    
    def __init__(self, monitoring_repository: MonitoringRepository, 
                 equipment_repository: EquipmentRepository):
        self.monitoring_repository = monitoring_repository
        self.equipment_repository = equipment_repository
    
    def create_monitoring_record(self, equipment_id: int, technician_id: int,
                                monitoring_date: date, shift: str = None,
                                voltage: float = None, current: float = None,
                                power_factor: float = None,
                                operational_status: str = "normal",
                                observations: str = None) -> DailyMonitoring:
        """Create a new monitoring record - APDS: Voltage, Current, Power Factor"""
        # Validate equipment exists
        if not equipment_id:
            raise ValueError("Equipment is required. Please select an equipment from the list.")
        
        equipment = self.equipment_repository.find_by_id(equipment_id)
        if not equipment:
            raise ValueError(f"Equipment with ID {equipment_id} not found. Please select a valid equipment from the list.")
        
        # Determine operational status based on readings (APDS thresholds)
        if operational_status == "normal":
            # Voltage: Normal range 220-240V, warning if outside
            if voltage and (voltage < 220 or voltage > 240):
                operational_status = "warning"
            # Current: Check against rated current (example: > 100A is warning)
            if current and current > 100:
                operational_status = "warning"
            # Power Factor: Should be close to 1.0, < 0.85 is critical
            if power_factor and power_factor < 0.85:
                operational_status = "critical"
            elif power_factor and power_factor < 0.90:
                operational_status = "warning"
        
        monitoring = DailyMonitoring(
            equipment_id=equipment_id,
            technician_id=technician_id,
            monitoring_date=monitoring_date,
            shift=shift,
            voltage=voltage,
            current=current,
            power_factor=power_factor,
            operational_status=operational_status,
            observations=observations
        )
        
        monitoring_id = self.monitoring_repository.create(monitoring)
        monitoring.id = monitoring_id
        
        # Update equipment status if critical
        if operational_status == "critical":
            equipment.status = "faulty"
            self.equipment_repository.update(equipment)
        
        return monitoring
    
    def get_equipment_monitoring_history(self, equipment_id: int, limit: int = 100) -> list:
        """Get monitoring history for equipment"""
        return self.monitoring_repository.find_by_equipment(equipment_id, limit)
    
    def get_technician_monitoring_history(self, technician_id: int, limit: int = 100) -> list:
        """Get monitoring history for technician"""
        return self.monitoring_repository.find_by_technician(technician_id, limit)
    
    def get_critical_monitoring_records(self) -> list:
        """Get all critical monitoring records"""
        return self.monitoring_repository.find_critical_status()
    
    def get_monitoring_by_date_range(self, start_date: date, end_date: date) -> list:
        """Get monitoring records by date range"""
        return self.monitoring_repository.find_by_date_range(start_date, end_date)
    
    def get_monitoring_record(self, monitoring_id: int) -> DailyMonitoring:
        """Get a single monitoring record by ID"""
        return self.monitoring_repository.find_by_id(monitoring_id)
    
    def update_monitoring_record(self, monitoring_id: int, equipment_id: int = None,
                                monitoring_date: date = None, shift: str = None,
                                voltage: float = None, current: float = None,
                                power_factor: float = None,
                                operational_status: str = None,
                                observations: str = None) -> DailyMonitoring:
        """Update a monitoring record"""
        monitoring = self.monitoring_repository.find_by_id(monitoring_id)
        if not monitoring:
            raise ValueError("Monitoring record not found")
        
        # Update fields if provided
        if equipment_id is not None:
            equipment = self.equipment_repository.find_by_id(equipment_id)
            if not equipment:
                raise ValueError("Equipment not found")
            monitoring.equipment_id = equipment_id
        
        if monitoring_date is not None:
            monitoring.monitoring_date = monitoring_date
        
        if shift is not None:
            monitoring.shift = shift
        
        if voltage is not None:
            monitoring.voltage = voltage
        
        if current is not None:
            monitoring.current = current
        
        if power_factor is not None:
            monitoring.power_factor = power_factor
        
        if operational_status is not None:
            monitoring.operational_status = operational_status
        else:
            # Recalculate operational status based on readings
            if monitoring.voltage and (monitoring.voltage < 220 or monitoring.voltage > 240):
                monitoring.operational_status = "warning"
            elif monitoring.current and monitoring.current > 100:
                monitoring.operational_status = "warning"
            elif monitoring.power_factor and monitoring.power_factor < 0.85:
                monitoring.operational_status = "critical"
            elif monitoring.power_factor and monitoring.power_factor < 0.90:
                monitoring.operational_status = "warning"
            else:
                monitoring.operational_status = "normal"
        
        if observations is not None:
            monitoring.observations = observations
        
        self.monitoring_repository.update(monitoring)
        
        # Update equipment status if critical
        if monitoring.operational_status == "critical":
            equipment = self.equipment_repository.find_by_id(monitoring.equipment_id)
            if equipment:
                equipment.status = "faulty"
                self.equipment_repository.update(equipment)
        
        return monitoring
    
    def delete_monitoring_record(self, monitoring_id: int) -> None:
        """Delete a monitoring record"""
        monitoring = self.monitoring_repository.find_by_id(monitoring_id)
        if not monitoring:
            raise ValueError("Monitoring record not found")
        
        self.monitoring_repository.delete(monitoring_id)

