# APDS Class Diagram

This document contains a comprehensive class diagram of the APDS (Asset Performance and Data System) project, showing all classes, their relationships, and the layered architecture.

## Architecture Overview

The APDS system follows a layered architecture pattern with:
- **Models Layer**: Domain entities (dataclasses)
- **Repository Layer**: Data access abstraction
- **Service Layer**: Business logic
- **Controller Layer**: Request handling
- **Design Patterns**: Factory, Observer, Strategy, Template Method
- **Database Layer**: Singleton connection management

## Class Diagram

```mermaid
classDiagram
    %% Models Layer - Domain Entities
    class User {
        +int id
        +str username
        +str email
        +str password_hash
        +str role
        +str full_name
        +datetime created_at
        +bool is_active
        +from_dict(data) User
        +to_dict() dict
        +has_permission(role) bool
    }

    class Equipment {
        +int id
        +str equipment_code
        +str equipment_name
        +str equipment_type
        +str location
        +str status
        +date last_maintenance_date
        +date next_maintenance_date
        +datetime created_at
        +from_dict(data) Equipment
        +to_dict() dict
    }

    class Fault {
        +int id
        +int equipment_id
        +int reported_by
        +str fault_description
        +str severity
        +str status
        +datetime reported_at
        +datetime resolved_at
        +from_dict(data) Fault
        +to_dict() dict
    }

    class DailyMonitoring {
        +int id
        +int equipment_id
        +int technician_id
        +date monitoring_date
        +str shift
        +float voltage
        +float current
        +float power_factor
        +str operational_status
        +str observations
        +datetime created_at
        +from_dict(data) DailyMonitoring
        +to_dict() dict
    }

    class RootCauseAnalysis {
        +int id
        +int fault_id
        +int analyzed_by
        +str root_cause
        +str contributing_factors
        +datetime analysis_date
        +from_dict(data) RootCauseAnalysis
        +to_dict() dict
    }

    class ResolutionReport {
        +int id
        +int fault_id
        +int rca_id
        +int prepared_by
        +str resolution_description
        +str actions_taken
        +str preventive_measures
        +str status
        +datetime created_at
        +int approved_by
        +datetime approved_at
        +from_dict(data) ResolutionReport
        +to_dict() dict
    }

    class Notification {
        +int id
        +int user_id
        +str title
        +str message
        +str notification_type
        +bool is_read
        +str related_entity_type
        +int related_entity_id
        +datetime created_at
        +from_dict(data) Notification
        +to_dict() dict
    }

    class Escalation {
        +int id
        +int fault_id
        +int escalated_from
        +int escalated_to
        +str escalation_reason
        +int escalation_level
        +str status
        +datetime escalated_at
        +datetime resolved_at
        +from_dict(data) Escalation
        +to_dict() dict
    }

    class PerformanceReport {
        +int id
        +int technician_id
        +date report_period_start
        +date report_period_end
        +str report_type
        +str analysis
        +str recommendations
        +str status
        +datetime submitted_at
        +int approved_by
        +datetime approved_at
        +datetime created_at
        +from_dict(data) PerformanceReport
        +to_dict() dict
    }

    class TechnicalReference {
        +int id
        +int equipment_id
        +int engineer_id
        +str reference_type
        +str document_name
        +str document_version
        +str findings
        +str relevance
        +str conclusions
        +datetime created_at
        +from_dict(data) TechnicalReference
        +to_dict() dict
    }

    class DocumentationPackage {
        +int id
        +int fault_id
        +int engineer_id
        +str package_name
        +str documentation_type
        +str status
        +datetime completion_date
        +datetime submitted_at
        +int approved_by
        +datetime approved_at
        +datetime created_at
        +from_dict(data) DocumentationPackage
        +to_dict() dict
    }

    class DocumentationItem {
        +int id
        +int package_id
        +str document_name
        +str document_type
        +str content
        +str version
        +str status
        +datetime created_at
        +from_dict(data) DocumentationItem
        +to_dict() dict
    }

    class DeliveryServiceVerification {
        +int id
        +int vendor_id
        +int equipment_id
        +str verification_type
        +date delivery_date
        +date service_date
        +int engineer_id
        +int dgm_id
        +str quality_assessment
        +str compliance_status
        +str verification_status
        +int verified_by
        +datetime verified_at
        +str supporting_documents
        +datetime created_at
        +from_dict(data) DeliveryServiceVerification
        +to_dict() dict
    }

    class DataReverification {
        +int id
        +int original_monitoring_id
        +int technician_id
        +int engineer_id
        +date verification_date
        +float original_voltage
        +float original_current
        +float original_power_factor
        +float new_voltage
        +float new_current
        +float new_power_factor
        +float variance_voltage
        +float variance_current
        +float variance_power_factor
        +str tolerance_levels
        +str comparison_results
        +str status
        +bool engineer_approval
        +datetime created_at
        +from_dict(data) DataReverification
        +to_dict() dict
    }

    class Vendor {
        +int id
        +str vendor_name
        +str contact_info
        +str material_list
        +str vendor_code
        +bool is_active
        +datetime created_at
        +from_dict(data) Vendor
        +to_dict() dict
    }

    class AuditLog {
        +int id
        +int user_id
        +str action
        +str entity_type
        +int entity_id
        +str old_values
        +str new_values
        +str ip_address
        +str user_agent
        +datetime created_at
        +from_dict(data) AuditLog
        +to_dict() dict
    }

    %% Repository Layer
    class BaseRepository {
        <<abstract>>
        #DatabaseConnection db
        #sqlite3.Connection conn
        +execute_query(query, params) cursor
        +execute_many(query, params_list) cursor
        +commit() void
        +fetch_one(query, params) row
        +fetch_all(query, params) rows
        +dict_to_row(row) dict
        +rows_to_dicts(rows) list
    }

    class UserRepository {
        +create(user) int
        +find_by_id(id) User
        +find_by_username(username) User
        +find_by_email(email) User
        +find_all() list
        +update(user) bool
        +delete(id) bool
    }

    class EquipmentRepository {
        +create(equipment) int
        +find_by_id(id) Equipment
        +find_all() list
        +update(equipment) bool
        +delete(id) bool
    }

    class FaultRepository {
        +create(fault) int
        +find_by_id(id) Fault
        +find_all(limit) list
        +find_by_status(status) list
        +find_by_equipment(equipment_id) list
        +find_by_severity(severity) list
        +find_unresolved() list
        +update(fault) bool
    }

    class MonitoringRepository {
        +create(monitoring) int
        +find_by_id(id) DailyMonitoring
        +find_all(limit) list
        +find_by_equipment(equipment_id) list
        +find_by_technician(technician_id) list
        +update(monitoring) bool
        +delete(id) bool
    }

    class RCARepository {
        +create(rca) int
        +find_by_id(id) RootCauseAnalysis
        +find_by_fault(fault_id) RootCauseAnalysis
        +find_all() list
    }

    class ReportRepository {
        +create(report) int
        +find_by_id(id) ResolutionReport
        +find_by_fault(fault_id) ResolutionReport
        +find_pending_approval() list
        +update(report) bool
    }

    class NotificationRepository {
        +create(notification) int
        +find_by_id(id) Notification
        +find_by_user(user_id, unread_only) list
        +mark_as_read(id) bool
        +mark_all_read(user_id) bool
        +get_unread_count(user_id) int
    }

    class EscalationRepository {
        +create(escalation) int
        +find_by_id(id) Escalation
        +find_by_fault(fault_id) list
        +find_pending() list
        +update(escalation) bool
    }

    class PerformanceReportRepository {
        +create(report) int
        +find_by_id(id) PerformanceReport
        +find_by_technician(technician_id) list
        +find_pending_approval() list
        +update(report) bool
    }

    class TechnicalReferenceRepository {
        +create(reference) int
        +find_by_id(id) TechnicalReference
        +find_by_equipment(equipment_id) list
        +find_by_engineer(engineer_id) list
        +find_all() list
    }

    class DocumentationPackageRepository {
        +create(package) int
        +find_by_id(id) DocumentationPackage
        +find_by_fault(fault_id) list
        +find_by_engineer(engineer_id) list
        +find_pending_submission() list
        +find_pending_approval() list
        +update(package) bool
    }

    class DeliveryVerificationRepository {
        +create(verification) int
        +find_by_id(id) DeliveryServiceVerification
        +find_by_vendor(vendor_id) list
        +find_pending() list
        +update(verification) bool
    }

    class DataReverificationRepository {
        +create(reverification) int
        +find_by_id(id) DataReverification
        +find_pending_approval() list
        +update(reverification) bool
    }

    class VendorRepository {
        +create(vendor) int
        +find_by_id(id) Vendor
        +find_all(active_only) list
        +update(vendor) bool
        +deactivate(id) bool
        +activate(id) bool
    }

    class AuditRepository {
        +create(log) int
        +find_by_id(id) AuditLog
        +find_by_user(user_id) list
        +find_by_entity(entity_type, entity_id) list
        +find_all(limit) list
    }

    %% Service Layer
    class AuthService {
        -UserRepository user_repository
        +login(username, password) dict
        +logout() void
        +register(user_data) dict
        +verify_password(password_hash, password) bool
        +hash_password(password) str
    }

    class MonitoringService {
        -MonitoringRepository monitoring_repository
        -EquipmentRepository equipment_repository
        +create_monitoring(data) DailyMonitoring
        +get_monitoring(id) DailyMonitoring
        +get_equipment_history(equipment_id) list
        +get_technician_history(technician_id) list
        +update_monitoring(id, data) DailyMonitoring
        +delete_monitoring(id) bool
    }

    class FaultService {
        -FaultRepository fault_repository
        -EquipmentRepository equipment_repository
        +report_fault(equipment_id, reported_by, description, severity) Fault
        +get_fault_by_id(id) Fault
        +get_all_faults(limit) list
        +get_faults_by_status(status) list
        +get_faults_by_equipment(equipment_id) list
        +get_unresolved_faults() list
        +update_fault_status(id, status) Fault
    }

    class EscalationService {
        -EscalationRepository escalation_repository
        -FaultRepository fault_repository
        -UserRepository user_repository
        +escalate_fault(fault_id, escalated_from, reason) Escalation
        +get_escalation(id) Escalation
        +get_escalations_by_fault(fault_id) list
        +get_pending_escalations() list
        +resolve_escalation(id) Escalation
    }

    class NotificationService {
        -NotificationRepository notification_repository
        +create_notification(user_id, title, message, type) Notification
        +create_notification_for_role(role, title, message, type) void
        +get_user_notifications(user_id, unread_only) list
        +mark_as_read(id) bool
        +mark_all_as_read(user_id) bool
        +get_unread_count(user_id) int
    }

    class ReportService {
        -ReportRepository report_repository
        -RCARepository rca_repository
        -FaultRepository fault_repository
        +create_draft_report(data) ResolutionReport
        +submit_for_approval(report_id) ResolutionReport
        +approve_report(report_id, approved_by) ResolutionReport
        +get_report(id) ResolutionReport
        +get_all_pending_reports() list
    }

    class PerformanceReportService {
        -PerformanceReportRepository report_repository
        -MonitoringRepository monitoring_repository
        +create_draft_report(data) PerformanceReport
        +compile_report_data(data) dict
        +submit_for_approval(report_id) PerformanceReport
        +approve_report(report_id, approved_by) PerformanceReport
        +get_pending_approval() list
    }

    class DataReverificationService {
        -DataReverificationRepository reverification_repository
        -MonitoringRepository monitoring_repository
        +create_reverification(data) DataReverification
        +approve_reverification(id, engineer_id) DataReverification
        +get_pending_approval() list
    }

    class TechnicalReferenceService {
        -TechnicalReferenceRepository reference_repository
        +create_reference(data) TechnicalReference
        +get_reference(id) TechnicalReference
        +get_equipment_references(equipment_id) list
        +get_engineer_references(engineer_id) list
    }

    class DocumentationPackageService {
        -DocumentationPackageRepository package_repository
        -FaultRepository fault_repository
        +create_package(data) DocumentationPackage
        +add_item(package_id, item_data) DocumentationItem
        +update_item(item_id, data) DocumentationItem
        +delete_item(item_id) bool
        +complete_package(package_id) DocumentationPackage
        +submit_package(package_id) DocumentationPackage
        +approve_package(package_id, approved_by) DocumentationPackage
    }

    class DeliveryVerificationService {
        -DeliveryVerificationRepository verification_repository
        -VendorRepository vendor_repository
        -EquipmentRepository equipment_repository
        +create_verification(data) DeliveryServiceVerification
        +update_verification(id, data) DeliveryServiceVerification
        +verify(id, data) DeliveryServiceVerification
        +get_verifications_by_vendor(vendor_id) list
        +get_pending_verifications() list
    }

    class VendorService {
        -VendorRepository vendor_repository
        +create_vendor(data) Vendor
        +get_vendor(id) Vendor
        +get_all_vendors(active_only) list
        +update_vendor(id, data) Vendor
        +deactivate_vendor(id) Vendor
        +activate_vendor(id) Vendor
    }

    %% Controller Layer
    class AuthController {
        -AuthService auth_service
        +login(data) dict
        +logout() dict
        +register(data) dict
        +is_authenticated() bool
        +get_current_user() dict
    }

    class MonitoringController {
        -MonitoringService monitoring_service
        +create_monitoring(data) dict
        +get_monitoring(id) dict
        +get_equipment_history(equipment_id, limit) dict
        +get_technician_history(limit) dict
        +update_monitoring(id, data) dict
        +delete_monitoring(id) dict
    }

    class FaultController {
        -FaultService fault_service
        +report_fault(data) dict
        +get_fault(id) dict
        +get_all_faults(limit) dict
        +get_faults_by_status(status) dict
        +update_fault_status(id, status) dict
    }

    class RCAController {
        -RCARepository rca_repository
        +create_rca(data) dict
        +get_rca(id) dict
        +get_rca_by_fault(fault_id) dict
    }

    class ReportController {
        -ReportService report_service
        +create_draft_report(data) dict
        +submit_for_approval(report_id) dict
        +approve_report(report_id) dict
        +get_all_pending_reports() dict
    }

    class NotificationController {
        -NotificationService notification_service
        +get_user_notifications(unread_only) dict
        +mark_as_read(id) dict
        +mark_all_as_read() dict
        +get_unread_count() dict
    }

    class EquipmentController {
        -EquipmentRepository equipment_repository
        +get_all_equipment() dict
        +get_equipment(id) dict
        +get_equipment_by_status(status) dict
    }

    class PerformanceReportController {
        -PerformanceReportService performance_report_service
        +create_draft_report(data) dict
        +compile_report_data(data) dict
        +submit_for_approval(report_id) dict
        +approve_report(report_id) dict
        +get_pending_approval() dict
    }

    class DataReverificationController {
        -DataReverificationService reverification_service
        +create_reverification(data) dict
        +approve_reverification(id) dict
        +get_pending_approval() dict
    }

    class TechnicalReferenceController {
        -TechnicalReferenceService reference_service
        +create_reference(data) dict
        +get_equipment_references(equipment_id) dict
        +get_engineer_references() dict
    }

    class DocumentationPackageController {
        -DocumentationPackageService package_service
        +create_package(data) dict
        +get_package(id) dict
        +get_packages_by_fault(fault_id) dict
        +get_engineer_packages() dict
        +add_item(data) dict
        +update_item(id, data) dict
        +delete_item(id) dict
        +complete_package(id) dict
        +submit_package(id) dict
        +approve_package(id) dict
    }

    class DeliveryVerificationController {
        -DeliveryVerificationService verification_service
        +create_verification(data) dict
        +get_verification(id) dict
        +update_verification(id, data) dict
        +verify(id, data) dict
        +get_verifications_by_vendor(vendor_id) dict
        +get_pending_verifications() dict
    }

    class VendorController {
        -VendorService vendor_service
        +create_vendor(data) dict
        +get_vendor(id) dict
        +get_all_vendors(active_only) dict
        +update_vendor(id, data) dict
        +deactivate_vendor(id) dict
        +activate_vendor(id) dict
    }

    %% Design Patterns - Factory
    class RepositoryFactory {
        <<utility>>
        +create_user_repository() UserRepository
        +create_equipment_repository() EquipmentRepository
        +create_monitoring_repository() MonitoringRepository
        +create_fault_repository() FaultRepository
        +create_rca_repository() RCARepository
        +create_report_repository() ReportRepository
        +create_notification_repository() NotificationRepository
        +create_escalation_repository() EscalationRepository
        +create_audit_repository() AuditRepository
        +create_performance_report_repository() PerformanceReportRepository
        +create_technical_reference_repository() TechnicalReferenceRepository
        +create_vendor_repository() VendorRepository
        +create_delivery_verification_repository() DeliveryVerificationRepository
        +create_data_reverification_repository() DataReverificationRepository
        +create_documentation_package_repository() DocumentationPackageRepository
    }

    class ServiceFactory {
        <<utility>>
        +create_auth_service() AuthService
        +create_monitoring_service() MonitoringService
        +create_fault_service() FaultService
        +create_escalation_service() EscalationService
        +create_notification_service() NotificationService
        +create_report_service() ReportService
        +create_performance_report_service() PerformanceReportService
        +create_data_reverification_service() DataReverificationService
        +create_technical_reference_service() TechnicalReferenceService
        +create_documentation_package_service() DocumentationPackageService
        +create_delivery_verification_service() DeliveryVerificationService
        +create_vendor_service() VendorService
    }

    %% Design Patterns - Observer
    class Observer {
        <<interface>>
        +update(event_type, data) void
    }

    class Subject {
        -List~Observer~ observers
        +attach(observer) void
        +detach(observer) void
        +notify(event_type, data) void
    }

    class NotificationObserver {
        -NotificationService notification_service
        +update(event_type, data) void
        -_handle_fault_reported(data) void
        -_handle_fault_escalated(data) void
        -_handle_report_pending(data) void
        -_handle_report_approved(data) void
    }

    %% Design Patterns - Strategy
    class EscalationStrategy {
        <<interface>>
        +should_escalate(fault) bool
        +get_target_role(current_role) str
    }

    class SeverityBasedEscalation {
        +should_escalate(fault) bool
        +get_target_role(current_role) str
    }

    class TimeBasedEscalation {
        -int hours_threshold
        +should_escalate(fault) bool
        +get_target_role(current_role) str
    }

    class NotificationStrategy {
        <<interface>>
        +send_notification(user_id, title, message, type) void
    }

    class ImmediateNotificationStrategy {
        -NotificationService notification_service
        +send_notification(user_id, title, message, type) void
    }

    %% Design Patterns - Template Method
    class ReportGenerator {
        <<abstract>>
        +generate_report(report) str
        #_generate_header(report) str
        #_generate_body(report) str
        #_generate_footer(report) str
        #_combine_sections(header, body, footer) str
    }

    class HTMLReportGenerator {
        #_generate_header(report) str
        #_generate_body(report) str
        #_generate_footer(report) str
    }

    class PlainTextReportGenerator {
        #_generate_header(report) str
        #_generate_body(report) str
    }

    %% Database Layer
    class DatabaseConnection {
        <<singleton>>
        -DatabaseConnection _instance
        -sqlite3.Connection _connection
        +get_connection() Connection
        +init_app(app) void
        +close() void
        -_create_tables() void
        -_check_database_accessible(path) bool
    }

    %% Relationships - Repository Inheritance
    BaseRepository <|-- UserRepository
    BaseRepository <|-- EquipmentRepository
    BaseRepository <|-- FaultRepository
    BaseRepository <|-- MonitoringRepository
    BaseRepository <|-- RCARepository
    BaseRepository <|-- ReportRepository
    BaseRepository <|-- NotificationRepository
    BaseRepository <|-- EscalationRepository
    BaseRepository <|-- PerformanceReportRepository
    BaseRepository <|-- TechnicalReferenceRepository
    BaseRepository <|-- DocumentationPackageRepository
    BaseRepository <|-- DeliveryVerificationRepository
    BaseRepository <|-- DataReverificationRepository
    BaseRepository <|-- VendorRepository
    BaseRepository <|-- AuditRepository

    %% Relationships - Repository uses DatabaseConnection
    BaseRepository --> DatabaseConnection : uses

    %% Relationships - Service uses Repository
    AuthService --> UserRepository : uses
    MonitoringService --> MonitoringRepository : uses
    MonitoringService --> EquipmentRepository : uses
    FaultService --> FaultRepository : uses
    FaultService --> EquipmentRepository : uses
    EscalationService --> EscalationRepository : uses
    EscalationService --> FaultRepository : uses
    EscalationService --> UserRepository : uses
    NotificationService --> NotificationRepository : uses
    ReportService --> ReportRepository : uses
    ReportService --> RCARepository : uses
    ReportService --> FaultRepository : uses
    PerformanceReportService --> PerformanceReportRepository : uses
    PerformanceReportService --> MonitoringRepository : uses
    DataReverificationService --> DataReverificationRepository : uses
    DataReverificationService --> MonitoringRepository : uses
    TechnicalReferenceService --> TechnicalReferenceRepository : uses
    DocumentationPackageService --> DocumentationPackageRepository : uses
    DocumentationPackageService --> FaultRepository : uses
    DeliveryVerificationService --> DeliveryVerificationRepository : uses
    DeliveryVerificationService --> VendorRepository : uses
    DeliveryVerificationService --> EquipmentRepository : uses
    VendorService --> VendorRepository : uses

    %% Relationships - Controller uses Service
    AuthController --> AuthService : uses
    MonitoringController --> MonitoringService : uses
    FaultController --> FaultService : uses
    ReportController --> ReportService : uses
    NotificationController --> NotificationService : uses
    PerformanceReportController --> PerformanceReportService : uses
    DataReverificationController --> DataReverificationService : uses
    TechnicalReferenceController --> TechnicalReferenceService : uses
    DocumentationPackageController --> DocumentationPackageService : uses
    DeliveryVerificationController --> DeliveryVerificationService : uses
    VendorController --> VendorService : uses

    %% Relationships - Controller uses Repository (direct access)
    RCAController --> RCARepository : uses
    EquipmentController --> EquipmentRepository : uses

    %% Relationships - Factory creates Repositories and Services
    RepositoryFactory ..> UserRepository : creates
    RepositoryFactory ..> EquipmentRepository : creates
    RepositoryFactory ..> MonitoringRepository : creates
    RepositoryFactory ..> FaultRepository : creates
    RepositoryFactory ..> RCARepository : creates
    RepositoryFactory ..> ReportRepository : creates
    RepositoryFactory ..> NotificationRepository : creates
    RepositoryFactory ..> EscalationRepository : creates
    RepositoryFactory ..> PerformanceReportRepository : creates
    RepositoryFactory ..> TechnicalReferenceRepository : creates
    RepositoryFactory ..> VendorRepository : creates
    RepositoryFactory ..> DeliveryVerificationRepository : creates
    RepositoryFactory ..> DataReverificationRepository : creates
    RepositoryFactory ..> DocumentationPackageRepository : creates
    RepositoryFactory ..> AuditRepository : creates

    ServiceFactory ..> AuthService : creates
    ServiceFactory ..> MonitoringService : creates
    ServiceFactory ..> FaultService : creates
    ServiceFactory ..> EscalationService : creates
    ServiceFactory ..> NotificationService : creates
    ServiceFactory ..> ReportService : creates
    ServiceFactory ..> PerformanceReportService : creates
    ServiceFactory ..> DataReverificationService : creates
    ServiceFactory ..> TechnicalReferenceService : creates
    ServiceFactory ..> DocumentationPackageService : creates
    ServiceFactory ..> DeliveryVerificationService : creates
    ServiceFactory ..> VendorService : creates

    ServiceFactory --> RepositoryFactory : uses

    %% Relationships - Observer Pattern
    Observer <|.. NotificationObserver : implements
    Subject --> Observer : notifies
    NotificationObserver --> NotificationService : uses

    %% Relationships - Strategy Pattern
    EscalationStrategy <|.. SeverityBasedEscalation : implements
    EscalationStrategy <|.. TimeBasedEscalation : implements
    NotificationStrategy <|.. ImmediateNotificationStrategy : implements
    ImmediateNotificationStrategy --> NotificationService : uses

    %% Relationships - Template Method Pattern
    ReportGenerator <|-- HTMLReportGenerator : extends
    ReportGenerator <|-- PlainTextReportGenerator : extends

    %% Relationships - Model Associations
    Fault --> Equipment : references
    Fault --> User : reported_by
    DailyMonitoring --> Equipment : references
    DailyMonitoring --> User : technician_id
    RootCauseAnalysis --> Fault : references
    RootCauseAnalysis --> User : analyzed_by
    ResolutionReport --> Fault : references
    ResolutionReport --> RootCauseAnalysis : references
    ResolutionReport --> User : prepared_by
    ResolutionReport --> User : approved_by
    Notification --> User : references
    Escalation --> Fault : references
    Escalation --> User : escalated_from
    Escalation --> User : escalated_to
    PerformanceReport --> User : technician_id
    PerformanceReport --> User : approved_by
    TechnicalReference --> Equipment : references
    TechnicalReference --> User : engineer_id
    DocumentationPackage --> Fault : references
    DocumentationPackage --> User : engineer_id
    DocumentationPackage --> User : approved_by
    DocumentationItem --> DocumentationPackage : references
    DeliveryServiceVerification --> Vendor : references
    DeliveryServiceVerification --> Equipment : references
    DeliveryServiceVerification --> User : engineer_id
    DeliveryServiceVerification --> User : dgm_id
    DeliveryServiceVerification --> User : verified_by
    DataReverification --> DailyMonitoring : references
    DataReverification --> User : technician_id
    DataReverification --> User : engineer_id
    AuditLog --> User : references
```

## Layer Descriptions

### Models Layer
The models layer contains 16 domain entity classes, all implemented as dataclasses. These represent the core business entities in the system:
- **User**: System users with role-based access (technician, engineer, dm, dgm, vendor)
- **Equipment**: Physical equipment being monitored
- **Fault**: Equipment faults reported by users
- **DailyMonitoring**: Daily monitoring data (voltage, current, power factor)
- **RootCauseAnalysis**: RCA performed on faults
- **ResolutionReport**: Reports documenting fault resolution
- **Notification**: User notifications
- **Escalation**: Fault escalation records
- **PerformanceReport**: Performance analysis reports
- **TechnicalReference**: Technical documentation references
- **DocumentationPackage**: Documentation packages for faults
- **DocumentationItem**: Individual items within documentation packages
- **DeliveryServiceVerification**: Vendor delivery/service verification records
- **DataReverification**: Data re-verification requests
- **Vendor**: Vendor information
- **AuditLog**: System audit trail

### Repository Layer
The repository layer provides data access abstraction. All repositories inherit from `BaseRepository`, which provides common database operations. Each repository handles CRUD operations for its corresponding model.

### Service Layer
The service layer contains business logic. Services coordinate between repositories and implement domain-specific operations. Services may use multiple repositories to fulfill complex business requirements.

### Controller Layer
Controllers handle HTTP requests and responses. They use services to process requests and return appropriate responses. Controllers are responsible for request validation, session management, and response formatting.

### Design Patterns

#### Factory Pattern
- **RepositoryFactory**: Creates repository instances
- **ServiceFactory**: Creates service instances with proper dependency injection

#### Observer Pattern
- **Observer**: Abstract interface for observers
- **Subject**: Manages observer list and notifications
- **NotificationObserver**: Concrete observer that handles notification events

#### Strategy Pattern
- **EscalationStrategy**: Abstract strategy for escalation logic
  - **SeverityBasedEscalation**: Escalates based on fault severity
  - **TimeBasedEscalation**: Escalates based on time thresholds
- **NotificationStrategy**: Abstract strategy for notification delivery
  - **ImmediateNotificationStrategy**: Sends notifications immediately

#### Template Method Pattern
- **ReportGenerator**: Abstract base class defining report generation algorithm
  - **HTMLReportGenerator**: Generates HTML format reports
  - **PlainTextReportGenerator**: Generates plain text format reports

### Database Layer
- **DatabaseConnection**: Singleton pattern implementation for managing database connections. Ensures only one connection instance exists and handles connection lifecycle.

## Relationship Types

- **Inheritance** (`<|--`): Repository classes inherit from BaseRepository
- **Dependency** (`-->`): Services depend on repositories, controllers depend on services
- **Composition** (`--*`): Models reference other models (e.g., Fault references Equipment)
- **Creation** (`..>`): Factories create instances of repositories and services
- **Implementation** (`<|..`): Concrete classes implement interfaces/abstract classes

## Notes

- All model classes use dataclasses and provide `from_dict()` and `to_dict()` methods for serialization
- The repository pattern provides a clean separation between data access and business logic
- Services encapsulate business rules and coordinate between multiple repositories when needed
- Controllers are thin layers that delegate to services
- Design patterns provide flexibility and maintainability
- The singleton pattern ensures efficient database connection management

