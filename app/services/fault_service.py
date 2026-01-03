"""
Fault Service
"""
from app.repositories.fault_repository import FaultRepository
from app.repositories.equipment_repository import EquipmentRepository
from app.models.fault import Fault
from app.models.equipment import Equipment
from datetime import datetime

class FaultService:
    """Service for fault management"""
    
    def __init__(self, fault_repository: FaultRepository,
                 equipment_repository: EquipmentRepository):
        self.fault_repository = fault_repository
        self.equipment_repository = equipment_repository
    
    def report_fault(self, equipment_id: int, reported_by: int,
                    fault_description: str, severity: str = "low") -> Fault:
        """Report a new fault"""
        # Validate equipment exists
        equipment = self.equipment_repository.find_by_id(equipment_id)
        if not equipment:
            raise ValueError("Equipment not found")
        
        # Create fault
        reported_at = datetime.now()
        fault = Fault(
            equipment_id=equipment_id,
            reported_by=reported_by,
            fault_description=fault_description,
            severity=severity,
            status="reported",
            reported_at=reported_at
        )
        
        fault_id = self.fault_repository.create(fault)
        fault.id = fault_id
        
        # Update equipment status
        equipment.status = "faulty"
        self.equipment_repository.update(equipment)
        
        return fault
    
    def get_fault_by_id(self, fault_id: int) -> Fault:
        """Get fault by ID"""
        return self.fault_repository.find_by_id(fault_id)
    
    def get_all_faults(self, limit: int = 100) -> list:
        """Get all faults"""
        return self.fault_repository.find_all(limit)
    
    def get_faults_by_status(self, status: str) -> list:
        """Get faults by status"""
        return self.fault_repository.find_by_status(status)
    
    def get_faults_by_equipment(self, equipment_id: int) -> list:
        """Get faults by equipment"""
        return self.fault_repository.find_by_equipment(equipment_id)
    
    def get_unresolved_faults(self) -> list:
        """Get unresolved faults"""
        return self.fault_repository.find_unresolved()
    
    def update_fault_status(self, fault_id: int, status: str) -> Fault:
        """Update fault status"""
        fault = self.fault_repository.find_by_id(fault_id)
        if not fault:
            raise ValueError("Fault not found")
        
        fault.status = status
        if status == "resolved":
            fault.resolved_at = datetime.now()
            # Update equipment status back to operational
            equipment = self.equipment_repository.find_by_id(fault.equipment_id)
            if equipment:
                equipment.status = "operational"
                self.equipment_repository.update(equipment)
        
        self.fault_repository.update(fault)
        return fault

