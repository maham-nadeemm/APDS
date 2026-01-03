"""
Strategy Pattern Implementation
"""
from abc import ABC, abstractmethod
from typing import List
from app.models.fault import Fault
from app.models.user import User

class EscalationStrategy(ABC):
    """Abstract base class for escalation strategies"""
    
    @abstractmethod
    def should_escalate(self, fault: Fault) -> bool:
        """Determine if fault should be escalated"""
        pass
    
    @abstractmethod
    def get_target_role(self, current_role: str) -> str:
        """Get target role for escalation"""
        pass

class SeverityBasedEscalation(EscalationStrategy):
    """Escalate based on fault severity"""
    
    def should_escalate(self, fault: Fault) -> bool:
        return fault.severity in ['high', 'critical']
    
    def get_target_role(self, current_role: str) -> str:
        role_map = {
            'technician': 'engineer',
            'engineer': 'dm',
            'dm': 'dgm',
            'dgm': 'dgm'  # Cannot escalate further
        }
        return role_map.get(current_role, 'engineer')

class TimeBasedEscalation(EscalationStrategy):
    """Escalate based on time since fault reported"""
    
    def __init__(self, hours_threshold: int = 24):
        self.hours_threshold = hours_threshold
    
    def should_escalate(self, fault: Fault) -> bool:
        if not fault.reported_at:
            return False
        from datetime import datetime, timedelta
        time_diff = datetime.now() - fault.reported_at
        return time_diff > timedelta(hours=self.hours_threshold)
    
    def get_target_role(self, current_role: str) -> str:
        role_map = {
            'technician': 'engineer',
            'engineer': 'dm',
            'dm': 'dgm'
        }
        return role_map.get(current_role, 'engineer')

class NotificationStrategy(ABC):
    """Abstract base class for notification strategies"""
    
    @abstractmethod
    def send_notification(self, user_id: int, title: str, message: str, notification_type: str):
        """Send notification to user"""
        pass

class ImmediateNotificationStrategy(NotificationStrategy):
    """Send notifications immediately"""
    
    def __init__(self, notification_service):
        self.notification_service = notification_service
    
    def send_notification(self, user_id: int, title: str, message: str, notification_type: str):
        self.notification_service.create_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type
        )




