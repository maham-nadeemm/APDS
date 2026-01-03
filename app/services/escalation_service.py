"""
Escalation Service
"""
from app.repositories.escalation_repository import EscalationRepository
from app.repositories.fault_repository import FaultRepository
from app.repositories.user_repository import UserRepository
from app.models.escalation import Escalation
from app.models.fault import Fault
from app.patterns.strategy import SeverityBasedEscalation, TimeBasedEscalation
from datetime import datetime

class EscalationService:
    """Service for escalation management"""
    
    def __init__(self, escalation_repository: EscalationRepository,
                 fault_repository: FaultRepository,
                 user_repository: UserRepository):
        self.escalation_repository = escalation_repository
        self.fault_repository = fault_repository
        self.user_repository = user_repository
        self.severity_strategy = SeverityBasedEscalation()
        self.time_strategy = TimeBasedEscalation(hours_threshold=24)
    
    def escalate_fault(self, fault_id: int, escalated_from: int,
                      escalation_reason: str, strategy_type: str = "severity") -> Escalation:
        """Escalate a fault using strategy pattern"""
        fault = self.fault_repository.find_by_id(fault_id)
        if not fault:
            raise ValueError("Fault not found")
        
        # Get current user
        from_user = self.user_repository.find_by_id(escalated_from)
        if not from_user:
            raise ValueError("User not found")
        
        # Choose strategy
        if strategy_type == "severity":
            strategy = self.severity_strategy
        else:
            strategy = self.time_strategy
        
        # Determine target role
        target_role = strategy.get_target_role(from_user.role)
        
        # Find target user
        target_users = self.user_repository.find_by_role(target_role)
        if not target_users:
            raise ValueError(f"No {target_role} available for escalation")
        
        # Use first available user of target role
        target_user = target_users[0]
        
        # Get existing escalation level
        existing_escalations = self.escalation_repository.find_by_fault(fault_id)
        escalation_level = len(existing_escalations) + 1
        
        # Create escalation
        escalation = Escalation(
            fault_id=fault_id,
            escalated_from=escalated_from,
            escalated_to=target_user.id,
            escalation_reason=escalation_reason,
            escalation_level=escalation_level,
            status="pending",
            escalated_at=datetime.now()
        )
        
        escalation_id = self.escalation_repository.create(escalation)
        escalation.id = escalation_id
        
        # Update fault status
        fault.status = "escalated"
        self.fault_repository.update(fault)
        
        return escalation
    
    def get_escalation_by_id(self, escalation_id: int) -> Escalation:
        """Get escalation by ID"""
        return self.escalation_repository.find_by_id(escalation_id)
    
    def get_escalations_by_fault(self, fault_id: int) -> list:
        """Get escalations for a fault"""
        return self.escalation_repository.find_by_fault(fault_id)
    
    def get_pending_escalations_for_user(self, user_id: int) -> list:
        """Get pending escalations for user"""
        return self.escalation_repository.find_by_user(user_id)
    
    def acknowledge_escalation(self, escalation_id: int) -> Escalation:
        """Acknowledge an escalation"""
        escalation = self.escalation_repository.find_by_id(escalation_id)
        if not escalation:
            raise ValueError("Escalation not found")
        
        escalation.status = "acknowledged"
        self.escalation_repository.update(escalation)
        return escalation
    
    def resolve_escalation(self, escalation_id: int) -> Escalation:
        """Resolve an escalation"""
        escalation = self.escalation_repository.find_by_id(escalation_id)
        if not escalation:
            raise ValueError("Escalation not found")
        
        escalation.status = "resolved"
        escalation.resolved_at = datetime.now()
        self.escalation_repository.update(escalation)
        return escalation




