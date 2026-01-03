"""
Form Routes
"""
from flask import Blueprint, render_template, request, redirect, url_for
from app.controllers.auth_controller import AuthController
from app.controllers.equipment_controller import EquipmentController
from app.controllers.fault_controller import FaultController
from app.controllers.notification_controller import NotificationController
from app.controllers.performance_report_controller import PerformanceReportController
from app.controllers.data_reverification_controller import DataReverificationController
from app.controllers.monitoring_controller import MonitoringController
from app.controllers.technical_reference_controller import TechnicalReferenceController
from app.controllers.documentation_package_controller import DocumentationPackageController
from app.controllers.delivery_verification_controller import DeliveryVerificationController
from app.controllers.vendor_controller import VendorController

forms_bp = Blueprint('forms', __name__)
auth_controller = AuthController()
equipment_controller = EquipmentController()
fault_controller = FaultController()
notification_controller = NotificationController()
performance_report_controller = PerformanceReportController()
data_reverification_controller = DataReverificationController()
monitoring_controller = MonitoringController()
technical_reference_controller = TechnicalReferenceController()
documentation_package_controller = DocumentationPackageController()
delivery_verification_controller = DeliveryVerificationController()
vendor_controller = VendorController()

def require_auth():
    """Require authentication"""
    if not auth_controller.is_authenticated():
        return redirect(url_for('auth.login'))
    return None

@forms_bp.route('/forms/daily-monitoring')
def daily_monitoring():
    """Daily monitoring form"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    equipment_id = request.args.get('equipment_id')
    equipment = equipment_controller.get_all_equipment()
    user = auth_controller.get_current_user()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    # Use simplified form
    return render_template('forms/daily_monitoring_simple.html',
                         user=user,
                         equipment=equipment.get('data', []),
                         selected_equipment_id=equipment_id,
                         notifications=notifications.get('data', []))

@forms_bp.route('/forms/equipment-status')
def equipment_status():
    """Equipment status form"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user = auth_controller.get_current_user()
    equipment = equipment_controller.get_all_equipment()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    return render_template('forms/equipment_status.html',
                         user=user,
                         equipment=equipment.get('data', []),
                         notifications=notifications.get('data', []))

@forms_bp.route('/forms/report-fault')
def report_fault():
    """Report fault form"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    equipment_id = request.args.get('equipment_id')
    user = auth_controller.get_current_user()
    equipment = equipment_controller.get_all_equipment()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    return render_template('forms/report_fault.html',
                         user=user,
                         equipment=equipment.get('data', []),
                         selected_equipment_id=equipment_id,
                         notifications=notifications.get('data', []))

@forms_bp.route('/forms/root-cause-analysis')
def root_cause_analysis():
    """Root cause analysis form"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    fault_id = request.args.get('fault_id')
    user = auth_controller.get_current_user()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    fault = None
    if fault_id:
        fault_result = fault_controller.get_fault(int(fault_id))
        if fault_result.get('success'):
            fault = fault_result.get('data')
    
    return render_template('forms/root_cause_analysis.html',
                         user=user,
                         fault=fault,
                         notifications=notifications.get('data', []))

@forms_bp.route('/forms/draft-resolution')
def draft_resolution():
    """Draft resolution report form"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    fault_id = request.args.get('fault_id')
    user = auth_controller.get_current_user()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    fault = None
    if fault_id:
        fault_result = fault_controller.get_fault(int(fault_id))
        if fault_result.get('success'):
            fault = fault_result.get('data')
    
    return render_template('forms/draft_resolution.html',
                         user=user,
                         fault=fault,
                         notifications=notifications.get('data', []))

@forms_bp.route('/forms/performance-report')
def performance_report():
    """Performance report form (UC-04)"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user = auth_controller.get_current_user()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    return render_template('forms/performance_report.html',
                         user=user,
                         notifications=notifications.get('data', []))

@forms_bp.route('/forms/data-reverification')
def data_reverification():
    """Data re-verification form (UC-05)"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    monitoring_id = request.args.get('monitoring_id')
    user = auth_controller.get_current_user()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    original_monitoring = None
    if monitoring_id:
        monitoring_result = monitoring_controller.get_technician_history(limit=1000)
        if monitoring_result.get('success'):
            for record in monitoring_result.get('data', []):
                if record.get('id') == int(monitoring_id):
                    original_monitoring = record
                    break
    
    return render_template('forms/data_reverification.html',
                         user=user,
                         original_monitoring=original_monitoring,
                         notifications=notifications.get('data', []))

@forms_bp.route('/forms/technical-reference')
def technical_reference():
    """Technical reference form (UC-07)"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    equipment_id = request.args.get('equipment_id')
    user = auth_controller.get_current_user()
    equipment = equipment_controller.get_all_equipment()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    return render_template('forms/technical_reference.html',
                         user=user,
                         equipment=equipment.get('data', []),
                         selected_equipment_id=equipment_id,
                         notifications=notifications.get('data', []))

@forms_bp.route('/forms/documentation-package')
def documentation_package():
    """Documentation package form (UC-09, UC-10)"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    fault_id = request.args.get('fault_id')
    user = auth_controller.get_current_user()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    fault = None
    if fault_id:
        fault_result = fault_controller.get_fault(int(fault_id))
        if fault_result.get('success'):
            fault = fault_result.get('data')
    
    return render_template('forms/documentation_package.html',
                         user=user,
                         fault=fault,
                         notifications=notifications.get('data', []))

@forms_bp.route('/forms/delivery-verification')
def delivery_verification():
    """Delivery/Service verification form (UC-13, UC-14)"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    vendor_id = request.args.get('vendor_id')
    equipment_id = request.args.get('equipment_id')
    user = auth_controller.get_current_user()
    equipment = equipment_controller.get_all_equipment()
    vendors = vendor_controller.get_all_vendors()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    return render_template('forms/delivery_verification.html',
                         user=user,
                         equipment=equipment.get('data', []),
                         vendors=vendors.get('data', []),
                         selected_vendor_id=vendor_id,
                         selected_equipment_id=equipment_id,
                         notifications=notifications.get('data', []))

@forms_bp.route('/forms/vendor-management')
def vendor_management():
    """Vendor management form (UC-15)"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    vendor_id = request.args.get('vendor_id')
    user = auth_controller.get_current_user()
    notifications = notification_controller.get_user_notifications(unread_only=True)
    
    vendor = None
    if vendor_id:
        vendor_result = vendor_controller.get_vendor(int(vendor_id))
        if vendor_result.get('success'):
            vendor = vendor_result.get('data')
    
    vendors = vendor_controller.get_all_vendors(active_only=False)
    
    return render_template('forms/vendor_management.html',
                         user=user,
                         vendor=vendor,
                         vendors=vendors.get('data', []),
                         notifications=notifications.get('data', []))

