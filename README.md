# Role-Based Operations & Monitoring System

A comprehensive full-stack Role-Based Operations & Monitoring System built with Python Flask, SQLite, and modern web technologies. This system implements Clean Architecture principles, SOLID design patterns, and provides role-based dashboards for different user types.

## 🏗️ Architecture Overview

### Backend Architecture (Clean Architecture)

The backend follows a layered Clean Architecture pattern:

```
app/
├── models/          # Domain models (data classes)
├── repositories/    # Data access layer (Repository Pattern)
├── services/        # Business logic layer
├── controllers/      # Request handling layer
├── routes/           # Route definitions (Flask Blueprints)
├── patterns/         # Design patterns implementation
├── algorithms/       # Business algorithms
└── database/         # Database connection and initialization
```

#### Layer Responsibilities:

1. **Models**: Domain entities with business logic
2. **Repositories**: Data persistence abstraction (Repository Pattern)
3. **Services**: Business logic and orchestration
4. **Controllers**: HTTP request/response handling
5. **Routes**: URL routing and blueprint registration

### Frontend Architecture

The frontend follows a component-based structure:

```
app/
├── templates/
│   ├── base.html           # Base template with sidebar/navbar
│   ├── auth/               # Authentication pages
│   ├── dashboards/         # Role-specific dashboards
│   ├── forms/              # Form templates
│   ├── views/              # Data view templates
│   └── reports/            # Report templates
└── static/
    ├── css/
    │   └── main.css        # Modern dashboard styling
    └── js/
        └── main.js         # Frontend JavaScript logic
```

## 🎯 Design Patterns Implemented

### 1. **Factory Pattern** (`app/patterns/factory.py`)
- `RepositoryFactory`: Creates repository instances
- `ServiceFactory`: Creates service instances with proper dependencies
- **Purpose**: Centralized object creation, dependency injection

### 2. **Strategy Pattern** (`app/patterns/strategy.py`)
- `EscalationStrategy`: Abstract base for escalation strategies
- `SeverityBasedEscalation`: Escalate based on fault severity
- `TimeBasedEscalation`: Escalate based on time thresholds
- `NotificationStrategy`: Abstract base for notification strategies
- **Purpose**: Encapsulate algorithms, make them interchangeable

### 3. **Repository Pattern** (`app/repositories/`)
- `BaseRepository`: Common database operations
- Specific repositories for each entity (User, Equipment, Fault, etc.)
- **Purpose**: Abstract data access, enable testing, maintainability

### 4. **Service Layer Pattern** (`app/services/`)
- Business logic separated from controllers
- Services orchestrate repositories
- **Purpose**: Reusable business logic, single responsibility

### 5. **Observer Pattern** (`app/patterns/observer.py`)
- `Subject`: Notifies observers of events
- `NotificationObserver`: Handles notification events
- **Purpose**: Decouple event producers from consumers

### 6. **Singleton Pattern** (`app/database/db_connection.py`)
- `DatabaseConnection`: Single database connection instance
- **Purpose**: Ensure single database connection, resource management

### 7. **Template Method Pattern** (`app/patterns/template_method.py`)
- `ReportGenerator`: Abstract report generation
- `HTMLReportGenerator`: HTML format reports
- `PlainTextReportGenerator`: Plain text format reports
- **Purpose**: Define algorithm skeleton, allow subclasses to customize steps

## 🔐 Role-Based Access Control (RBAC)

### Roles and Permissions:

1. **Technician**
   - Daily monitoring data entry
   - Equipment status viewing
   - Fault reporting
   - Access: Technician Dashboard

2. **Engineer**
   - Root cause analysis
   - Draft resolution reports
   - Fault investigation
   - Access: Engineer Dashboard

3. **Deputy Manager (DM)**
   - Report review and approval
   - Historical data analysis
   - Trend comparison
   - Access: DM Dashboard

4. **Deputy General Manager (DGM)**
   - All DM permissions
   - System-wide oversight
   - Approved reports archive
   - Access: DGM Dashboard

## 📊 Core Functionalities

### 1. Authentication & Authorization
- User login/logout
- Role-based session management
- Password hashing (SHA-256)
- Session-based authentication

### 2. Daily Monitoring
- Equipment monitoring data entry
- Temperature, pressure, vibration tracking
- Operational status classification (normal/warning/critical)
- Automatic equipment status updates

### 3. Fault Management
- Fault reporting by technicians
- Severity classification (low/medium/high/critical)
- Status tracking (reported/investigating/resolved/escalated)
- Equipment-fault association

### 4. Root Cause Analysis (RCA)
- Engineers analyze faults
- Root cause identification
- Contributing factors documentation
- Fault-RCA linkage

### 5. Resolution Reports
- Draft report creation
- Submission for approval workflow
- DM/DGM approval process
- Automatic fault resolution on approval

### 6. Escalation System
- Automatic escalation based on severity/time
- Multi-level escalation (Technician → Engineer → DM → DGM)
- Escalation history tracking
- Strategy pattern for escalation rules

### 7. Notification System
- Real-time notifications
- Role-based notification distribution
- Unread notification tracking
- Notification types (info/warning/error/success/escalation)

### 8. Audit Logging
- User action tracking
- Entity change logging
- IP address and user agent recording
- Historical audit trail

## 🗄️ Database Schema

### Core Tables:
- `users`: User accounts and roles
- `equipment`: Equipment inventory
- `daily_monitoring`: Monitoring records
- `faults`: Fault reports
- `root_cause_analysis`: RCA records
- `resolution_reports`: Resolution reports
- `notifications`: User notifications
- `escalations`: Escalation records
- `audit_logs`: Audit trail

## 🚀 Installation & Setup

### Prerequisites:
- Python 3.8+ (with pip included)
- pip (usually comes with Python)

### Steps:

1. **Clone/Download the project**

2. **Install dependencies:**

   **Windows:**
   ```powershell
   # If pip command works:
   pip install -r requirements.txt
   
   # If pip command doesn't work, use:
   python -m pip install -r requirements.txt
   # or
   py -m pip install -r requirements.txt
   ```

   **macOS/Linux:**
   ```bash
   # If pip3 command works:
   pip3 install -r requirements.txt
   
   # If pip3 command doesn't work, use:
   python3 -m pip install -r requirements.txt
   ```

   **Using Virtual Environment (Recommended):**
   ```bash
   # Create virtual environment
   python -m venv venv  # Windows
   python3 -m venv venv  # macOS/Linux
   
   # Activate it
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py  # Windows
   python3 app.py  # macOS/Linux
   ```

4. **Access the application:**
- Open browser: `http://localhost:5000`
- Database will be automatically created on first run

### Troubleshooting:

**If you get "pip not found" error:**
- See `INSTALLATION_TROUBLESHOOTING.md` for detailed solutions
- Common fixes:
  - Install Python from https://www.python.org/downloads/ (check "Add to PATH")
  - Use `python -m pip` instead of `pip`
  - Use virtual environment (recommended)

### Initial Setup:

The database is automatically initialized with tables on first run. You'll need to create initial users manually or through a setup script.

## 📁 Project Structure

```
NEW JUNIORS PROJECT/
├── app/
│   ├── __init__.py
│   ├── static/
│   │   ├── css/
│   │   │   └── main.css
│   │   └── js/
│   │       └── main.js
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   └── login.html
│   │   ├── dashboards/
│   │   │   ├── technician.html
│   │   │   ├── engineer.html
│   │   │   ├── dm.html
│   │   │   └── dgm.html
│   │   ├── forms/
│   │   │   ├── daily_monitoring.html
│   │   │   ├── equipment_status.html
│   │   │   ├── root_cause_analysis.html
│   │   │   └── draft_resolution.html
│   │   ├── views/
│   │   │   ├── monitoring_history.html
│   │   │   ├── fault_list.html
│   │   │   ├── escalation_timeline.html
│   │   │   ├── historical_data.html
│   │   │   ├── trend_comparison.html
│   │   │   └── report_review.html
│   │   └── reports/
│   │       └── approved_reports.html
│   ├── models/
│   │   ├── user.py
│   │   ├── equipment.py
│   │   ├── monitoring.py
│   │   ├── fault.py
│   │   ├── rca.py
│   │   ├── report.py
│   │   ├── notification.py
│   │   ├── escalation.py
│   │   └── audit_log.py
│   ├── repositories/
│   │   ├── base_repository.py
│   │   ├── user_repository.py
│   │   ├── equipment_repository.py
│   │   ├── monitoring_repository.py
│   │   ├── fault_repository.py
│   │   ├── rca_repository.py
│   │   ├── report_repository.py
│   │   ├── notification_repository.py
│   │   ├── escalation_repository.py
│   │   └── audit_repository.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── monitoring_service.py
│   │   ├── fault_service.py
│   │   ├── escalation_service.py
│   │   ├── notification_service.py
│   │   └── report_service.py
│   ├── controllers/
│   │   ├── auth_controller.py
│   │   ├── monitoring_controller.py
│   │   ├── fault_controller.py
│   │   ├── report_controller.py
│   │   ├── notification_controller.py
│   │   ├── equipment_controller.py
│   │   └── rca_controller.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── dashboard_routes.py
│   │   ├── api_routes.py
│   │   ├── form_routes.py
│   │   ├── view_routes.py
│   │   └── report_routes.py
│   ├── patterns/
│   │   ├── factory.py
│   │   ├── strategy.py
│   │   ├── observer.py
│   │   └── template_method.py
│   ├── algorithms/
│   └── database/
│       ├── __init__.py
│       └── db_connection.py
├── app.py
├── requirements.txt
└── README.md
```

## 🔧 SOLID Principles Applied

1. **Single Responsibility Principle (SRP)**
   - Each class has one reason to change
   - Controllers handle HTTP, Services handle business logic, Repositories handle data

2. **Open/Closed Principle (OCP)**
   - Strategy pattern allows extension without modification
   - New escalation strategies can be added without changing existing code

3. **Liskov Substitution Principle (LSP)**
   - Repository implementations are interchangeable
   - Strategy implementations follow base contract

4. **Interface Segregation Principle (ISP)**
   - Small, focused interfaces (Observer, Strategy)
   - Clients depend only on methods they use

5. **Dependency Inversion Principle (DIP)**
   - High-level modules depend on abstractions (repositories, services)
   - Factory pattern provides dependency injection

## 🎨 Frontend Features

- **Modern Dashboard UI**: Clean, responsive design
- **Role-Based Navigation**: Sidebar menus adapt to user role
- **Real-Time Notifications**: Notification dropdown with badge counts
- **Form Validation**: Client-side validation
- **AJAX/Fetch API**: Dynamic data loading
- **Toast Notifications**: User feedback system
- **Responsive Design**: Mobile-friendly layout

## 📝 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /logout` - User logout
- `GET /api/current-user` - Get current user

### Monitoring
- `POST /api/monitoring` - Create monitoring record
- `GET /api/monitoring/equipment/<id>` - Get equipment history
- `GET /api/monitoring/technician` - Get technician history

### Faults
- `POST /api/faults` - Report fault
- `GET /api/faults` - Get all faults
- `GET /api/faults/<id>` - Get fault by ID
- `PUT /api/faults/<id>/status` - Update fault status

### Reports
- `POST /api/reports` - Create draft report
- `POST /api/reports/<id>/submit` - Submit for approval
- `POST /api/reports/<id>/approve` - Approve report
- `GET /api/reports/pending` - Get pending reports

### Notifications
- `GET /api/notifications` - Get user notifications
- `POST /api/notifications/<id>/read` - Mark as read
- `POST /api/notifications/read-all` - Mark all as read
- `GET /api/notifications/unread-count` - Get unread count

## 🔍 Algorithms

### Escalation Algorithm
- Severity-based: Escalates high/critical faults automatically
- Time-based: Escalates faults older than threshold (24 hours default)
- Multi-level: Technician → Engineer → DM → DGM

### Status Determination Algorithm
- Monitoring data analysis
- Automatic status classification based on readings
- Equipment status updates on critical conditions

## 🧪 Testing Recommendations

1. **Unit Tests**: Test services and repositories in isolation
2. **Integration Tests**: Test API endpoints
3. **E2E Tests**: Test complete user workflows
4. **Role-Based Tests**: Verify RBAC functionality

## 📚 Viva Presentation Points

1. **Architecture**: Explain Clean Architecture layers
2. **Design Patterns**: Demonstrate each pattern with examples
3. **SOLID Principles**: Show how each principle is applied
4. **RBAC**: Explain role hierarchy and permissions
5. **Scalability**: Discuss how architecture supports growth
6. **Maintainability**: Show separation of concerns

## 🔐 Security Considerations

- Password hashing (SHA-256)
- Session-based authentication
- SQL injection prevention (parameterized queries)
- Role-based access control
- Audit logging for compliance

## 🚧 Future Enhancements

- Email notifications
- PDF report generation
- Data visualization charts
- Export functionality
- Advanced search and filtering
- Real-time updates (WebSockets)

## 📄 License

This project is created for educational purposes as a Final Year Project.

## 👨‍💻 Development Notes

- Database: SQLite (can be migrated to PostgreSQL/MySQL)
- Frontend: Vanilla JavaScript (can be enhanced with frameworks)
- Styling: Custom CSS (can use Bootstrap/Tailwind)
- Backend: Flask (can be extended with Flask-RESTful)

---

**Built with ❤️ for Final Year Project**




