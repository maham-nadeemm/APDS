"""
Data Re-verification Model (UC-05)
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

@dataclass
class DataReverification:
    """Data Re-verification model"""
    id: Optional[int] = None
    original_monitoring_id: int = 0
    technician_id: int = 0
    engineer_id: Optional[int] = None
    verification_date: date = date.today()
    original_voltage: Optional[float] = None
    original_current: Optional[float] = None
    original_power_factor: Optional[float] = None
    new_voltage: Optional[float] = None
    new_current: Optional[float] = None
    new_power_factor: Optional[float] = None
    variance_voltage: Optional[float] = None
    variance_current: Optional[float] = None
    variance_power_factor: Optional[float] = None
    tolerance_levels: Optional[str] = None
    comparison_results: Optional[str] = None
    status: str = "pending"  # pending, verified, discrepancy, resolved
    engineer_approval: bool = False
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create DataReverification from dictionary"""
        return cls(
            id=data.get('id'),
            original_monitoring_id=data.get('original_monitoring_id', 0),
            technician_id=data.get('technician_id', 0),
            engineer_id=data.get('engineer_id'),
            verification_date=datetime.fromisoformat(data['verification_date']).date() if data.get('verification_date') else date.today(),
            original_voltage=data.get('original_voltage'),
            original_current=data.get('original_current'),
            original_power_factor=data.get('original_power_factor'),
            new_voltage=data.get('new_voltage'),
            new_current=data.get('new_current'),
            new_power_factor=data.get('new_power_factor'),
            variance_voltage=data.get('variance_voltage'),
            variance_current=data.get('variance_current'),
            variance_power_factor=data.get('variance_power_factor'),
            tolerance_levels=data.get('tolerance_levels'),
            comparison_results=data.get('comparison_results'),
            status=data.get('status', 'pending'),
            engineer_approval=bool(data.get('engineer_approval', False)),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
    
    def to_dict(self) -> dict:
        """Convert DataReverification to dictionary"""
        return {
            'id': self.id,
            'original_monitoring_id': self.original_monitoring_id,
            'technician_id': self.technician_id,
            'engineer_id': self.engineer_id,
            'verification_date': self.verification_date.isoformat() if isinstance(self.verification_date, date) else str(self.verification_date),
            'original_voltage': self.original_voltage,
            'original_current': self.original_current,
            'original_power_factor': self.original_power_factor,
            'new_voltage': self.new_voltage,
            'new_current': self.new_current,
            'new_power_factor': self.new_power_factor,
            'variance_voltage': self.variance_voltage,
            'variance_current': self.variance_current,
            'variance_power_factor': self.variance_power_factor,
            'tolerance_levels': self.tolerance_levels,
            'comparison_results': self.comparison_results,
            'status': self.status,
            'engineer_approval': self.engineer_approval,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }




