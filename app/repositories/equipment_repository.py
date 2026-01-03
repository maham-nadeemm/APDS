"""
Equipment Repository
"""
from app.repositories.base_repository import BaseRepository
from app.models.equipment import Equipment

class EquipmentRepository(BaseRepository):
    """Repository for equipment data access"""
    
    def create(self, equipment: Equipment) -> int:
        """Create new equipment"""
        query = """
            INSERT INTO equipment (equipment_code, equipment_name, equipment_type, 
                                 location, status, last_maintenance_date, next_maintenance_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (
            equipment.equipment_code,
            equipment.equipment_name,
            equipment.equipment_type,
            equipment.location,
            equipment.status,
            equipment.last_maintenance_date.isoformat() if equipment.last_maintenance_date else None,
            equipment.next_maintenance_date.isoformat() if equipment.next_maintenance_date else None
        ))
        self.commit()
        return cursor.lastrowid
    
    def find_by_id(self, equipment_id: int) -> Equipment:
        """Find equipment by ID"""
        query = "SELECT * FROM equipment WHERE id = ?"
        row = self.fetch_one(query, (equipment_id,))
        if row:
            data = self.dict_to_row(row)
            return Equipment.from_dict(data)
        return None
    
    def find_by_code(self, code: str) -> Equipment:
        """Find equipment by code"""
        query = "SELECT * FROM equipment WHERE equipment_code = ?"
        row = self.fetch_one(query, (code,))
        if row:
            data = self.dict_to_row(row)
            return Equipment.from_dict(data)
        return None
    
    def find_all(self) -> list:
        """Find all equipment"""
        query = "SELECT * FROM equipment ORDER BY equipment_name"
        rows = self.fetch_all(query)
        return [Equipment.from_dict(self.dict_to_row(row)) for row in rows]
    
    def find_by_status(self, status: str) -> list:
        """Find equipment by status"""
        query = "SELECT * FROM equipment WHERE status = ?"
        rows = self.fetch_all(query, (status,))
        return [Equipment.from_dict(self.dict_to_row(row)) for row in rows]
    
    def update(self, equipment: Equipment) -> bool:
        """Update equipment"""
        query = """
            UPDATE equipment 
            SET equipment_name = ?, equipment_type = ?, location = ?, 
                status = ?, last_maintenance_date = ?, next_maintenance_date = ?
            WHERE id = ?
        """
        self.execute_query(query, (
            equipment.equipment_name,
            equipment.equipment_type,
            equipment.location,
            equipment.status,
            equipment.last_maintenance_date.isoformat() if equipment.last_maintenance_date else None,
            equipment.next_maintenance_date.isoformat() if equipment.next_maintenance_date else None,
            equipment.id
        ))
        self.commit()
        return True




