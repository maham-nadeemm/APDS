"""
Vendor Repository (UC-15)
"""
from app.repositories.base_repository import BaseRepository
from app.models.vendor import Vendor

class VendorRepository(BaseRepository):
    """Repository for vendor data access"""
    
    def create(self, vendor: Vendor) -> int:
        """Create new vendor"""
        query = """
            INSERT INTO vendors 
            (vendor_name, contact_info, material_list, vendor_code, is_active)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (
            vendor.vendor_name,
            vendor.contact_info,
            vendor.material_list,
            vendor.vendor_code,
            1 if vendor.is_active else 0
        ))
        self.commit()
        return cursor.lastrowid
    
    def find_by_id(self, vendor_id: int) -> Vendor:
        """Find vendor by ID"""
        query = "SELECT * FROM vendors WHERE id = ?"
        row = self.fetch_one(query, (vendor_id,))
        if row:
            data = self.dict_to_row(row)
            return Vendor.from_dict(data)
        return None
    
    def find_by_code(self, vendor_code: str) -> Vendor:
        """Find vendor by code"""
        query = "SELECT * FROM vendors WHERE vendor_code = ?"
        row = self.fetch_one(query, (vendor_code,))
        if row:
            data = self.dict_to_row(row)
            return Vendor.from_dict(data)
        return None
    
    def find_all(self, active_only: bool = True) -> list:
        """Find all vendors"""
        if active_only:
            query = "SELECT * FROM vendors WHERE is_active = 1 ORDER BY vendor_name"
        else:
            query = "SELECT * FROM vendors ORDER BY vendor_name"
        rows = self.fetch_all(query)
        return [Vendor.from_dict(self.dict_to_row(row)) for row in rows]
    
    def update(self, vendor: Vendor) -> bool:
        """Update vendor"""
        query = """
            UPDATE vendors 
            SET vendor_name = ?, contact_info = ?, material_list = ?, is_active = ?
            WHERE id = ?
        """
        self.execute_query(query, (
            vendor.vendor_name,
            vendor.contact_info,
            vendor.material_list,
            1 if vendor.is_active else 0,
            vendor.id
        ))
        self.commit()
        return True




