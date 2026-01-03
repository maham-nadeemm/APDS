"""
Vendor Controller (UC-15)
"""
from flask import session
from app.patterns.factory import ServiceFactory

class VendorController:
    """Controller for vendor management operations"""
    
    def __init__(self):
        self.vendor_service = ServiceFactory.create_vendor_service()
    
    def create_vendor(self, data: dict) -> dict:
        """Create vendor"""
        try:
            vendor = self.vendor_service.create_vendor(
                vendor_name=data.get('vendor_name'),
                vendor_code=data.get('vendor_code'),
                contact_info=data.get('contact_info'),
                material_list=data.get('material_list')
            )
            
            return {
                'success': True,
                'message': 'Vendor created successfully',
                'data': vendor.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def update_vendor(self, vendor_id: int, data: dict) -> dict:
        """Update vendor"""
        try:
            vendor = self.vendor_service.update_vendor(
                vendor_id=vendor_id,
                vendor_name=data.get('vendor_name'),
                contact_info=data.get('contact_info'),
                material_list=data.get('material_list'),
                is_active=data.get('is_active')
            )
            
            return {
                'success': True,
                'message': 'Vendor updated successfully',
                'data': vendor.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_vendor(self, vendor_id: int) -> dict:
        """Get vendor by ID"""
        try:
            vendor = self.vendor_service.get_vendor_by_id(vendor_id)
            if vendor:
                return {
                    'success': True,
                    'data': vendor.to_dict()
                }
            return {
                'success': False,
                'message': 'Vendor not found'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_vendor_by_code(self, vendor_code: str) -> dict:
        """Get vendor by code"""
        try:
            vendor = self.vendor_service.get_vendor_by_code(vendor_code)
            if vendor:
                return {
                    'success': True,
                    'data': vendor.to_dict()
                }
            return {
                'success': False,
                'message': 'Vendor not found'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_all_vendors(self, active_only: bool = True) -> dict:
        """Get all vendors"""
        try:
            vendors = self.vendor_service.get_all_vendors(active_only=active_only)
            return {
                'success': True,
                'data': [v.to_dict() for v in vendors]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def deactivate_vendor(self, vendor_id: int) -> dict:
        """Deactivate vendor"""
        try:
            vendor = self.vendor_service.deactivate_vendor(vendor_id)
            return {
                'success': True,
                'message': 'Vendor deactivated successfully',
                'data': vendor.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def activate_vendor(self, vendor_id: int) -> dict:
        """Activate vendor"""
        try:
            vendor = self.vendor_service.activate_vendor(vendor_id)
            return {
                'success': True,
                'message': 'Vendor activated successfully',
                'data': vendor.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }




