"""
Factory Pattern Implementation
"""
from app.repositories.user_repository import UserRepository
from app.repositories.equipment_repository import EquipmentRepository
from app.repositories.monitoring_repository import MonitoringRepository
from app.repositories.fault_repository import FaultRepository
from app.repositories.rca_repository import RCARepository
from app.repositories.report_repository import ReportRepository
from app.repositories.notification_repository import NotificationRepository
from app.repositories.escalation_repository import EscalationRepository
from app.repositories.audit_repository import AuditRepository
from app.repositories.performance_report_repository import PerformanceReportRepository
from app.repositories.technical_reference_repository import TechnicalReferenceRepository
from app.repositories.vendor_repository import VendorRepository
from app.repositories.delivery_verification_repository import DeliveryVerificationRepository
from app.repositories.data_reverification_repository import DataReverificationRepository
from app.repositories.documentation_package_repository import DocumentationPackageRepository

from app.services.auth_service import AuthService
from app.services.performance_report_service import PerformanceReportService
from app.services.data_reverification_service import DataReverificationService
from app.services.technical_reference_service import TechnicalReferenceService
from app.services.monitoring_service import MonitoringService
from app.services.fault_service import FaultService
from app.services.escalation_service import EscalationService
from app.services.notification_service import NotificationService
from app.services.report_service import ReportService
from app.services.documentation_package_service import DocumentationPackageService
from app.services.delivery_verification_service import DeliveryVerificationService
from app.services.vendor_service import VendorService

class RepositoryFactory:
    """Factory for creating repository instances"""
    
    @staticmethod
    def create_user_repository():
        return UserRepository()
    
    @staticmethod
    def create_equipment_repository():
        return EquipmentRepository()
    
    @staticmethod
    def create_monitoring_repository():
        return MonitoringRepository()
    
    @staticmethod
    def create_fault_repository():
        return FaultRepository()
    
    @staticmethod
    def create_rca_repository():
        return RCARepository()
    
    @staticmethod
    def create_report_repository():
        return ReportRepository()
    
    @staticmethod
    def create_notification_repository():
        return NotificationRepository()
    
    @staticmethod
    def create_escalation_repository():
        return EscalationRepository()
    
    @staticmethod
    def create_audit_repository():
        return AuditRepository()
    
    @staticmethod
    def create_performance_report_repository():
        return PerformanceReportRepository()
    
    @staticmethod
    def create_technical_reference_repository():
        return TechnicalReferenceRepository()
    
    @staticmethod
    def create_vendor_repository():
        return VendorRepository()
    
    @staticmethod
    def create_delivery_verification_repository():
        return DeliveryVerificationRepository()
    
    @staticmethod
    def create_data_reverification_repository():
        return DataReverificationRepository()
    
    @staticmethod
    def create_documentation_package_repository():
        return DocumentationPackageRepository()

class ServiceFactory:
    """Factory for creating service instances"""
    
    @staticmethod
    def create_auth_service():
        repo = RepositoryFactory.create_user_repository()
        return AuthService(repo)
    
    @staticmethod
    def create_monitoring_service():
        monitoring_repo = RepositoryFactory.create_monitoring_repository()
        equipment_repo = RepositoryFactory.create_equipment_repository()
        return MonitoringService(monitoring_repo, equipment_repo)
    
    @staticmethod
    def create_fault_service():
        fault_repo = RepositoryFactory.create_fault_repository()
        equipment_repo = RepositoryFactory.create_equipment_repository()
        return FaultService(fault_repo, equipment_repo)
    
    @staticmethod
    def create_escalation_service():
        escalation_repo = RepositoryFactory.create_escalation_repository()
        fault_repo = RepositoryFactory.create_fault_repository()
        user_repo = RepositoryFactory.create_user_repository()
        return EscalationService(escalation_repo, fault_repo, user_repo)
    
    @staticmethod
    def create_notification_service():
        notification_repo = RepositoryFactory.create_notification_repository()
        return NotificationService(notification_repo)
    
    @staticmethod
    def create_report_service():
        report_repo = RepositoryFactory.create_report_repository()
        rca_repo = RepositoryFactory.create_rca_repository()
        fault_repo = RepositoryFactory.create_fault_repository()
        return ReportService(report_repo, rca_repo, fault_repo)
    
    @staticmethod
    def create_performance_report_service():
        report_repo = RepositoryFactory.create_performance_report_repository()
        monitoring_repo = RepositoryFactory.create_monitoring_repository()
        return PerformanceReportService(report_repo, monitoring_repo)
    
    @staticmethod
    def create_data_reverification_service():
        reverification_repo = RepositoryFactory.create_data_reverification_repository()
        monitoring_repo = RepositoryFactory.create_monitoring_repository()
        return DataReverificationService(reverification_repo, monitoring_repo)
    
    @staticmethod
    def create_technical_reference_service():
        reference_repo = RepositoryFactory.create_technical_reference_repository()
        return TechnicalReferenceService(reference_repo)
    
    @staticmethod
    def create_documentation_package_service():
        package_repo = RepositoryFactory.create_documentation_package_repository()
        fault_repo = RepositoryFactory.create_fault_repository()
        return DocumentationPackageService(package_repo, fault_repo)
    
    @staticmethod
    def create_delivery_verification_service():
        verification_repo = RepositoryFactory.create_delivery_verification_repository()
        vendor_repo = RepositoryFactory.create_vendor_repository()
        equipment_repo = RepositoryFactory.create_equipment_repository()
        return DeliveryVerificationService(verification_repo, vendor_repo, equipment_repo)
    
    @staticmethod
    def create_vendor_service():
        vendor_repo = RepositoryFactory.create_vendor_repository()
        return VendorService(vendor_repo)
