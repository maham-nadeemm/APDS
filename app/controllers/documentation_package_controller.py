"""
Documentation Package Controller (UC-09, UC-10)
"""
from flask import session
from app.patterns.factory import ServiceFactory

class DocumentationPackageController:
    """Controller for documentation package operations"""
    
    def __init__(self):
        self.package_service = ServiceFactory.create_documentation_package_service()
    
    def create_package(self, data: dict) -> dict:
        """Create documentation package"""
        try:
            engineer_id = session.get('user_id')
            if not engineer_id:
                return {'success': False, 'message': 'Not authenticated'}
            
            package = self.package_service.create_package(
                fault_id=int(data.get('fault_id')),
                engineer_id=engineer_id,
                package_name=data.get('package_name'),
                documentation_type=data.get('documentation_type')
            )
            
            return {
                'success': True,
                'message': 'Documentation package created successfully',
                'data': package.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def add_item(self, data: dict) -> dict:
        """Add item to package"""
        try:
            item = self.package_service.add_item_to_package(
                package_id=int(data.get('package_id')),
                document_name=data.get('document_name'),
                document_type=data.get('document_type'),
                content=data.get('content'),
                version=data.get('version')
            )
            
            return {
                'success': True,
                'message': 'Item added successfully',
                'data': item.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def update_item(self, item_id: int, data: dict) -> dict:
        """Update item"""
        try:
            item = self.package_service.update_item(
                item_id=item_id,
                document_name=data.get('document_name'),
                document_type=data.get('document_type'),
                content=data.get('content'),
                version=data.get('version'),
                status=data.get('status')
            )
            
            return {
                'success': True,
                'message': 'Item updated successfully',
                'data': item.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def complete_package(self, package_id: int) -> dict:
        """Complete package"""
        try:
            package = self.package_service.complete_package(package_id)
            return {
                'success': True,
                'message': 'Package completed successfully',
                'data': package.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def submit_package(self, package_id: int) -> dict:
        """Submit package for approval"""
        try:
            package = self.package_service.submit_package(package_id)
            return {
                'success': True,
                'message': 'Package submitted successfully',
                'data': package.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def approve_package(self, package_id: int) -> dict:
        """Approve package"""
        try:
            approved_by = session.get('user_id')
            if not approved_by:
                return {'success': False, 'message': 'Not authenticated'}
            
            package = self.package_service.approve_package(package_id, approved_by)
            return {
                'success': True,
                'message': 'Package approved successfully',
                'data': package.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_package(self, package_id: int) -> dict:
        """Get package by ID"""
        try:
            package = self.package_service.get_package_by_id(package_id)
            if package:
                items = self.package_service.get_package_items(package_id)
                package_dict = package.to_dict()
                package_dict['items'] = [item.to_dict() for item in items]
                return {
                    'success': True,
                    'data': package_dict
                }
            return {
                'success': False,
                'message': 'Package not found'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_packages_by_fault(self, fault_id: int) -> dict:
        """Get packages by fault"""
        try:
            packages = self.package_service.get_packages_by_fault(fault_id)
            return {
                'success': True,
                'data': [p.to_dict() for p in packages]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_engineer_packages(self) -> dict:
        """Get engineer's packages"""
        try:
            engineer_id = session.get('user_id')
            if not engineer_id:
                return {'success': False, 'message': 'Not authenticated'}
            
            packages = self.package_service.get_packages_by_engineer(engineer_id)
            return {
                'success': True,
                'data': [p.to_dict() for p in packages]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_pending_submission(self) -> dict:
        """Get packages pending submission"""
        try:
            packages = self.package_service.get_pending_submission()
            return {
                'success': True,
                'data': [p.to_dict() for p in packages]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_pending_approval(self) -> dict:
        """Get packages pending approval"""
        try:
            packages = self.package_service.get_pending_approval()
            return {
                'success': True,
                'data': [p.to_dict() for p in packages]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def delete_item(self, item_id: int) -> dict:
        """Delete item"""
        try:
            self.package_service.delete_item(item_id)
            return {
                'success': True,
                'message': 'Item deleted successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }




