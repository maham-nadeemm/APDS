"""
Technical Reference Repository (UC-07)
"""
from app.repositories.base_repository import BaseRepository
from app.models.technical_reference import TechnicalReference

class TechnicalReferenceRepository(BaseRepository):
    """Repository for technical reference data access"""
    
    def create(self, reference: TechnicalReference) -> int:
        """Create new technical reference"""
        query = """
            INSERT INTO technical_references 
            (equipment_id, engineer_id, reference_type, document_name, 
             document_version, findings, relevance, conclusions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (
            reference.equipment_id,
            reference.engineer_id,
            reference.reference_type,
            reference.document_name,
            reference.document_version,
            reference.findings,
            reference.relevance,
            reference.conclusions
        ))
        self.commit()
        return cursor.lastrowid
    
    def find_by_id(self, reference_id: int) -> TechnicalReference:
        """Find reference by ID"""
        query = "SELECT * FROM technical_references WHERE id = ?"
        row = self.fetch_one(query, (reference_id,))
        if row:
            data = self.dict_to_row(row)
            return TechnicalReference.from_dict(data)
        return None
    
    def find_by_equipment(self, equipment_id: int) -> list:
        """Find references by equipment"""
        query = """
            SELECT * FROM technical_references 
            WHERE equipment_id = ? 
            ORDER BY created_at DESC
        """
        rows = self.fetch_all(query, (equipment_id,))
        return [TechnicalReference.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_by_engineer(self, engineer_id: int) -> list:
        """Find references by engineer"""
        query = """
            SELECT * FROM technical_references 
            WHERE engineer_id = ? 
            ORDER BY created_at DESC
        """
        rows = self.fetch_all(query, (engineer_id,))
        return [TechnicalReference.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_by_type(self, reference_type: str) -> list:
        """Find references by type"""
        query = """
            SELECT * FROM technical_references 
            WHERE reference_type = ? 
            ORDER BY created_at DESC
        """
        rows = self.fetch_all(query, (reference_type,))
        return [TechnicalReference.from_dict(self.dict_to_row(row)) for row in rows]




