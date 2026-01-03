"""
Authentication Controller
"""
from flask import session, request
from app.services.auth_service import AuthService
from app.patterns.factory import ServiceFactory

class AuthController:
    """Controller for authentication operations"""
    
    def __init__(self):
        self.auth_service = ServiceFactory.create_auth_service()
    
    def login(self, username: str, password: str) -> dict:
        """Handle user login"""
        try:
            user = self.auth_service.authenticate(username, password)
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session['full_name'] = user.full_name
            
            return {
                'success': True,
                'message': 'Login successful',
                'user': user.to_dict(),
                'redirect': self._get_role_dashboard(user.role)
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def logout(self):
        """Handle user logout"""
        session.clear()
        return {
            'success': True,
            'message': 'Logout successful'
        }
    
    def get_current_user(self) -> dict:
        """Get current logged in user"""
        if 'user_id' not in session:
            return None
        
        user = self.auth_service.get_user_by_id(session['user_id'])
        if user:
            return user.to_dict()
        return None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return 'user_id' in session
    
    def require_role(self, required_role: str) -> bool:
        """Check if user has required role"""
        if not self.is_authenticated():
            return False
        
        user = self.auth_service.get_user_by_id(session['user_id'])
        if not user:
            return False
        
        return user.has_permission(required_role)
    
    def _get_role_dashboard(self, role: str) -> str:
        """Get dashboard URL for role"""
        role_dashboards = {
            'technician': '/dashboard/technician',
            'engineer': '/dashboard/engineer',
            'dm': '/dashboard/dm',
            'dgm': '/dashboard/dgm'
        }
        return role_dashboards.get(role, '/dashboard/technician')




