"""
Notification Service
"""
from app.repositories.notification_repository import NotificationRepository
from app.repositories.user_repository import UserRepository
from app.models.notification import Notification

class NotificationService:
    """Service for notification management"""
    
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository
        self.user_repository = UserRepository()
    
    def create_notification(self, user_id: int, title: str, message: str,
                           notification_type: str = "info",
                           related_entity_type: str = None,
                           related_entity_id: int = None) -> Notification:
        """Create a new notification"""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            is_read=False,
            related_entity_type=related_entity_type,
            related_entity_id=related_entity_id
        )
        
        notification_id = self.notification_repository.create(notification)
        notification.id = notification_id
        return notification
    
    def create_notification_for_role(self, role: str, title: str, message: str,
                                    notification_type: str = "info",
                                    related_entity_type: str = None,
                                    related_entity_id: int = None) -> list:
        """Create notifications for all users with a specific role"""
        users = self.user_repository.find_by_role(role)
        notifications = []
        
        for user in users:
            notification = self.create_notification(
                user_id=user.id,
                title=title,
                message=message,
                notification_type=notification_type,
                related_entity_type=related_entity_type,
                related_entity_id=related_entity_id
            )
            notifications.append(notification)
        
        return notifications
    
    def get_user_notifications(self, user_id: int, unread_only: bool = False) -> list:
        """Get notifications for user"""
        return self.notification_repository.find_by_user(user_id, unread_only)
    
    def mark_as_read(self, notification_id: int) -> bool:
        """Mark notification as read"""
        return self.notification_repository.mark_as_read(notification_id)
    
    def mark_all_as_read(self, user_id: int) -> bool:
        """Mark all user notifications as read"""
        return self.notification_repository.mark_all_as_read(user_id)
    
    def get_unread_count(self, user_id: int) -> int:
        """Get unread notification count"""
        return self.notification_repository.count_unread(user_id)




