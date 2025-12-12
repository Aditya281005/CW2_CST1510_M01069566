"""
Ticket Model Class - Demonstrates OOP Encapsulation and Priority Management
"""
from typing import Dict, Any, Optional
from datetime import datetime
from .base_model import BaseModel


class Ticket(BaseModel):
    """
    Ticket model representing an IT support ticket.
    
    OOP Principles Demonstrated:
    - Inheritance: Extends BaseModel
    - Encapsulation: Private attributes with validation
    - Business Logic: Priority management and SLA tracking
    """
    
    # Class variables
    VALID_PRIORITIES = ['low', 'medium', 'high', 'urgent']
    VALID_STATUSES = ['open', 'in_progress', 'pending', 'resolved', 'closed']
    VALID_CATEGORIES = ['hardware', 'software', 'network', 'security', 'access', 'other']
    
    def __init__(
        self,
        title: str,
        description: str,
        priority: str = 'medium',
        status: str = 'open',
        category: str = 'other',
        requester: Optional[str] = None,
        assigned_to: Optional[str] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None
    ):
        """
        Initialize Ticket model.
        
        Args:
            title: Ticket title
            description: Detailed description
            priority: Priority level (low, medium, high, urgent)
            status: Current status
            category: Ticket category
            requester: Username of requester
            assigned_to: Username of assigned technician
            id: Unique identifier
            created_at: Creation timestamp
        """
        super().__init__(id, created_at)
        self._title = title
        self._description = description
        self._priority = priority
        self._status = status
        self._category = category
        self._requester = requester
        self._assigned_to = assigned_to
        
        # Validate on initialization
        is_valid, error = self.validate()
        if not is_valid:
            raise ValueError(f"Invalid ticket data: {error}")
    
    # Encapsulation: Getters and Setters
    @property
    def title(self) -> str:
        """Get the ticket title."""
        return self._title
    
    @title.setter
    def title(self, value: str):
        """Set the ticket title with validation."""
        if not value or len(value.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(value) < 5:
            raise ValueError("Title must be at least 5 characters long")
        self._title = value.strip()
    
    @property
    def description(self) -> str:
        """Get the ticket description."""
        return self._description
    
    @description.setter
    def description(self, value: str):
        """Set the ticket description."""
        if not value or len(value.strip()) == 0:
            raise ValueError("Description cannot be empty")
        self._description = value.strip()
    
    @property
    def priority(self) -> str:
        """Get the ticket priority."""
        return self._priority
    
    @priority.setter
    def priority(self, value: str):
        """Set the ticket priority with validation."""
        if value not in self.VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of: {', '.join(self.VALID_PRIORITIES)}")
        self._priority = value
    
    @property
    def status(self) -> str:
        """Get the ticket status."""
        return self._status
    
    @status.setter
    def status(self, value: str):
        """Set the ticket status with validation."""
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(self.VALID_STATUSES)}")
        self._status = value
    
    @property
    def category(self) -> str:
        """Get the ticket category."""
        return self._category
    
    @category.setter
    def category(self, value: str):
        """Set the ticket category with validation."""
        if value not in self.VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(self.VALID_CATEGORIES)}")
        self._category = value
    
    @property
    def requester(self) -> Optional[str]:
        """Get the requester."""
        return self._requester
    
    @requester.setter
    def requester(self, value: Optional[str]):
        """Set the requester."""
        self._requester = value
    
    @property
    def assigned_to(self) -> Optional[str]:
        """Get the assigned technician."""
        return self._assigned_to
    
    @assigned_to.setter
    def assigned_to(self, value: Optional[str]):
        """Set the assigned technician."""
        self._assigned_to = value
    
    # Business Logic Methods
    def is_urgent(self) -> bool:
        """Check if ticket is urgent priority."""
        return self._priority == 'urgent'
    
    def is_high_priority(self) -> bool:
        """Check if ticket is high or urgent priority."""
        return self._priority in ['high', 'urgent']
    
    def is_open(self) -> bool:
        """Check if ticket is still open."""
        return self._status in ['open', 'in_progress', 'pending']
    
    def is_resolved(self) -> bool:
        """Check if ticket is resolved or closed."""
        return self._status in ['resolved', 'closed']
    
    def is_assigned(self) -> bool:
        """Check if ticket is assigned to someone."""
        return self._assigned_to is not None
    
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
            'open': ['in_progress', 'closed'],
            'in_progress': ['pending', 'resolved', 'open'],
            'pending': ['in_progress', 'resolved', 'closed'],
            'resolved': ['closed', 'open'],
            'closed': ['open']
        }
        
        return new_status in valid_transitions.get(self._status, [])
    
    def assign_to_technician(self, technician_username: str):
        """
        Assign ticket to a technician.
        
        Args:
            technician_username: Username of the technician
        """
        self._assigned_to = technician_username
        if self._status == 'open':
            self._status = 'in_progress'
    
    def escalate(self):
        """Escalate ticket priority to next level."""
        priority_order = ['low', 'medium', 'high', 'urgent']
        current_index = priority_order.index(self._priority)
        if current_index < len(priority_order) - 1:
            self._priority = priority_order[current_index + 1]
    
    def resolve(self):
        """Mark ticket as resolved."""
        if self._status in ['open', 'in_progress', 'pending']:
            self._status = 'resolved'
    
    def close(self):
        """Close the ticket."""
        self._status = 'closed'
    
    def reopen(self):
        """Reopen a closed ticket."""
        if self._status == 'closed':
            self._status = 'open'
    
    def put_on_hold(self):
        """Put ticket on hold (pending status)."""
        if self._status == 'in_progress':
            self._status = 'pending'
    
    def get_sla_hours(self) -> int:
        """
        Get SLA response time in hours based on priority.
        
        Returns:
            SLA hours
        """
        sla_mapping = {
            'urgent': 2,
            'high': 8,
            'medium': 24,
            'low': 72
        }
        return sla_mapping.get(self._priority, 24)
    
    def is_sla_breached(self) -> bool:
        """
        Check if SLA has been breached.
        
        Returns:
            True if SLA breached, False otherwise
        """
        if not self._created_at:
            return False
        
        try:
            created = datetime.fromisoformat(self._created_at)
            now = datetime.now()
            hours_elapsed = (now - created).total_seconds() / 3600
            sla_hours = self.get_sla_hours()
            
            return hours_elapsed > sla_hours and self.is_open()
        except ValueError:
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert ticket to dictionary.
        
        Returns:
            Dictionary representation of the ticket
        """
        data = super().to_dict()
        data.update({
            'title': self._title,
            'description': self._description,
            'priority': self._priority,
            'status': self._status,
            'category': self._category,
            'requester': self._requester,
            'assigned_to': self._assigned_to
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Ticket':
        """
        Create Ticket instance from dictionary.
        
        Args:
            data: Dictionary containing ticket data
            
        Returns:
            Ticket instance
        """
        return cls(
            title=data['title'],
            description=data['description'],
            priority=data.get('priority', 'medium'),
            status=data.get('status', 'open'),
            category=data.get('category', 'other'),
            requester=data.get('requester'),
            assigned_to=data.get('assigned_to'),
            id=data.get('id'),
            created_at=data.get('created_at')
        )
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Ticket':
        """
        Create Ticket instance from database row.
        
        Args:
            row: Database row tuple
            
        Returns:
            Ticket instance
        """
        return cls(
            id=row[0],
            title=row[1],
            description=row[2],
            priority=row[3] if len(row) > 3 else 'medium',
            status=row[4] if len(row) > 4 else 'open',
            category=row[5] if len(row) > 5 else 'other',
            requester=row[6] if len(row) > 6 else None,
            assigned_to=row[7] if len(row) > 7 else None,
            created_at=row[8] if len(row) > 8 else None
        )
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate ticket data.
        
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
        
        # Priority validation
        if self._priority not in self.VALID_PRIORITIES:
            return False, f"Priority must be one of: {', '.join(self.VALID_PRIORITIES)}"
        
        # Status validation
        if self._status not in self.VALID_STATUSES:
            return False, f"Status must be one of: {', '.join(self.VALID_STATUSES)}"
        
        # Category validation
        if self._category not in self.VALID_CATEGORIES:
            return False, f"Category must be one of: {', '.join(self.VALID_CATEGORIES)}"
        
        return True, ""
    
    def __repr__(self) -> str:
        """String representation of the ticket."""
        return f"Ticket(id={self._id}, title='{self._title}', priority='{self._priority}', status='{self._status}')"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"[{self._priority.upper()}] {self._title} - {self._status}"
