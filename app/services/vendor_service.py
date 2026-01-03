"""
Vendor Service (UC-15)
"""
from datetime import datetime
from app.repositories.vendor_repository import VendorRepository
from app.models.vendor import Vendor

class VendorService:
    """Service for vendor management operations"""
    
    def __init__(self, vendor_repository: VendorRepository):
        self.vendor_repository = vendor_repository
    
    def create_vendor(self, vendor_name: str, vendor_code: str,
                     contact_info: str = None, material_list: str = None) -> Vendor:
        """Create new vendor"""
        # Check if vendor code already exists
        existing = self.vendor_repository.find_by_code(vendor_code)
        if existing:
            raise ValueError(f"Vendor with code '{vendor_code}' already exists")
        
        vendor = Vendor(
            vendor_name=vendor_name,
            vendor_code=vendor_code,
            contact_info=contact_info,
            material_list=material_list,
            is_active=True,
            created_at=datetime.now()
        )
        
        vendor_id = self.vendor_repository.create(vendor)
        vendor.id = vendor_id
        return vendor
    
    def update_vendor(self, vendor_id: int, vendor_name: str = None,
                     contact_info: str = None, material_list: str = None,
                     is_active: bool = None) -> Vendor:
        """Update vendor"""
        vendor = self.vendor_repository.find_by_id(vendor_id)
        if not vendor:
            raise ValueError("Vendor not found")
        
        if vendor_name is not None:
            vendor.vendor_name = vendor_name
        if contact_info is not None:
            vendor.contact_info = contact_info
        if material_list is not None:
            vendor.material_list = material_list
        if is_active is not None:
            vendor.is_active = is_active
        
        self.vendor_repository.update(vendor)
        return vendor
    
    def get_vendor_by_id(self, vendor_id: int) -> Vendor:
        """Get vendor by ID"""
        return self.vendor_repository.find_by_id(vendor_id)
    
    def get_vendor_by_code(self, vendor_code: str) -> Vendor:
        """Get vendor by code"""
        return self.vendor_repository.find_by_code(vendor_code)
    
    def get_all_vendors(self, active_only: bool = True) -> list:
        """Get all vendors"""
        return self.vendor_repository.find_all(active_only=active_only)
    
    def deactivate_vendor(self, vendor_id: int) -> Vendor:
        """Deactivate vendor"""
        vendor = self.vendor_repository.find_by_id(vendor_id)
        if not vendor:
            raise ValueError("Vendor not found")
        
        vendor.is_active = False
        self.vendor_repository.update(vendor)
        return vendor
    
    def activate_vendor(self, vendor_id: int) -> Vendor:
        """Activate vendor"""
        vendor = self.vendor_repository.find_by_id(vendor_id)
        if not vendor:
            raise ValueError("Vendor not found")
        
        vendor.is_active = True
        self.vendor_repository.update(vendor)
        return vendor




