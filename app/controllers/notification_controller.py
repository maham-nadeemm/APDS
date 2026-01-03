"""
Notification Controller
"""
from flask import session
from app.services.notification_service import NotificationService
from app.patterns.factory import ServiceFactory

class NotificationController:
    """Controller for notification operations"""
    
    def __init__(self):
        self.notification_service = ServiceFactory.create_notification_service()
    
    def get_user_notifications(self, unread_only: bool = False) -> dict:
        """Get user notifications"""
        try:
            user_id = session.get('user_id')
            if not user_id:
                return {'success': False, 'message': 'Not authenticated'}
            
            notifications = self.notification_service.get_user_notifications(user_id, unread_only)
            return {
                'success': True,
                'data': [notif.to_dict() for notif in notifications]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def mark_as_read(self, notification_id: int) -> dict:
        """Mark notification as read"""
        try:
            self.notification_service.mark_as_read(notification_id)
            return {
                'success': True,
                'message': 'Notification marked as read'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def mark_all_as_read(self) -> dict:
        """Mark all notifications as read"""
        try:
            user_id = session.get('user_id')
            if not user_id:
                return {'success': False, 'message': 'Not authenticated'}
            
            self.notification_service.mark_all_as_read(user_id)
            return {
                'success': True,
                'message': 'All notifications marked as read'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_unread_count(self) -> dict:
        """Get unread notification count"""
        try:
            user_id = session.get('user_id')
            if not user_id:
                return {'success': False, 'count': 0}
            
            count = self.notification_service.get_unread_count(user_id)
            return {
                'success': True,
                'count': count
            }
        except Exception as e:
            return {
                'success': False,
                'count': 0
            }




