"""
RCA Controller
"""
from flask import session
from app.repositories.rca_repository import RCARepository
from app.patterns.factory import RepositoryFactory
from app.models.rca import RootCauseAnalysis
from datetime import datetime

class RCAController:
    """Controller for Root Cause Analysis operations"""
    
    def __init__(self):
        self.rca_repository = RepositoryFactory.create_rca_repository()
    
    def create_rca(self, data: dict) -> dict:
        """Create RCA"""
        try:
            analyzed_by = session.get('user_id')
            if not analyzed_by:
                return {'success': False, 'message': 'Not authenticated'}
            
            rca = RootCauseAnalysis(
                fault_id=int(data.get('fault_id')),
                analyzed_by=analyzed_by,
                root_cause=data.get('root_cause'),
                contributing_factors=data.get('contributing_factors'),
                analysis_date=datetime.now()
            )
            
            rca_id = self.rca_repository.create(rca)
            rca.id = rca_id
            
            return {
                'success': True,
                'message': 'RCA created successfully',
                'data': rca.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_rca(self, rca_id: int) -> dict:
        """Get RCA by ID"""
        try:
            rca = self.rca_repository.find_by_id(rca_id)
            if rca:
                return {
                    'success': True,
                    'data': rca.to_dict()
                }
            return {
                'success': False,
                'message': 'RCA not found'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_rca_by_fault(self, fault_id: int) -> dict:
        """Get RCA by fault ID"""
        try:
            rca = self.rca_repository.find_by_fault(fault_id)
            if rca:
                return {
                    'success': True,
                    'data': rca.to_dict()
                }
            return {
                'success': False,
                'message': 'RCA not found'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }




