"""
Documentation Package Service (UC-09, UC-10)
"""
from datetime import datetime
from app.repositories.documentation_package_repository import DocumentationPackageRepository
from app.repositories.fault_repository import FaultRepository
from app.models.documentation_package import DocumentationPackage, DocumentationItem

class DocumentationPackageService:
    """Service for documentation package operations"""
    
    def __init__(self, package_repository: DocumentationPackageRepository,
                 fault_repository: FaultRepository):
        self.package_repository = package_repository
        self.fault_repository = fault_repository
    
    def create_package(self, fault_id: int, engineer_id: int, package_name: str,
                      documentation_type: str = None) -> DocumentationPackage:
        """Create documentation package"""
        # Validate fault exists
        fault = self.fault_repository.find_by_id(fault_id)
        if not fault:
            raise ValueError("Fault not found")
        
        package = DocumentationPackage(
            fault_id=fault_id,
            engineer_id=engineer_id,
            package_name=package_name,
            documentation_type=documentation_type,
            status="in_progress",
            created_at=datetime.now()
        )
        
        package_id = self.package_repository.create_package(package)
        package.id = package_id
        return package
    
    def add_item_to_package(self, package_id: int, document_name: str,
                           document_type: str = None, content: str = None,
                           version: str = None) -> DocumentationItem:
        """Add item to package"""
        package = self.package_repository.find_package_by_id(package_id)
        if not package:
            raise ValueError("Package not found")
        
        if package.status in ["submitted", "approved"]:
            raise ValueError("Cannot add items to submitted/approved packages")
        
        item = DocumentationItem(
            package_id=package_id,
            document_name=document_name,
            document_type=document_type,
            content=content,
            version=version,
            status="draft",
            created_at=datetime.now()
        )
        
        item_id = self.package_repository.create_item(item)
        item.id = item_id
        return item
    
    def update_item(self, item_id: int, document_name: str = None,
                   document_type: str = None, content: str = None,
                   version: str = None, status: str = None) -> DocumentationItem:
        """Update documentation item"""
        item = self.package_repository.find_item_by_id(item_id)
        if not item:
            raise ValueError("Item not found")
        
        package = self.package_repository.find_package_by_id(item.package_id)
        if package.status in ["submitted", "approved"]:
            raise ValueError("Cannot update items in submitted/approved packages")
        
        if document_name is not None:
            item.document_name = document_name
        if document_type is not None:
            item.document_type = document_type
        if content is not None:
            item.content = content
        if version is not None:
            item.version = version
        if status is not None:
            item.status = status
        
        self.package_repository.update_item(item)
        return item
    
    def complete_package(self, package_id: int) -> DocumentationPackage:
        """Mark package as completed"""
        package = self.package_repository.find_package_by_id(package_id)
        if not package:
            raise ValueError("Package not found")
        
        # Check if all items are completed
        items = self.package_repository.find_items_by_package(package_id)
        if not items:
            raise ValueError("Package has no items")
        
        incomplete_items = [item for item in items if item.status == "draft"]
        if incomplete_items:
            raise ValueError("Package has incomplete items. Complete all items before marking package as complete.")
        
        package.status = "completed"
        package.completion_date = datetime.now()
        self.package_repository.update_package(package)
        return package
    
    def submit_package(self, package_id: int) -> DocumentationPackage:
        """Submit package for approval"""
        package = self.package_repository.find_package_by_id(package_id)
        if not package:
            raise ValueError("Package not found")
        
        if package.status != "completed":
            raise ValueError("Package must be completed before submission")
        
        package.status = "submitted"
        package.submitted_at = datetime.now()
        self.package_repository.update_package(package)
        return package
    
    def approve_package(self, package_id: int, approved_by: int) -> DocumentationPackage:
        """Approve package"""
        package = self.package_repository.find_package_by_id(package_id)
        if not package:
            raise ValueError("Package not found")
        
        if package.status != "submitted":
            raise ValueError("Package must be submitted before approval")
        
        package.status = "approved"
        package.approved_by = approved_by
        package.approved_at = datetime.now()
        self.package_repository.update_package(package)
        return package
    
    def get_package_by_id(self, package_id: int) -> DocumentationPackage:
        """Get package by ID"""
        return self.package_repository.find_package_by_id(package_id)
    
    def get_packages_by_fault(self, fault_id: int) -> list:
        """Get packages by fault"""
        return self.package_repository.find_packages_by_fault(fault_id)
    
    def get_packages_by_engineer(self, engineer_id: int) -> list:
        """Get packages by engineer"""
        return self.package_repository.find_packages_by_engineer(engineer_id)
    
    def get_package_items(self, package_id: int) -> list:
        """Get items in package"""
        return self.package_repository.find_items_by_package(package_id)
    
    def get_pending_submission(self) -> list:
        """Get packages pending submission"""
        return self.package_repository.find_pending_submission()
    
    def get_pending_approval(self) -> list:
        """Get packages pending approval"""
        return self.package_repository.find_pending_approval()
    
    def delete_item(self, item_id: int) -> bool:
        """Delete item from package"""
        item = self.package_repository.find_item_by_id(item_id)
        if not item:
            raise ValueError("Item not found")
        
        package = self.package_repository.find_package_by_id(item.package_id)
        if package.status in ["submitted", "approved"]:
            raise ValueError("Cannot delete items from submitted/approved packages")
        
        return self.package_repository.delete_item(item_id)




