"""
Documentation Package Repository (UC-09, UC-10)
"""
from app.repositories.base_repository import BaseRepository
from app.models.documentation_package import DocumentationPackage, DocumentationItem

class DocumentationPackageRepository(BaseRepository):
    """Repository for documentation package data access"""
    
    def create_package(self, package: DocumentationPackage) -> int:
        """Create new documentation package"""
        query = """
            INSERT INTO documentation_packages 
            (fault_id, engineer_id, package_name, documentation_type, status)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (
            package.fault_id,
            package.engineer_id,
            package.package_name,
            package.documentation_type,
            package.status
        ))
        self.commit()
        return cursor.lastrowid
    
    def find_package_by_id(self, package_id: int) -> DocumentationPackage:
        """Find package by ID"""
        query = "SELECT * FROM documentation_packages WHERE id = ?"
        row = self.fetch_one(query, (package_id,))
        if row:
            data = self.dict_to_row(row)
            return DocumentationPackage.from_dict(data)
        return None
    
    def find_packages_by_fault(self, fault_id: int) -> list:
        """Find packages by fault"""
        query = """
            SELECT * FROM documentation_packages 
            WHERE fault_id = ? 
            ORDER BY created_at DESC
        """
        rows = self.fetch_all(query, (fault_id,))
        return [DocumentationPackage.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_packages_by_engineer(self, engineer_id: int) -> list:
        """Find packages by engineer"""
        query = """
            SELECT * FROM documentation_packages 
            WHERE engineer_id = ? 
            ORDER BY created_at DESC
        """
        rows = self.fetch_all(query, (engineer_id,))
        return [DocumentationPackage.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_pending_submission(self) -> list:
        """Find packages pending submission"""
        query = """
            SELECT * FROM documentation_packages 
            WHERE status = 'completed' 
            ORDER BY completion_date DESC
        """
        rows = self.fetch_all(query)
        return [DocumentationPackage.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_pending_approval(self) -> list:
        """Find packages pending approval"""
        query = """
            SELECT * FROM documentation_packages 
            WHERE status = 'submitted' 
            ORDER BY submitted_at DESC
        """
        rows = self.fetch_all(query)
        return [DocumentationPackage.from_dict(self.dict_to_row(row)) for row in rows]
    
    def update_package(self, package: DocumentationPackage) -> bool:
        """Update package"""
        query = """
            UPDATE documentation_packages 
            SET status = ?, completion_date = ?, submitted_at = ?,
                approved_by = ?, approved_at = ?
            WHERE id = ?
        """
        completion_date = package.completion_date.isoformat() if package.completion_date else None
        submitted_at = package.submitted_at.isoformat() if package.submitted_at else None
        approved_at = package.approved_at.isoformat() if package.approved_at else None
        
        self.execute_query(query, (
            package.status,
            completion_date,
            submitted_at,
            package.approved_by,
            approved_at,
            package.id
        ))
        self.commit()
        return True
    
    # Documentation Items methods
    def create_item(self, item: DocumentationItem) -> int:
        """Create new documentation item"""
        query = """
            INSERT INTO documentation_items 
            (package_id, document_name, document_type, content, version, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (
            item.package_id,
            item.document_name,
            item.document_type,
            item.content,
            item.version,
            item.status
        ))
        self.commit()
        return cursor.lastrowid
    
    def find_item_by_id(self, item_id: int) -> DocumentationItem:
        """Find item by ID"""
        query = "SELECT * FROM documentation_items WHERE id = ?"
        row = self.fetch_one(query, (item_id,))
        if row:
            data = self.dict_to_row(row)
            return DocumentationItem.from_dict(data)
        return None
    
    def find_items_by_package(self, package_id: int) -> list:
        """Find items by package"""
        query = """
            SELECT * FROM documentation_items 
            WHERE package_id = ? 
            ORDER BY created_at DESC
        """
        rows = self.fetch_all(query, (package_id,))
        return [DocumentationItem.from_dict(self.dict_to_row(row)) for row in rows]
    
    def update_item(self, item: DocumentationItem) -> bool:
        """Update item"""
        query = """
            UPDATE documentation_items 
            SET document_name = ?, document_type = ?, content = ?,
                version = ?, status = ?
            WHERE id = ?
        """
        self.execute_query(query, (
            item.document_name,
            item.document_type,
            item.content,
            item.version,
            item.status,
            item.id
        ))
        self.commit()
        return True
    
    def delete_item(self, item_id: int) -> bool:
        """Delete item"""
        query = "DELETE FROM documentation_items WHERE id = ?"
        self.execute_query(query, (item_id,))
        self.commit()
        return True




