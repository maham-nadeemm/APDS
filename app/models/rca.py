"""
Root Cause Analysis Model
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class RootCauseAnalysis:
    """Root Cause Analysis model"""
    id: Optional[int] = None
    fault_id: int = 0
    analyzed_by: int = 0
    root_cause: str = ""
    contributing_factors: Optional[str] = None
    analysis_date: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create RootCauseAnalysis from dictionary"""
        return cls(
            id=data.get('id'),
            fault_id=data.get('fault_id', 0),
            analyzed_by=data.get('analyzed_by', 0),
            root_cause=data.get('root_cause', ''),
            contributing_factors=data.get('contributing_factors'),
            analysis_date=datetime.fromisoformat(data['analysis_date']) if data.get('analysis_date') else None
        )
    
    def to_dict(self) -> dict:
        """Convert RootCauseAnalysis to dictionary"""
        return {
            'id': self.id,
            'fault_id': self.fault_id,
            'analyzed_by': self.analyzed_by,
            'root_cause': self.root_cause,
            'contributing_factors': self.contributing_factors,
            'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None
        }




