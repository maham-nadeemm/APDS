"""
Observer Pattern Implementation
"""
from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    """Abstract observer interface"""
    
    @abstractmethod
    def update(self, event_type: str, data: dict):
        """Update observer with event data"""
        pass

class Subject:
    """Subject that notifies observers"""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        """Attach an observer"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        """Detach an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event_type: str, data: dict):
        """Notify all observers"""
        for observer in self._observers:
            observer.update(event_type, data)

class NotificationObserver(Observer):
    """Observer that handles notifications"""
    
    def __init__(self, notification_service):
        self.notification_service = notification_service
    
    def update(self, event_type: str, data: dict):
        """Handle notification events"""
        if event_type == 'fault_reported':
            self._handle_fault_reported(data)
        elif event_type == 'fault_escalated':
            self._handle_fault_escalated(data)
        elif event_type == 'report_pending_approval':
            self._handle_report_pending(data)
        elif event_type == 'report_approved':
            self._handle_report_approved(data)
    
    def _handle_fault_reported(self, data: dict):
        """Handle fault reported event"""
        fault = data.get('fault')
        if fault and fault.severity in ['high', 'critical']:
            # Notify engineers
            self.notification_service.create_notification_for_role(
                role='engineer',
                title='Critical Fault Reported',
                message=f"Critical fault reported: {fault.fault_description}",
                notification_type='error',
                related_entity_type='fault',
                related_entity_id=fault.id
            )
    
    def _handle_fault_escalated(self, data: dict):
        """Handle fault escalated event"""
        escalation = data.get('escalation')
        if escalation:
            self.notification_service.create_notification(
                user_id=escalation.escalated_to,
                title='Fault Escalated',
                message=f"Fault has been escalated to you: {escalation.escalation_reason}",
                notification_type='escalation',
                related_entity_type='escalation',
                related_entity_id=escalation.id
            )
    
    def _handle_report_pending(self, data: dict):
        """Handle report pending approval event"""
        report = data.get('report')
        if report:
            # Notify approvers (DM or DGM)
            self.notification_service.create_notification_for_role(
                role='dm',
                title='Report Pending Approval',
                message=f"Resolution report is pending your approval",
                notification_type='warning',
                related_entity_type='report',
                related_entity_id=report.id
            )
    
    def _handle_report_approved(self, data: dict):
        """Handle report approved event"""
        report = data.get('report')
        if report:
            self.notification_service.create_notification(
                user_id=report.prepared_by,
                title='Report Approved',
                message="Your resolution report has been approved",
                notification_type='success',
                related_entity_type='report',
                related_entity_id=report.id
            )




