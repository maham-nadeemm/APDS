"""
Report Routes
"""
from flask import Blueprint, render_template, redirect, url_for
from app.controllers.auth_controller import AuthController
from app.controllers.report_controller import ReportController
from app.controllers.notification_controller import NotificationController

reports_bp = Blueprint('reports', __name__)
auth_controller = AuthController()
report_controller = ReportController()
notification_controller = NotificationController()

def require_auth():
    """Require authentication"""
    if not auth_controller.is_authenticated():
        return redirect(url_for('auth.login'))
    return None

@reports_bp.route('/reports/approved')
def approved_reports():
    """Approved reports archive"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user = auth_controller.get_current_user()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    return render_template('reports/approved_reports.html',
                         user=user,
                         notifications=notifications.get('data', []))




