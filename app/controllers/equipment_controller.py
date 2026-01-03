"""
Equipment Controller
"""
from app.repositories.equipment_repository import EquipmentRepository
from app.patterns.factory import RepositoryFactory

class EquipmentController:
    """Controller for equipment operations"""
    
    def __init__(self):
        self.equipment_repository = RepositoryFactory.create_equipment_repository()
    
    def get_all_equipment(self) -> dict:
        """Get all equipment"""
        try:
            equipment_list = self.equipment_repository.find_all()
            return {
                'success': True,
                'data': [eq.to_dict() for eq in equipment_list]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_equipment(self, equipment_id: int) -> dict:
        """Get equipment by ID"""
        try:
            equipment = self.equipment_repository.find_by_id(equipment_id)
            if equipment:
                return {
                    'success': True,
                    'data': equipment.to_dict()
                }
            return {
                'success': False,
                'message': 'Equipment not found'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_equipment_by_status(self, status: str) -> dict:
        """Get equipment by status"""
        try:
            equipment_list = self.equipment_repository.find_by_status(status)
            return {
                'success': True,
                'data': [eq.to_dict() for eq in equipment_list]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }




