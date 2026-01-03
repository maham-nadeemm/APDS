"""
Authentication Service
"""
import hashlib
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.repositories.audit_repository import AuditRepository
from app.models.audit_log import AuditLog

class AuthService:
    """Service for authentication and authorization"""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.audit_repository = AuditRepository()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == password_hash
    
    def register_user(self, username: str, email: str, password: str, 
                     role: str, full_name: str) -> User:
        """Register a new user"""
        # Check if username exists
        if self.user_repository.find_by_username(username):
            raise ValueError("Username already exists")
        
        # Check if email exists
        if self.user_repository.find_by_email(email):
            raise ValueError("Email already exists")
        
        # Create user
        password_hash = self.hash_password(password)
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role,
            full_name=full_name
        )
        
        user_id = self.user_repository.create(user)
        user.id = user_id
        
        # Audit log
        self.audit_repository.create(AuditLog(
            user_id=user_id,
            action='user_registered',
            entity_type='user',
            entity_id=user_id
        ))
        
        return user
    
    def authenticate(self, username: str, password: str) -> User:
        """Authenticate user"""
        user = self.user_repository.find_by_username(username)
        
        if not user:
            raise ValueError("Invalid username or password")
        
        if not user.is_active:
            raise ValueError("User account is inactive")
        
        if not self.verify_password(password, user.password_hash):
            raise ValueError("Invalid username or password")
        
        # Audit log
        self.audit_repository.create(AuditLog(
            user_id=user.id,
            action='user_login',
            entity_type='user',
            entity_id=user.id
        ))
        
        return user
    
    def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID"""
        return self.user_repository.find_by_id(user_id)
    
    def has_permission(self, user: User, required_role: str) -> bool:
        """Check if user has required permission"""
        return user.has_permission(required_role)




