"""
Base Model Class - Demonstrates OOP Encapsulation and Abstraction
"""
from datetime import datetime
from typing import Dict, Any, Optional


class BaseModel:
    """
    Base model class that all other models inherit from.
    
    OOP Principles Demonstrated:
    - Encapsulation: Private attributes with getters/setters
    - Abstraction: Common functionality for all models
    - Inheritance: Base class for all data models
    """
    
    def __init__(self, id: Optional[int] = None, created_at: Optional[str] = None):
        """
        Initialize base model.
        
        Args:
            id: Unique identifier
            created_at: Creation timestamp
        """
        self._id = id
        self._created_at = created_at or datetime.now().isoformat()
    
    # Encapsulation: Getters and Setters
    @property
    def id(self) -> Optional[int]:
        """Get the model ID."""
        return self._id
    
    @id.setter
    def id(self, value: int):
        """Set the model ID."""
        if value is not None and value < 0:
            raise ValueError("ID must be a positive integer")
        self._id = value
    
    @property
    def created_at(self) -> str:
        """Get the creation timestamp."""
        return self._created_at
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary.
        
        Returns:
            Dictionary representation of the model
        """
        return {
            'id': self._id,
            'created_at': self._created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """
        Create model instance from dictionary.
        
        Args:
            data: Dictionary containing model data
            
        Returns:
            Model instance
        """
        return cls(
            id=data.get('id'),
            created_at=data.get('created_at')
        )
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate model data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if self._id is not None and self._id < 0:
            return False, "ID must be a positive integer"
        return True, ""
    
    def __repr__(self) -> str:
        """String representation of the model."""
        return f"{self.__class__.__name__}(id={self._id})"
    
    def __eq__(self, other) -> bool:
        """Check equality based on ID."""
        if not isinstance(other, BaseModel):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        """Hash based on ID."""
        return hash(self._id)
