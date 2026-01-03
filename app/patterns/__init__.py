"""
Design Patterns Package
"""
from app.patterns.factory import RepositoryFactory, ServiceFactory
from app.patterns.strategy import EscalationStrategy, NotificationStrategy
from app.patterns.observer import NotificationObserver, Subject
from app.database.db_connection import DatabaseConnection
from app.patterns.template_method import ReportGenerator

__all__ = [
    'RepositoryFactory',
    'ServiceFactory',
    'EscalationStrategy',
    'NotificationStrategy',
    'NotificationObserver',
    'Subject',
    'DatabaseConnection',
    'ReportGenerator'
]

