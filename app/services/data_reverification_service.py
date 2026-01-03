"""
Data Re-verification Service (UC-05)
"""
from datetime import date, datetime
from app.repositories.data_reverification_repository import DataReverificationRepository
from app.repositories.monitoring_repository import MonitoringRepository
from app.models.data_reverification import DataReverification

class DataReverificationService:
    """Service for data re-verification operations"""
    
    def __init__(self, reverification_repository: DataReverificationRepository,
                 monitoring_repository: MonitoringRepository):
        self.reverification_repository = reverification_repository
        self.monitoring_repository = monitoring_repository
    
    def create_reverification(self, original_monitoring_id: int, technician_id: int,
                             new_voltage: float, new_current: float, new_power_factor: float,
                             tolerance_levels: str = None) -> DataReverification:
        """Create data re-verification"""
        # Get original monitoring record
        original = self.monitoring_repository.find_by_id(original_monitoring_id)
        if not original:
            raise ValueError("Original monitoring record not found")
        
        # Calculate variances
        variance_voltage = abs(new_voltage - original.voltage) if original.voltage and new_voltage else None
        variance_current = abs(new_current - original.current) if original.current and new_current else None
        variance_pf = abs(new_power_factor - original.power_factor) if original.power_factor and new_power_factor else None
        
        # Determine status based on variances
        status = "verified"
        comparison_results = []
        
        # Check voltage variance (default tolerance: 5V)
        voltage_tolerance = 5.0
        if variance_voltage and variance_voltage > voltage_tolerance:
            status = "discrepancy"
            comparison_results.append(f"Voltage variance {variance_voltage:.2f}V exceeds tolerance {voltage_tolerance}V")
        
        # Check current variance (default tolerance: 5A)
        current_tolerance = 5.0
        if variance_current and variance_current > current_tolerance:
            status = "discrepancy"
            comparison_results.append(f"Current variance {variance_current:.2f}A exceeds tolerance {current_tolerance}A")
        
        # Check power factor variance (default tolerance: 0.05)
        pf_tolerance = 0.05
        if variance_pf and variance_pf > pf_tolerance:
            status = "discrepancy"
            comparison_results.append(f"Power Factor variance {variance_pf:.3f} exceeds tolerance {pf_tolerance}")
        
        if status == "verified":
            comparison_results.append("All readings within acceptable tolerance levels")
        
        reverification = DataReverification(
            original_monitoring_id=original_monitoring_id,
            technician_id=technician_id,
            verification_date=date.today(),
            original_voltage=original.voltage,
            original_current=original.current,
            original_power_factor=original.power_factor,
            new_voltage=new_voltage,
            new_current=new_current,
            new_power_factor=new_power_factor,
            variance_voltage=variance_voltage,
            variance_current=variance_current,
            variance_power_factor=variance_pf,
            tolerance_levels=tolerance_levels or f"Voltage: ±{voltage_tolerance}V, Current: ±{current_tolerance}A, PF: ±{pf_tolerance}",
            comparison_results="; ".join(comparison_results),
            status=status,
            engineer_approval=False,
            created_at=datetime.now()
        )
        
        reverification_id = self.reverification_repository.create(reverification)
        reverification.id = reverification_id
        return reverification
    
    def approve_reverification(self, reverification_id: int, engineer_id: int) -> DataReverification:
        """Approve re-verification by engineer"""
        reverification = self.reverification_repository.find_by_id(reverification_id)
        if not reverification:
            raise ValueError("Re-verification not found")
        
        reverification.engineer_id = engineer_id
        reverification.engineer_approval = True
        reverification.status = "resolved"
        reverification.comparison_results += "; Engineer approved changes"
        
        self.reverification_repository.update(reverification)
        return reverification
    
    def get_reverification_by_id(self, reverification_id: int) -> DataReverification:
        """Get re-verification by ID"""
        return self.reverification_repository.find_by_id(reverification_id)
    
    def get_technician_reverifications(self, technician_id: int) -> list:
        """Get re-verifications by technician"""
        return self.reverification_repository.find_by_technician(technician_id)
    
    def get_pending_approval(self) -> list:
        """Get re-verifications pending engineer approval"""
        return self.reverification_repository.find_pending_approval()




