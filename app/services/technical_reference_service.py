"""
Technical Reference Service (UC-07)
"""
from datetime import datetime
from app.repositories.technical_reference_repository import TechnicalReferenceRepository
from app.models.technical_reference import TechnicalReference

class TechnicalReferenceService:
    """Service for technical reference operations"""
    
    def __init__(self, reference_repository: TechnicalReferenceRepository):
        self.reference_repository = reference_repository
    
    def create_reference(self, equipment_id: int, engineer_id: int,
                        reference_type: str, document_name: str,
                        document_version: str = None, findings: str = None,
                        relevance: str = None, conclusions: str = None) -> TechnicalReference:
        """Create technical reference"""
        reference = TechnicalReference(
            equipment_id=equipment_id,
            engineer_id=engineer_id,
            reference_type=reference_type,
            document_name=document_name,
            document_version=document_version,
            findings=findings,
            relevance=relevance,
            conclusions=conclusions,
            created_at=datetime.now()
        )
        
        reference_id = self.reference_repository.create(reference)
        reference.id = reference_id
        return reference
    
    def get_reference_by_id(self, reference_id: int) -> TechnicalReference:
        """Get reference by ID"""
        return self.reference_repository.find_by_id(reference_id)
    
    def get_references_by_equipment(self, equipment_id: int) -> list:
        """Get references by equipment"""
        return self.reference_repository.find_by_equipment(equipment_id)
    
    def get_references_by_engineer(self, engineer_id: int) -> list:
        """Get references by engineer"""
        return self.reference_repository.find_by_engineer(engineer_id)
    
    def get_references_by_type(self, reference_type: str) -> list:
        """Get references by type"""
        return self.reference_repository.find_by_type(reference_type)




