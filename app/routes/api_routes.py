"""
API Routes
"""
from flask import Blueprint, request, jsonify, session
from app.controllers.auth_controller import AuthController
from app.controllers.monitoring_controller import MonitoringController
from app.controllers.fault_controller import FaultController
from app.controllers.report_controller import ReportController
from app.controllers.notification_controller import NotificationController
from app.controllers.equipment_controller import EquipmentController
from app.controllers.rca_controller import RCAController
from app.controllers.performance_report_controller import PerformanceReportController
from app.controllers.data_reverification_controller import DataReverificationController
from app.controllers.technical_reference_controller import TechnicalReferenceController
from app.controllers.documentation_package_controller import DocumentationPackageController
from app.controllers.delivery_verification_controller import DeliveryVerificationController
from app.controllers.vendor_controller import VendorController

api_bp = Blueprint('api', __name__, url_prefix='/api')
auth_controller = AuthController()
monitoring_controller = MonitoringController()
fault_controller = FaultController()
report_controller = ReportController()
notification_controller = NotificationController()
equipment_controller = EquipmentController()
rca_controller = RCAController()
performance_report_controller = PerformanceReportController()
data_reverification_controller = DataReverificationController()
technical_reference_controller = TechnicalReferenceController()
documentation_package_controller = DocumentationPackageController()
delivery_verification_controller = DeliveryVerificationController()
vendor_controller = VendorController()

def require_auth_api():
    """Check authentication for API"""
    if not auth_controller.is_authenticated():
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    return None

# Monitoring API
@api_bp.route('/monitoring', methods=['POST'])
def create_monitoring():
    """Create monitoring record"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    result = monitoring_controller.create_monitoring(data)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/monitoring/equipment/<int:equipment_id>', methods=['GET'])
def get_equipment_monitoring(equipment_id):
    """Get equipment monitoring history"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    limit = request.args.get('limit', 100, type=int)
    result = monitoring_controller.get_equipment_history(equipment_id, limit)
    return jsonify(result), 200

@api_bp.route('/monitoring/technician', methods=['GET'])
def get_technician_monitoring():
    """Get technician monitoring history"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    limit = request.args.get('limit', 100, type=int)
    result = monitoring_controller.get_technician_history(limit)
    return jsonify(result), 200

@api_bp.route('/monitoring/<int:monitoring_id>', methods=['GET'])
def get_monitoring(monitoring_id):
    """Get a single monitoring record"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = monitoring_controller.get_monitoring(monitoring_id)
    status_code = 200 if result['success'] else 404
    return jsonify(result), status_code

@api_bp.route('/monitoring/<int:monitoring_id>', methods=['PUT'])
def update_monitoring(monitoring_id):
    """Update monitoring record"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    result = monitoring_controller.update_monitoring(monitoring_id, data)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/monitoring/<int:monitoring_id>', methods=['DELETE'])
def delete_monitoring(monitoring_id):
    """Delete monitoring record"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = monitoring_controller.delete_monitoring(monitoring_id)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

# Fault API
@api_bp.route('/faults', methods=['POST'])
def report_fault():
    """Report a fault"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    result = fault_controller.report_fault(data)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/faults', methods=['GET'])
def get_faults():
    """Get all faults"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    limit = request.args.get('limit', 100, type=int)
    result = fault_controller.get_all_faults(limit)
    return jsonify(result), 200

@api_bp.route('/faults/<int:fault_id>', methods=['GET'])
def get_fault(fault_id):
    """Get fault by ID"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = fault_controller.get_fault(fault_id)
    status_code = 200 if result['success'] else 404
    return jsonify(result), status_code

@api_bp.route('/faults/<int:fault_id>/status', methods=['PUT'])
def update_fault_status(fault_id):
    """Update fault status"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    status = data.get('status')
    result = fault_controller.update_fault_status(fault_id, status)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

# Report API
@api_bp.route('/reports', methods=['POST'])
def create_report():
    """Create draft report"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    result = report_controller.create_draft_report(data)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/reports/<int:report_id>/submit', methods=['POST'])
def submit_report(report_id):
    """Submit report for approval"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = report_controller.submit_for_approval(report_id)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/reports/<int:report_id>/approve', methods=['POST'])
def approve_report(report_id):
    """Approve report"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = report_controller.approve_report(report_id)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/reports/pending', methods=['GET'])
def get_pending_reports():
    """Get pending approval reports (all types)"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    # Get all pending reports (both regular and performance)
    result = report_controller.get_all_pending_reports()
    return jsonify(result), 200

# Notification API
@api_bp.route('/notifications', methods=['GET'])
def get_notifications():
    """Get user notifications"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    result = notification_controller.get_user_notifications(unread_only)
    return jsonify(result), 200

@api_bp.route('/notifications/<int:notification_id>/read', methods=['POST'])
def mark_notification_read(notification_id):
    """Mark notification as read"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = notification_controller.mark_as_read(notification_id)
    return jsonify(result), 200

@api_bp.route('/notifications/read-all', methods=['POST'])
def mark_all_read():
    """Mark all notifications as read"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = notification_controller.mark_all_as_read()
    return jsonify(result), 200

@api_bp.route('/notifications/unread-count', methods=['GET'])
def get_unread_count():
    """Get unread notification count"""
    result = notification_controller.get_unread_count()
    return jsonify(result), 200

# RCA API
@api_bp.route('/rca', methods=['POST'])
def create_rca():
    """Create root cause analysis"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    result = rca_controller.create_rca(data)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/rca/<int:rca_id>', methods=['GET'])
def get_rca(rca_id):
    """Get RCA by ID"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = rca_controller.get_rca(rca_id)
    status_code = 200 if result['success'] else 404
    return jsonify(result), status_code

@api_bp.route('/rca/fault/<int:fault_id>', methods=['GET'])
def get_rca_by_fault(fault_id):
    """Get RCA by fault ID"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = rca_controller.get_rca_by_fault(fault_id)
    status_code = 200 if result['success'] else 404
    return jsonify(result), status_code

# Equipment API
@api_bp.route('/equipment', methods=['GET'])
def get_equipment():
    """Get all equipment"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = equipment_controller.get_all_equipment()
    return jsonify(result), 200

@api_bp.route('/equipment/<int:equipment_id>', methods=['GET'])
def get_equipment_by_id(equipment_id):
    """Get equipment by ID"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = equipment_controller.get_equipment(equipment_id)
    status_code = 200 if result['success'] else 404
    return jsonify(result), status_code

# Performance Report API (UC-04)
@api_bp.route('/performance-reports', methods=['POST'])
def create_performance_report():
    """Create performance report"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    result = performance_report_controller.create_draft_report(data)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/performance-reports/compile', methods=['POST'])
def compile_performance_data():
    """Compile monitoring data for performance report"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    result = performance_report_controller.compile_report_data(data)
    return jsonify(result), 200

@api_bp.route('/performance-reports/<int:report_id>/submit', methods=['POST'])
def submit_performance_report(report_id):
    """Submit performance report for approval"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = performance_report_controller.submit_for_approval(report_id)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/performance-reports/<int:report_id>/approve', methods=['POST'])
def approve_performance_report(report_id):
    """Approve performance report"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = performance_report_controller.approve_report(report_id)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/performance-reports/pending', methods=['GET'])
def get_pending_performance_reports():
    """Get pending performance reports"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = performance_report_controller.get_pending_approval()
    return jsonify(result), 200

# Data Re-verification API (UC-05)
@api_bp.route('/data-reverification', methods=['POST'])
def create_data_reverification():
    """Create data re-verification"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    result = data_reverification_controller.create_reverification(data)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/data-reverification/<int:reverification_id>/approve', methods=['POST'])
def approve_data_reverification(reverification_id):
    """Approve data re-verification"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = data_reverification_controller.approve_reverification(reverification_id)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/data-reverification/pending', methods=['GET'])
def get_pending_reverifications():
    """Get pending re-verifications"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = data_reverification_controller.get_pending_approval()
    return jsonify(result), 200

# Technical Reference API (UC-07)
@api_bp.route('/technical-references', methods=['POST'])
def create_technical_reference():
    """Create technical reference"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    result = technical_reference_controller.create_reference(data)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/technical-references/equipment/<int:equipment_id>', methods=['GET'])
def get_equipment_references(equipment_id):
    """Get references by equipment"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = technical_reference_controller.get_equipment_references(equipment_id)
    return jsonify(result), 200

@api_bp.route('/technical-references/engineer', methods=['GET'])
def get_engineer_references():
    """Get engineer's references"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = technical_reference_controller.get_engineer_references()
    return jsonify(result), 200

# Documentation Package API (UC-09, UC-10)
@api_bp.route('/documentation-packages', methods=['POST'])
def create_documentation_package():
    """Create documentation package"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    result = documentation_package_controller.create_package(data)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/documentation-packages/<int:package_id>', methods=['GET'])
def get_documentation_package(package_id):
    """Get documentation package by ID"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = documentation_package_controller.get_package(package_id)
    status_code = 200 if result['success'] else 404
    return jsonify(result), status_code

@api_bp.route('/documentation-packages/fault/<int:fault_id>', methods=['GET'])
def get_packages_by_fault(fault_id):
    """Get packages by fault"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = documentation_package_controller.get_packages_by_fault(fault_id)
    return jsonify(result), 200

@api_bp.route('/documentation-packages/engineer', methods=['GET'])
def get_engineer_packages():
    """Get engineer's packages"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = documentation_package_controller.get_engineer_packages()
    return jsonify(result), 200

@api_bp.route('/documentation-packages/<int:package_id>/items', methods=['POST'])
def add_package_item(package_id):
    """Add item to package"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    data['package_id'] = package_id
    result = documentation_package_controller.add_item(data)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/documentation-packages/items/<int:item_id>', methods=['PUT'])
def update_package_item(item_id):
    """Update package item"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    result = documentation_package_controller.update_item(item_id, data)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/documentation-packages/items/<int:item_id>', methods=['DELETE'])
def delete_package_item(item_id):
    """Delete package item"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = documentation_package_controller.delete_item(item_id)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/documentation-packages/<int:package_id>/complete', methods=['POST'])
def complete_documentation_package(package_id):
    """Complete documentation package"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = documentation_package_controller.complete_package(package_id)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/documentation-packages/<int:package_id>/submit', methods=['POST'])
def submit_documentation_package(package_id):
    """Submit documentation package"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = documentation_package_controller.submit_package(package_id)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/documentation-packages/<int:package_id>/approve', methods=['POST'])
def approve_documentation_package(package_id):
    """Approve documentation package"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = documentation_package_controller.approve_package(package_id)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/documentation-packages/pending-submission', methods=['GET'])
def get_pending_submission_packages():
    """Get packages pending submission"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = documentation_package_controller.get_pending_submission()
    return jsonify(result), 200

@api_bp.route('/documentation-packages/pending-approval', methods=['GET'])
def get_pending_approval_packages():
    """Get packages pending approval"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = documentation_package_controller.get_pending_approval()
    return jsonify(result), 200

# Delivery/Service Verification API (UC-13, UC-14)
@api_bp.route('/delivery-verification', methods=['POST'])
def create_delivery_verification():
    """Create delivery/service verification"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    result = delivery_verification_controller.create_verification(data)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/delivery-verification/<int:verification_id>', methods=['GET'])
def get_delivery_verification(verification_id):
    """Get verification by ID"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = delivery_verification_controller.get_verification(verification_id)
    status_code = 200 if result['success'] else 404
    return jsonify(result), status_code

@api_bp.route('/delivery-verification/<int:verification_id>', methods=['PUT'])
def update_delivery_verification(verification_id):
    """Update verification"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    result = delivery_verification_controller.update_verification(verification_id, data)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/delivery-verification/<int:verification_id>/verify', methods=['POST'])
def verify_delivery(verification_id):
    """Verify delivery/service"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    result = delivery_verification_controller.verify(verification_id, data)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/delivery-verification/vendor/<int:vendor_id>', methods=['GET'])
def get_vendor_verifications(vendor_id):
    """Get verifications by vendor"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = delivery_verification_controller.get_verifications_by_vendor(vendor_id)
    return jsonify(result), 200

@api_bp.route('/delivery-verification/pending', methods=['GET'])
def get_pending_verifications():
    """Get pending verifications"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = delivery_verification_controller.get_pending_verifications()
    return jsonify(result), 200

# Vendor Management API (UC-15)
@api_bp.route('/vendors', methods=['POST'])
def create_vendor():
    """Create vendor"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    result = vendor_controller.create_vendor(data)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/vendors', methods=['GET'])
def get_vendors():
    """Get all vendors"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    active_only = request.args.get('active_only', 'true').lower() == 'true'
    result = vendor_controller.get_all_vendors(active_only=active_only)
    return jsonify(result), 200

@api_bp.route('/vendors/<int:vendor_id>', methods=['GET'])
def get_vendor(vendor_id):
    """Get vendor by ID"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = vendor_controller.get_vendor(vendor_id)
    status_code = 200 if result['success'] else 404
    return jsonify(result), status_code

@api_bp.route('/vendors/<int:vendor_id>', methods=['PUT'])
def update_vendor(vendor_id):
    """Update vendor"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    data = request.get_json()
    result = vendor_controller.update_vendor(vendor_id, data)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/vendors/<int:vendor_id>/deactivate', methods=['POST'])
def deactivate_vendor(vendor_id):
    """Deactivate vendor"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = vendor_controller.deactivate_vendor(vendor_id)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@api_bp.route('/vendors/<int:vendor_id>/activate', methods=['POST'])
def activate_vendor(vendor_id):
    """Activate vendor"""
    auth_check = require_auth_api()
    if auth_check:
        return auth_check
    
    result = vendor_controller.activate_vendor(vendor_id)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

