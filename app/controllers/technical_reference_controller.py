"""
Technical Reference Controller (UC-07)
"""
from flask import session
from app.patterns.factory import ServiceFactory

class TechnicalReferenceController:
    """Controller for technical reference operations"""
    
    def __init__(self):
        self.reference_service = ServiceFactory.create_technical_reference_service()
    
    def create_reference(self, data: dict) -> dict:
        """Create technical reference"""
        try:
            engineer_id = session.get('user_id')
            if not engineer_id:
                return {'success': False, 'message': 'Not authenticated'}
            
            reference = self.reference_service.create_reference(
                equipment_id=int(data.get('equipment_id')),
                engineer_id=engineer_id,
                reference_type=data.get('reference_type', 'drawing'),
                document_name=data.get('document_name'),
                document_version=data.get('document_version'),
                findings=data.get('findings'),
                relevance=data.get('relevance'),
                conclusions=data.get('conclusions')
            )
            
            return {
                'success': True,
                'message': 'Technical reference created successfully',
                'data': reference.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_reference(self, reference_id: int) -> dict:
        """Get reference by ID"""
        try:
            reference = self.reference_service.get_reference_by_id(reference_id)
            if reference:
                return {
                    'success': True,
                    'data': reference.to_dict()
                }
            return {
                'success': False,
                'message': 'Reference not found'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_equipment_references(self, equipment_id: int) -> dict:
        """Get references by equipment"""
        try:
            references = self.reference_service.get_references_by_equipment(equipment_id)
            return {
                'success': True,
                'data': [r.to_dict() for r in references]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_engineer_references(self) -> dict:
        """Get engineer's references"""
        try:
            engineer_id = session.get('user_id')
            if not engineer_id:
                return {'success': False, 'message': 'Not authenticated'}
            
            references = self.reference_service.get_references_by_engineer(engineer_id)
            return {
                'success': True,
                'data': [r.to_dict() for r in references]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

