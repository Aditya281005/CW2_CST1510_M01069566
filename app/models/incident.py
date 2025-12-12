"""
Incident Model Class - Demonstrates OOP Encapsulation and Business Logic
"""
from typing import Dict, Any, Optional
from datetime import datetime
from .base_model import BaseModel


class Incident(BaseModel):
    """
    Incident model representing a cyber security incident.
    
    OOP Principles Demonstrated:
    - Inheritance: Extends BaseModel
    - Encapsulation: Private attributes with validation
    - Business Logic: Status transitions and severity checks
    """
    
    # Class variables (shared across all instances)
    VALID_SEVERITIES = ['low', 'medium', 'high', 'critical']
    VALID_STATUSES = ['open', 'investigating', 'resolved', 'closed']
    
    def __init__(
        self,
        title: str,
        description: str,
        incident_date: str,
        severity: str = 'medium',
        status: str = 'open',
        assigned_to: Optional[str] = None,
        reported_by: Optional[str] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None
    ):
        """
        Initialize Incident model.
        
        Args:
            title: Incident title
            description: Detailed description
            incident_date: Date when incident occurred
            severity: Severity level (low, medium, high, critical)
            status: Current status (open, investigating, resolved, closed)
            assigned_to: Username of assigned analyst
            reported_by: Username of reporter
            id: Unique identifier
            created_at: Creation timestamp
        """
        super().__init__(id, created_at)
        self._title = title
        self._description = description
        self._incident_date = incident_date
        self._severity = severity
        self._status = status
        self._assigned_to = assigned_to
        self._reported_by = reported_by
        
        # Validate on initialization
        is_valid, error = self.validate()
        if not is_valid:
            raise ValueError(f"Invalid incident data: {error}")
    
    # Encapsulation: Getters and Setters
    @property
    def title(self) -> str:
        """Get the incident title."""
        return self._title
    
    @title.setter
    def title(self, value: str):
        """Set the incident title with validation."""
        if not value or len(value.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(value) < 5:
            raise ValueError("Title must be at least 5 characters long")
        self._title = value.strip()
    
    @property
    def description(self) -> str:
        """Get the incident description."""
        return self._description
    
    @description.setter
    def description(self, value: str):
        """Set the incident description."""
        if not value or len(value.strip()) == 0:
            raise ValueError("Description cannot be empty")
        self._description = value.strip()
    
    @property
    def incident_date(self) -> str:
        """Get the incident date."""
        return self._incident_date
    
    @incident_date.setter
    def incident_date(self, value: str):
        """Set the incident date with validation."""
        try:
            datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        self._incident_date = value
    
    @property
    def severity(self) -> str:
        """Get the incident severity."""
        return self._severity
    
    @severity.setter
    def severity(self, value: str):
        """Set the incident severity with validation."""
        if value not in self.VALID_SEVERITIES:
            raise ValueError(f"Severity must be one of: {', '.join(self.VALID_SEVERITIES)}")
        self._severity = value
    
    @property
    def status(self) -> str:
        """Get the incident status."""
        return self._status
    
    @status.setter
    def status(self, value: str):
        """Set the incident status with validation."""
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(self.VALID_STATUSES)}")
        self._status = value
    
    @property
    def assigned_to(self) -> Optional[str]:
        """Get the assigned analyst."""
        return self._assigned_to
    
    @assigned_to.setter
    def assigned_to(self, value: Optional[str]):
        """Set the assigned analyst."""
        self._assigned_to = value
    
    @property
    def reported_by(self) -> Optional[str]:
        """Get the reporter."""
        return self._reported_by
    
    @reported_by.setter
    def reported_by(self, value: Optional[str]):
        """Set the reporter."""
        self._reported_by = value
    
    # Business Logic Methods
    def is_critical(self) -> bool:
        """Check if incident is critical severity."""
        return self._severity == 'critical'
    
    def is_high_priority(self) -> bool:
        """Check if incident is high or critical severity."""
        return self._severity in ['high', 'critical']
    
    def is_open(self) -> bool:
        """Check if incident is still open."""
        return self._status in ['open', 'investigating']
    
    def is_resolved(self) -> bool:
        """Check if incident is resolved or closed."""
        return self._status in ['resolved', 'closed']
    
    def can_transition_to(self, new_status: str) -> bool:
        """
        Check if status transition is valid.
        
        Args:
            new_status: Target status
            
        Returns:
            True if transition is valid, False otherwise
        """
        # Define valid transitions
        valid_transitions = {
            'open': ['investigating', 'closed'],
            'investigating': ['resolved', 'open', 'closed'],
            'resolved': ['closed', 'open'],
            'closed': ['open']
        }
        
        return new_status in valid_transitions.get(self._status, [])
    
    def assign_to_analyst(self, analyst_username: str):
        """
        Assign incident to an analyst.
        
        Args:
            analyst_username: Username of the analyst
        """
        self._assigned_to = analyst_username
        if self._status == 'open':
            self._status = 'investigating'
    
    def escalate(self):
        """Escalate incident severity to next level."""
        severity_order = ['low', 'medium', 'high', 'critical']
        current_index = severity_order.index(self._severity)
        if current_index < len(severity_order) - 1:
            self._severity = severity_order[current_index + 1]
    
    def resolve(self):
        """Mark incident as resolved."""
        if self._status in ['open', 'investigating']:
            self._status = 'resolved'
    
    def close(self):
        """Close the incident."""
        self._status = 'closed'
    
    def reopen(self):
        """Reopen a closed incident."""
        if self._status == 'closed':
            self._status = 'open'
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert incident to dictionary.
        
        Returns:
            Dictionary representation of the incident
        """
        data = super().to_dict()
        data.update({
            'title': self._title,
            'description': self._description,
            'incident_date': self._incident_date,
            'severity': self._severity,
            'status': self._status,
            'assigned_to': self._assigned_to,
            'reported_by': self._reported_by
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Incident':
        """
        Create Incident instance from dictionary.
        
        Args:
            data: Dictionary containing incident data
            
        Returns:
            Incident instance
        """
        return cls(
            title=data['title'],
            description=data['description'],
            incident_date=data['incident_date'],
            severity=data.get('severity', 'medium'),
            status=data.get('status', 'open'),
            assigned_to=data.get('assigned_to'),
            reported_by=data.get('reported_by'),
            id=data.get('id'),
            created_at=data.get('created_at')
        )
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Incident':
        """
        Create Incident instance from database row.
        
        Args:
            row: Database row tuple
            
        Returns:
            Incident instance
        """
        return cls(
            id=row[0],
            title=row[1],
            description=row[2],
            incident_date=row[3],
            severity=row[4],
            status=row[5],
            assigned_to=row[6] if len(row) > 6 else None,
            reported_by=row[7] if len(row) > 7 else None,
            created_at=row[8] if len(row) > 8 else None
        )
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate incident data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Call parent validation
        is_valid, error = super().validate()
        if not is_valid:
            return False, error
        
        # Title validation
        if not self._title or len(self._title.strip()) == 0:
            return False, "Title cannot be empty"
        if len(self._title) < 5:
            return False, "Title must be at least 5 characters long"
        
        # Description validation
        if not self._description or len(self._description.strip()) == 0:
            return False, "Description cannot be empty"
        
        # Date validation
        try:
            datetime.fromisoformat(self._incident_date)
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"
        
        # Severity validation
        if self._severity not in self.VALID_SEVERITIES:
            return False, f"Severity must be one of: {', '.join(self.VALID_SEVERITIES)}"
        
        # Status validation
        if self._status not in self.VALID_STATUSES:
            return False, f"Status must be one of: {', '.join(self.VALID_STATUSES)}"
        
        return True, ""
    
    def __repr__(self) -> str:
        """String representation of the incident."""
        return f"Incident(id={self._id}, title='{self._title}', severity='{self._severity}', status='{self._status}')"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"[{self._severity.upper()}] {self._title} - {self._status}"
