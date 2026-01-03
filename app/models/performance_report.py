"""
Performance Report Model (UC-04)
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

@dataclass
class PerformanceReport:
    """Performance Report model"""
    id: Optional[int] = None
    technician_id: int = 0
    report_period_start: date = date.today()
    report_period_end: date = date.today()
    report_type: str = "weekly"  # weekly, monthly, custom
    analysis: Optional[str] = None
    recommendations: Optional[str] = None
    status: str = "draft"  # draft, submitted, approved, rejected
    submitted_at: Optional[datetime] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create PerformanceReport from dictionary"""
        return cls(
            id=data.get('id'),
            technician_id=data.get('technician_id', 0),
            report_period_start=datetime.fromisoformat(data['report_period_start']).date() if data.get('report_period_start') else date.today(),
            report_period_end=datetime.fromisoformat(data['report_period_end']).date() if data.get('report_period_end') else date.today(),
            report_type=data.get('report_type', 'weekly'),
            analysis=data.get('analysis'),
            recommendations=data.get('recommendations'),
            status=data.get('status', 'draft'),
            submitted_at=datetime.fromisoformat(data['submitted_at']) if data.get('submitted_at') else None,
            approved_by=data.get('approved_by'),
            approved_at=datetime.fromisoformat(data['approved_at']) if data.get('approved_at') else None,
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
    
    def to_dict(self) -> dict:
        """Convert PerformanceReport to dictionary"""
        return {
            'id': self.id,
            'technician_id': self.technician_id,
            'report_period_start': self.report_period_start.isoformat() if isinstance(self.report_period_start, date) else str(self.report_period_start),
            'report_period_end': self.report_period_end.isoformat() if isinstance(self.report_period_end, date) else str(self.report_period_end),
            'report_type': self.report_type,
            'analysis': self.analysis,
            'recommendations': self.recommendations,
            'status': self.status,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }




