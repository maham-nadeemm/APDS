"""
Notification Repository
"""
from app.repositories.base_repository import BaseRepository
from app.models.notification import Notification

class NotificationRepository(BaseRepository):
    """Repository for notification data access"""
    
    def create(self, notification: Notification) -> int:
        """Create new notification"""
        query = """
            INSERT INTO notifications 
            (user_id, title, message, notification_type, is_read, 
             related_entity_type, related_entity_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (
            notification.user_id,
            notification.title,
            notification.message,
            notification.notification_type,
            1 if notification.is_read else 0,
            notification.related_entity_type,
            notification.related_entity_id
        ))
        self.commit()
        return cursor.lastrowid
    
    def find_by_id(self, notification_id: int) -> Notification:
        """Find notification by ID"""
        query = "SELECT * FROM notifications WHERE id = ?"
        row = self.fetch_one(query, (notification_id,))
        if row:
            data = self.dict_to_row(row)
            return Notification.from_dict(data)
        return None
    
    def find_by_user(self, user_id: int, unread_only: bool = False) -> list:
        """Find notifications by user"""
        if unread_only:
            query = "SELECT * FROM notifications WHERE user_id = ? AND is_read = 0 ORDER BY created_at DESC"
        else:
            query = "SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC"
        rows = self.fetch_all(query, (user_id,))
        return [Notification.from_dict(self.dict_to_row(row)) for row in rows]
    
    def mark_as_read(self, notification_id: int) -> bool:
        """Mark notification as read"""
        query = "UPDATE notifications SET is_read = 1 WHERE id = ?"
        self.execute_query(query, (notification_id,))
        self.commit()
        return True
    
    def mark_all_as_read(self, user_id: int) -> bool:
        """Mark all user notifications as read"""
        query = "UPDATE notifications SET is_read = 1 WHERE user_id = ? AND is_read = 0"
        self.execute_query(query, (user_id,))
        self.commit()
        return True
    
    def count_unread(self, user_id: int) -> int:
        """Count unread notifications for user"""
        query = "SELECT COUNT(*) as count FROM notifications WHERE user_id = ? AND is_read = 0"
        row = self.fetch_one(query, (user_id,))
        return row['count'] if row else 0




