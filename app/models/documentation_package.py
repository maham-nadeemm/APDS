"""
Documentation Package Model (UC-09, UC-10)
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class DocumentationPackage:
    """Documentation Package model"""
    id: Optional[int] = None
    fault_id: int = 0
    engineer_id: int = 0
    package_name: str = ""
    documentation_type: Optional[str] = None
    status: str = "in_progress"  # in_progress, completed, submitted, approved
    completion_date: Optional[datetime] = None
    submitted_at: Optional[datetime] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create DocumentationPackage from dictionary"""
        return cls(
            id=data.get('id'),
            fault_id=data.get('fault_id', 0),
            engineer_id=data.get('engineer_id', 0),
            package_name=data.get('package_name', ''),
            documentation_type=data.get('documentation_type'),
            status=data.get('status', 'in_progress'),
            completion_date=datetime.fromisoformat(data['completion_date']) if data.get('completion_date') else None,
            submitted_at=datetime.fromisoformat(data['submitted_at']) if data.get('submitted_at') else None,
            approved_by=data.get('approved_by'),
            approved_at=datetime.fromisoformat(data['approved_at']) if data.get('approved_at') else None,
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
    
    def to_dict(self) -> dict:
        """Convert DocumentationPackage to dictionary"""
        return {
            'id': self.id,
            'fault_id': self.fault_id,
            'engineer_id': self.engineer_id,
            'package_name': self.package_name,
            'documentation_type': self.documentation_type,
            'status': self.status,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

@dataclass
class DocumentationItem:
    """Documentation Item model"""
    id: Optional[int] = None
    package_id: int = 0
    document_name: str = ""
    document_type: Optional[str] = None
    content: Optional[str] = None
    version: Optional[str] = None
    status: str = "draft"  # draft, completed, approved
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create DocumentationItem from dictionary"""
        return cls(
            id=data.get('id'),
            package_id=data.get('package_id', 0),
            document_name=data.get('document_name', ''),
            document_type=data.get('document_type'),
            content=data.get('content'),
            version=data.get('version'),
            status=data.get('status', 'draft'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
    
    def to_dict(self) -> dict:
        """Convert DocumentationItem to dictionary"""
        return {
            'id': self.id,
            'package_id': self.package_id,
            'document_name': self.document_name,
            'document_type': self.document_type,
            'content': self.content,
            'version': self.version,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }




