"""
User Repository
"""
from app.repositories.base_repository import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository):
    """Repository for user data access"""
    
    def create(self, user: User) -> int:
        """Create a new user"""
        query = """
            INSERT INTO users (username, email, password_hash, role, full_name, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (
            user.username,
            user.email,
            user.password_hash,
            user.role,
            user.full_name,
            1 if user.is_active else 0
        ))
        self.commit()
        return cursor.lastrowid
    
    def find_by_id(self, user_id: int) -> User:
        """Find user by ID"""
        query = "SELECT * FROM users WHERE id = ?"
        row = self.fetch_one(query, (user_id,))
        if row:
            data = self.dict_to_row(row)
            return User.from_dict(data)
        return None
    
    def find_by_username(self, username: str) -> User:
        """Find user by username"""
        query = "SELECT * FROM users WHERE username = ?"
        row = self.fetch_one(query, (username,))
        if row:
            data = self.dict_to_row(row)
            return User.from_dict(data)
        return None
    
    def find_by_email(self, email: str) -> User:
        """Find user by email"""
        query = "SELECT * FROM users WHERE email = ?"
        row = self.fetch_one(query, (email,))
        if row:
            data = self.dict_to_row(row)
            return User.from_dict(data)
        return None
    
    def find_by_role(self, role: str) -> list:
        """Find all users by role"""
        query = "SELECT * FROM users WHERE role = ? AND is_active = 1"
        rows = self.fetch_all(query, (role,))
        return [User.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_all(self) -> list:
        """Find all users"""
        query = "SELECT * FROM users WHERE is_active = 1"
        rows = self.fetch_all(query)
        return [User.from_dict(self.dict_to_row(row)) for row in rows]
    
    def update(self, user: User) -> bool:
        """Update user"""
        query = """
            UPDATE users 
            SET username = ?, email = ?, role = ?, full_name = ?, is_active = ?
            WHERE id = ?
        """
        self.execute_query(query, (
            user.username,
            user.email,
            user.role,
            user.full_name,
            1 if user.is_active else 0,
            user.id
        ))
        self.commit()
        return True
    
    def delete(self, user_id: int) -> bool:
        """Soft delete user"""
        query = "UPDATE users SET is_active = 0 WHERE id = ?"
        self.execute_query(query, (user_id,))
        self.commit()
        return True




