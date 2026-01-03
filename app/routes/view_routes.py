"""
View Routes
"""
from flask import Blueprint, render_template, request, redirect, url_for
from app.controllers.auth_controller import AuthController
from app.controllers.monitoring_controller import MonitoringController
from app.controllers.fault_controller import FaultController
from app.controllers.report_controller import ReportController
from app.controllers.notification_controller import NotificationController

views_bp = Blueprint('views', __name__)
auth_controller = AuthController()
monitoring_controller = MonitoringController()
fault_controller = FaultController()
report_controller = ReportController()
notification_controller = NotificationController()

def require_auth():
    """Require authentication"""
    if not auth_controller.is_authenticated():
        return redirect(url_for('auth.login'))
    return None

@views_bp.route('/views/monitoring-history')
def monitoring_history():
    """Monitoring history view"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user = auth_controller.get_current_user()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    return render_template('views/monitoring_history.html',
                         user=user,
                         notifications=notifications.get('data', []))

@views_bp.route('/views/fault-list')
def fault_list():
    """Fault list view"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user = auth_controller.get_current_user()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    return render_template('views/fault_list.html',
                         user=user,
                         notifications=notifications.get('data', []))

@views_bp.route('/views/escalation-timeline')
def escalation_timeline():
    """Escalation timeline view"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user = auth_controller.get_current_user()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    return render_template('views/escalation_timeline.html',
                         user=user,
                         notifications=notifications.get('data', []))

@views_bp.route('/views/historical-data')
def historical_data():
    """Historical data view"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user = auth_controller.get_current_user()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    return render_template('views/historical_data.html',
                         user=user,
                         notifications=notifications.get('data', []))

@views_bp.route('/views/trend-comparison')
def trend_comparison():
    """Trend comparison view"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user = auth_controller.get_current_user()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    return render_template('views/trend_comparison.html',
                         user=user,
                         notifications=notifications.get('data', []))

@views_bp.route('/views/report-review')
def report_review():
    """Report review view"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    report_id = request.args.get('report_id')
    user = auth_controller.get_current_user()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    report = None
    if report_id:
        report_result = report_controller.get_report(int(report_id))
        if report_result.get('success'):
            report = report_result.get('data')
    
    return render_template('views/report_review.html',
                         user=user,
                         report=report,
                         notifications=notifications.get('data', []))


