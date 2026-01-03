"""
Daily Monitoring Model
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

@dataclass
class DailyMonitoring:
    """Daily monitoring data model - APDS: Voltage, Current, Power Factor"""
    id: Optional[int] = None
    equipment_id: int = 0
    technician_id: int = 0
    monitoring_date: date = date.today()
    shift: Optional[str] = None  # morning, afternoon, night
    voltage: Optional[float] = None  # Voltage in Volts
    current: Optional[float] = None  # Current in Amperes
    power_factor: Optional[float] = None  # Power Factor (0-1)
    operational_status: str = "normal"  # normal, warning, critical
    observations: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create DailyMonitoring from dictionary"""
        return cls(
            id=data.get('id'),
            equipment_id=data.get('equipment_id', 0),
            technician_id=data.get('technician_id', 0),
            monitoring_date=datetime.fromisoformat(data['monitoring_date']).date() if data.get('monitoring_date') else date.today(),
            shift=data.get('shift'),
            voltage=data.get('voltage'),
            current=data.get('current'),
            power_factor=data.get('power_factor'),
            operational_status=data.get('operational_status', 'normal'),
            observations=data.get('observations'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
    
    def to_dict(self) -> dict:
        """Convert DailyMonitoring to dictionary"""
        return {
            'id': self.id,
            'equipment_id': self.equipment_id,
            'technician_id': self.technician_id,
            'monitoring_date': self.monitoring_date.isoformat() if isinstance(self.monitoring_date, date) else str(self.monitoring_date),
            'shift': self.shift,
            'voltage': self.voltage,
            'current': self.current,
            'power_factor': self.power_factor,
            'operational_status': self.operational_status,
            'observations': self.observations,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

