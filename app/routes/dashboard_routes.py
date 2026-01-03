"""
Dashboard Routes
"""
from flask import Blueprint, render_template, session, redirect, url_for
from app.controllers.auth_controller import AuthController
from app.controllers.notification_controller import NotificationController
from app.controllers.fault_controller import FaultController
from app.controllers.monitoring_controller import MonitoringController
from app.controllers.equipment_controller import EquipmentController
from app.controllers.report_controller import ReportController

dashboard_bp = Blueprint('dashboard', __name__)
auth_controller = AuthController()
notification_controller = NotificationController()
fault_controller = FaultController()
monitoring_controller = MonitoringController()
equipment_controller = EquipmentController()
report_controller = ReportController()

def require_auth():
    """Require authentication decorator"""
    if not auth_controller.is_authenticated():
        return redirect(url_for('auth.login'))
    return None

def require_role(required_role: str):
    """Require role decorator"""
    if not auth_controller.require_role(required_role):
        return redirect(url_for('auth.login'))
    return None

@dashboard_bp.route('/dashboard/technician')
def technician_dashboard():
    """Technician dashboard"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user = auth_controller.get_current_user()
    if user['role'] != 'technician':
        return redirect(auth_controller._get_role_dashboard(user['role']))
    
    notifications = notification_controller.get_user_notifications(unread_only=True)
    equipment = equipment_controller.get_all_equipment()
    
    return render_template('dashboards/technician.html',
                         user=user,
                         notifications=notifications.get('data', []),
                         equipment=equipment.get('data', []))

@dashboard_bp.route('/dashboard/engineer')
def engineer_dashboard():
    """Engineer dashboard"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user = auth_controller.get_current_user()
    if user['role'] != 'engineer':
        return redirect(auth_controller._get_role_dashboard(user['role']))
    
    notifications = notification_controller.get_user_notifications(unread_only=True)
    faults = fault_controller.get_all_faults(limit=50)
    critical_monitoring = monitoring_controller.get_critical_records()
    
    return render_template('dashboards/engineer.html',
                         user=user,
                         notifications=notifications.get('data', []),
                         faults=faults.get('data', []),
                         critical_monitoring=critical_monitoring.get('data', []))

@dashboard_bp.route('/dashboard/dm')
def dm_dashboard():
    """Deputy Manager dashboard"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user = auth_controller.get_current_user()
    if user['role'] != 'dm':
        return redirect(auth_controller._get_role_dashboard(user['role']))
    
    notifications = notification_controller.get_user_notifications(unread_only=True)
    pending_reports = report_controller.get_pending_approval()
    faults = fault_controller.get_all_faults(limit=50)
    
    return render_template('dashboards/dm.html',
                         user=user,
                         notifications=notifications.get('data', []),
                         pending_reports=pending_reports.get('data', []),
                         faults=faults.get('data', []))

@dashboard_bp.route('/dashboard/dgm')
def dgm_dashboard():
    """Deputy General Manager dashboard"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user = auth_controller.get_current_user()
    if user['role'] != 'dgm':
        return redirect(auth_controller._get_role_dashboard(user['role']))
    
    notifications = notification_controller.get_user_notifications(unread_only=True)
    pending_reports = report_controller.get_pending_approval()
    faults = fault_controller.get_all_faults(limit=100)
    
    return render_template('dashboards/dgm.html',
                         user=user,
                         notifications=notifications.get('data', []),
                         pending_reports=pending_reports.get('data', []),
                         faults=faults.get('data', []))




