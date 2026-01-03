"""
Database Setup Script
Creates initial users and equipment for testing
"""
from app.database.db_connection import DatabaseConnection
from app.services.auth_service import AuthService
from app.patterns.factory import ServiceFactory
from app.repositories.equipment_repository import EquipmentRepository
from app.models.equipment import Equipment

def setup_database():
    """Create initial users and equipment"""
    db = DatabaseConnection()
    auth_service = ServiceFactory.create_auth_service()
    equipment_repo = EquipmentRepository()
    
    # Create test users
    users = [
        {
            'username': 'technician1',
            'email': 'tech1@example.com',
            'password': 'password123',
            'role': 'technician',
            'full_name': 'John Technician'
        },
        {
            'username': 'engineer1',
            'email': 'eng1@example.com',
            'password': 'password123',
            'role': 'engineer',
            'full_name': 'Jane Engineer'
        },
        {
            'username': 'dm1',
            'email': 'dm1@example.com',
            'password': 'password123',
            'role': 'dm',
            'full_name': 'Bob Deputy Manager'
        },
        {
            'username': 'dgm1',
            'email': 'dgm1@example.com',
            'password': 'password123',
            'role': 'dgm',
            'full_name': 'Alice Deputy General Manager'
        }
    ]
    
    print("Creating test users...")
    for user_data in users:
        try:
            user = auth_service.register_user(**user_data)
            print(f"[OK] Created user: {user_data['username']} ({user_data['role']})")
        except ValueError as e:
            print(f"[SKIP] User {user_data['username']} already exists or error: {e}")
    
    # Create sample equipment
    print("\nCreating sample equipment...")
    equipment_list = [
        {
            'equipment_code': 'EQ-001',
            'equipment_name': 'Main Power Transformer',
            'equipment_type': 'Transformer',
            'location': 'Building A - Floor 1',
            'status': 'operational'
        },
        {
            'equipment_code': 'EQ-002',
            'equipment_name': 'Distribution Panel A',
            'equipment_type': 'Panel',
            'location': 'Building A - Floor 2',
            'status': 'operational'
        },
        {
            'equipment_code': 'EQ-003',
            'equipment_name': 'Backup Generator',
            'equipment_type': 'Generator',
            'location': 'Building B - Basement',
            'status': 'operational'
        },
        {
            'equipment_code': 'EQ-004',
            'equipment_name': 'HVAC Control Unit',
            'equipment_type': 'HVAC',
            'location': 'Building A - Rooftop',
            'status': 'operational'
        },
        {
            'equipment_code': 'EQ-005',
            'equipment_name': 'Emergency Lighting System',
            'equipment_type': 'Lighting',
            'location': 'Building A - All Floors',
            'status': 'operational'
        }
    ]
    
    for eq_data in equipment_list:
        try:
            # Check if equipment already exists
            existing = equipment_repo.find_by_code(eq_data['equipment_code'])
            if existing:
                print(f"[SKIP] Equipment {eq_data['equipment_code']} already exists")
                continue
            
            equipment = Equipment(
                equipment_code=eq_data['equipment_code'],
                equipment_name=eq_data['equipment_name'],
                equipment_type=eq_data['equipment_type'],
                location=eq_data['location'],
                status=eq_data['status']
            )
            equipment_id = equipment_repo.create(equipment)
            print(f"[OK] Created equipment: {eq_data['equipment_code']} - {eq_data['equipment_name']}")
        except Exception as e:
            print(f"[ERROR] Failed to create equipment {eq_data['equipment_code']}: {e}")
    
    print("\nDatabase setup complete!")
    print("\nTest credentials:")
    print("Username: technician1, engineer1, dm1, or dgm1")
    print("Password: password123")

if __name__ == '__main__':
    setup_database()

