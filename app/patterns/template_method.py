"""
Template Method Pattern Implementation
"""
from abc import ABC, abstractmethod
from app.models.report import ResolutionReport

class ReportGenerator(ABC):
    """Abstract base class for report generation"""
    
    def generate_report(self, report: ResolutionReport) -> str:
        """Template method that defines the algorithm structure"""
        header = self._generate_header(report)
        body = self._generate_body(report)
        footer = self._generate_footer(report)
        return self._combine_sections(header, body, footer)
    
    @abstractmethod
    def _generate_header(self, report: ResolutionReport) -> str:
        """Generate report header"""
        pass
    
    @abstractmethod
    def _generate_body(self, report: ResolutionReport) -> str:
        """Generate report body"""
        pass
    
    def _generate_footer(self, report: ResolutionReport) -> str:
        """Generate report footer (can be overridden)"""
        return f"\n--- End of Report ---\nGenerated on: {report.created_at}"
    
    def _combine_sections(self, header: str, body: str, footer: str) -> str:
        """Combine report sections"""
        return f"{header}\n\n{body}\n\n{footer}"

class HTMLReportGenerator(ReportGenerator):
    """HTML format report generator"""
    
    def _generate_header(self, report: ResolutionReport) -> str:
        return f"""
        <html>
        <head>
            <title>Resolution Report #{report.id}</title>
        </head>
        <body>
            <h1>Resolution Report</h1>
            <p><strong>Report ID:</strong> {report.id}</p>
            <p><strong>Fault ID:</strong> {report.fault_id}</p>
        """
    
    def _generate_body(self, report: ResolutionReport) -> str:
        return f"""
            <h2>Resolution Description</h2>
            <p>{report.resolution_description}</p>
            
            <h2>Actions Taken</h2>
            <p>{report.actions_taken}</p>
            
            <h2>Preventive Measures</h2>
            <p>{report.preventive_measures or 'N/A'}</p>
        """
    
    def _generate_footer(self, report: ResolutionReport) -> str:
        return f"""
            <hr>
            <p><em>Report Status: {report.status}</em></p>
            <p><em>Generated on: {report.created_at}</em></p>
        </body>
        </html>
        """

class PlainTextReportGenerator(ReportGenerator):
    """Plain text format report generator"""
    
    def _generate_header(self, report: ResolutionReport) -> str:
        return f"""
RESOLUTION REPORT
=================
Report ID: {report.id}
Fault ID: {report.fault_id}
Status: {report.status}
"""
    
    def _generate_body(self, report: ResolutionReport) -> str:
        return f"""
RESOLUTION DESCRIPTION
----------------------
{report.resolution_description}

ACTIONS TAKEN
-------------
{report.actions_taken}

PREVENTIVE MEASURES
-------------------
{report.preventive_measures or 'N/A'}
"""




