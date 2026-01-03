# Architecture & Design Patterns Documentation

## System Architecture Overview

This document provides a comprehensive explanation of the architecture and design patterns used in the Role-Based Operations & Monitoring System.

## 1. Clean Architecture Implementation

### Layer Structure

The system follows Clean Architecture principles with clear separation of concerns:

```
┌─────────────────────────────────────┐
│         Presentation Layer         │  (Routes, Controllers)
│  - HTTP Request/Response Handling   │
│  - Session Management               │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│         Application Layer           │  (Services)
│  - Business Logic                   │
│  - Use Cases                        │
│  - Orchestration                    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│         Domain Layer                 │  (Models)
│  - Business Entities                 │
│  - Domain Rules                      │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│         Infrastructure Layer         │  (Repositories, Database)
│  - Data Persistence                  │
│  - External Services                 │
└─────────────────────────────────────┘
```

### Layer Responsibilities

#### Models Layer (`app/models/`)
- **Purpose**: Domain entities representing business concepts
- **Responsibilities**:
  - Data structure definition
  - Business rule validation
  - Data transformation (to_dict, from_dict)
- **Example**: `User` model with permission checking logic

#### Repositories Layer (`app/repositories/`)
- **Purpose**: Abstract data access
- **Responsibilities**:
  - CRUD operations
  - Query execution
  - Data mapping (SQL to Models)
- **Pattern**: Repository Pattern
- **Example**: `UserRepository` handles all user data operations

#### Services Layer (`app/services/`)
- **Purpose**: Business logic implementation
- **Responsibilities**:
  - Business rule enforcement
  - Transaction coordination
  - Cross-cutting concerns
- **Example**: `FaultService` handles fault reporting logic

#### Controllers Layer (`app/controllers/`)
- **Purpose**: Request/response handling
- **Responsibilities**:
  - Input validation
  - Response formatting
  - Session management
- **Example**: `FaultController` processes fault-related requests

#### Routes Layer (`app/routes/`)
- **Purpose**: URL routing and endpoint definition
- **Responsibilities**:
  - Route registration
  - HTTP method handling
  - Blueprint organization
- **Example**: `api_routes.py` defines all API endpoints

## 2. Design Patterns Detailed Explanation

### 2.1 Factory Pattern

**Location**: `app/patterns/factory.py`

**Purpose**: Centralize object creation and manage dependencies

**Implementation**:
```python
class RepositoryFactory:
    @staticmethod
    def create_user_repository():
        return UserRepository()
    
class ServiceFactory:
    @staticmethod
    def create_fault_service():
        fault_repo = RepositoryFactory.create_fault_repository()
        equipment_repo = RepositoryFactory.create_equipment_repository()
        return FaultService(fault_repo, equipment_repo)
```

**Benefits**:
- Dependency injection
- Easy testing (can mock factories)
- Single point of object creation
- Loose coupling

**Usage Example**:
```python
# In controllers
fault_service = ServiceFactory.create_fault_service()
```

### 2.2 Strategy Pattern

**Location**: `app/patterns/strategy.py`

**Purpose**: Encapsulate algorithms and make them interchangeable

**Implementation**:
```python
class EscalationStrategy(ABC):
    @abstractmethod
    def should_escalate(self, fault: Fault) -> bool:
        pass
    
    @abstractmethod
    def get_target_role(self, current_role: str) -> str:
        pass

class SeverityBasedEscalation(EscalationStrategy):
    def should_escalate(self, fault: Fault) -> bool:
        return fault.severity in ['high', 'critical']
```

**Benefits**:
- Open/Closed Principle: Add new strategies without modifying existing code
- Runtime algorithm selection
- Eliminates conditional logic

**Usage Example**:
```python
# In EscalationService
if strategy_type == "severity":
    strategy = SeverityBasedEscalation()
else:
    strategy = TimeBasedEscalation()
```

### 2.3 Repository Pattern

**Location**: `app/repositories/`

**Purpose**: Abstract data access layer

**Implementation**:
```python
class BaseRepository(ABC):
    def __init__(self):
        self.db = DatabaseConnection()
        self.conn = self.db.get_connection()
    
    def find_by_id(self, id: int):
        # Implementation
        pass

class UserRepository(BaseRepository):
    def find_by_username(self, username: str) -> User:
        query = "SELECT * FROM users WHERE username = ?"
        row = self.fetch_one(query, (username,))
        return User.from_dict(self.dict_to_row(row))
```

**Benefits**:
- Testability (can mock repositories)
- Database independence
- Single Responsibility
- Easy to swap data sources

### 2.4 Service Layer Pattern

**Location**: `app/services/`

**Purpose**: Encapsulate business logic

**Implementation**:
```python
class FaultService:
    def __init__(self, fault_repo, equipment_repo):
        self.fault_repository = fault_repo
        self.equipment_repository = equipment_repo
    
    def report_fault(self, equipment_id, reported_by, description, severity):
        # Business logic
        equipment = self.equipment_repository.find_by_id(equipment_id)
        if not equipment:
            raise ValueError("Equipment not found")
        
        fault = Fault(...)
        fault_id = self.fault_repository.create(fault)
        
        # Update equipment status
        equipment.status = "faulty"
        self.equipment_repository.update(equipment)
        
        return fault
```

**Benefits**:
- Reusable business logic
- Transaction management
- Business rule centralization
- Testable business logic

### 2.5 Observer Pattern

**Location**: `app/patterns/observer.py`

**Purpose**: Implement event-driven architecture

**Implementation**:
```python
class Subject:
    def __init__(self):
        self._observers = []
    
    def notify(self, event_type: str, data: dict):
        for observer in self._observers:
            observer.update(event_type, data)

class NotificationObserver(Observer):
    def update(self, event_type: str, data: dict):
        if event_type == 'fault_reported':
            self._handle_fault_reported(data)
```

**Benefits**:
- Loose coupling between components
- Event-driven communication
- Easy to add new observers
- Decoupled notification system

### 2.6 Singleton Pattern

**Location**: `app/database/db_connection.py`

**Purpose**: Ensure single database connection instance

**Implementation**:
```python
class DatabaseConnection:
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
```

**Benefits**:
- Resource management
- Single connection point
- Memory efficiency
- Thread-safe database access

### 2.7 Template Method Pattern

**Location**: `app/patterns/template_method.py`

**Purpose**: Define algorithm skeleton with customizable steps

**Implementation**:
```python
class ReportGenerator(ABC):
    def generate_report(self, report: ResolutionReport) -> str:
        header = self._generate_header(report)
        body = self._generate_body(report)
        footer = self._generate_footer(report)
        return self._combine_sections(header, body, footer)
    
    @abstractmethod
    def _generate_header(self, report): pass
    
    @abstractmethod
    def _generate_body(self, report): pass

class HTMLReportGenerator(ReportGenerator):
    def _generate_header(self, report):
        return f"<html>..."
```

**Benefits**:
- Code reuse
- Consistent algorithm structure
- Easy to add new formats
- DRY principle

## 3. SOLID Principles Application

### Single Responsibility Principle (SRP)

**Example**: Each class has one reason to change
- `UserRepository`: Only user data access
- `AuthService`: Only authentication logic
- `FaultController`: Only fault request handling

### Open/Closed Principle (OCP)

**Example**: Strategy Pattern allows extension without modification
```python
# Can add new escalation strategy without changing EscalationService
class CustomEscalationStrategy(EscalationStrategy):
    # New implementation
    pass
```

### Liskov Substitution Principle (LSP)

**Example**: All repository implementations are interchangeable
```python
# Can substitute any repository implementation
user_repo = UserRepository()  # or MockUserRepository in tests
```

### Interface Segregation Principle (ISP)

**Example**: Small, focused interfaces
```python
# Observer interface is minimal
class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, data: dict):
        pass
```

### Dependency Inversion Principle (DIP)

**Example**: High-level modules depend on abstractions
```python
# Service depends on repository abstraction, not concrete implementation
class FaultService:
    def __init__(self, fault_repo: FaultRepository):
        self.fault_repository = fault_repo
```

## 4. Frontend Architecture

### Component-Based Structure

**Base Template** (`base.html`):
- Sidebar navigation
- Top navbar
- Notification system
- User profile section

**Role-Specific Templates**:
- Each role has its own dashboard
- Inherits from base template
- Role-specific menu items
- Role-specific data views

### JavaScript Architecture

**Main.js** (`app/static/js/main.js`):
- Initialization functions
- Notification system
- Toast notifications
- Form helpers
- Date formatting utilities

**Template-Specific JS**:
- Form submission handlers
- Dynamic data loading
- AJAX requests
- Client-side validation

## 5. Data Flow

### Request Flow:
```
HTTP Request
    ↓
Route (Blueprint)
    ↓
Controller
    ↓
Service (Business Logic)
    ↓
Repository (Data Access)
    ↓
Database
```

### Response Flow:
```
Database
    ↓
Repository (Data Mapping)
    ↓
Service (Business Processing)
    ↓
Controller (Response Formatting)
    ↓
Route (HTTP Response)
    ↓
Frontend (Template Rendering)
```

## 6. Security Architecture

### Authentication Flow:
1. User submits credentials
2. `AuthService` validates credentials
3. Session created with user data
4. Role-based redirect to dashboard

### Authorization:
- Role hierarchy: Technician < Engineer < DM < DGM
- Permission checking in controllers
- Route-level protection

### Data Security:
- Password hashing (SHA-256)
- Parameterized queries (SQL injection prevention)
- Session management
- Audit logging

## 7. Scalability Considerations

### Current Architecture Supports:
- **Horizontal Scaling**: Stateless controllers, session-based auth
- **Database Scaling**: Repository pattern allows database swap
- **Feature Addition**: Service layer makes adding features easy
- **Testing**: All layers are testable in isolation

### Future Enhancements:
- Caching layer (Redis)
- Message queue for notifications
- Microservices architecture
- API versioning

## 8. Testing Strategy

### Unit Tests:
- Test services in isolation
- Mock repositories
- Test business logic

### Integration Tests:
- Test API endpoints
- Test database operations
- Test authentication flow

### E2E Tests:
- Test complete user workflows
- Test role-based access
- Test form submissions

## 9. Algorithm Explanations

### Escalation Algorithm:
1. Check fault severity/time
2. Determine target role using strategy
3. Find available user of target role
4. Create escalation record
5. Update fault status
6. Send notifications

### Status Determination Algorithm:
1. Analyze monitoring readings
2. Compare against thresholds
3. Classify status (normal/warning/critical)
4. Update equipment status if critical

## 10. Viva Presentation Points

### Key Points to Emphasize:

1. **Clean Architecture**: Clear separation of concerns, testability
2. **Design Patterns**: 7 patterns implemented with real-world examples
3. **SOLID Principles**: Each principle demonstrated with code
4. **Scalability**: Architecture supports future growth
5. **Maintainability**: Modular, well-organized codebase
6. **Security**: Authentication, authorization, audit logging
7. **User Experience**: Role-based dashboards, real-time notifications

### Code Examples to Show:
- Factory pattern creating services
- Strategy pattern for escalations
- Repository pattern abstracting data access
- Service layer orchestrating business logic
- Observer pattern for notifications

---

**This architecture ensures:**
- ✅ Maintainability
- ✅ Testability
- ✅ Scalability
- ✅ Security
- ✅ Code Reusability
- ✅ Separation of Concerns




