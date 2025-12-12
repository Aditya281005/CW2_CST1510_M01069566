"""
Dataset Model Class - Demonstrates OOP Encapsulation and Data Classification
"""
from typing import Dict, Any, Optional
from .base_model import BaseModel


class Dataset(BaseModel):
    """
    Dataset model representing a data collection.
    
    OOP Principles Demonstrated:
    - Inheritance: Extends BaseModel
    - Encapsulation: Private attributes with validation
    - Business Logic: Classification and access control
    """
    
    # Class variables
    VALID_CLASSIFICATIONS = ['public', 'internal', 'confidential', 'restricted']
    VALID_FORMATS = ['csv', 'json', 'xml', 'parquet', 'sql', 'other']
    
    def __init__(
        self,
        name: str,
        description: str,
        source: str,
        classification: str = 'internal',
        format: str = 'csv',
        size_mb: Optional[float] = None,
        owner: Optional[str] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None
    ):
        """
        Initialize Dataset model.
        
        Args:
            name: Dataset name
            description: Dataset description
            source: Data source
            classification: Security classification level
            format: Data format (csv, json, etc.)
            size_mb: Size in megabytes
            owner: Dataset owner username
            id: Unique identifier
            created_at: Creation timestamp
        """
        super().__init__(id, created_at)
        self._name = name
        self._description = description
        self._source = source
        self._classification = classification
        self._format = format
        self._size_mb = size_mb
        self._owner = owner
        
        # Validate on initialization
        is_valid, error = self.validate()
        if not is_valid:
            raise ValueError(f"Invalid dataset data: {error}")
    
    # Encapsulation: Getters and Setters
    @property
    def name(self) -> str:
        """Get the dataset name."""
        return self._name
    
    @name.setter
    def name(self, value: str):
        """Set the dataset name with validation."""
        if not value or len(value.strip()) == 0:
            raise ValueError("Name cannot be empty")
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long")
        self._name = value.strip()
    
    @property
    def description(self) -> str:
        """Get the dataset description."""
        return self._description
    
    @description.setter
    def description(self, value: str):
        """Set the dataset description."""
        if not value or len(value.strip()) == 0:
            raise ValueError("Description cannot be empty")
        self._description = value.strip()
    
    @property
    def source(self) -> str:
        """Get the data source."""
        return self._source
    
    @source.setter
    def source(self, value: str):
        """Set the data source."""
        if not value or len(value.strip()) == 0:
            raise ValueError("Source cannot be empty")
        self._source = value.strip()
    
    @property
    def classification(self) -> str:
        """Get the classification level."""
        return self._classification
    
    @classification.setter
    def classification(self, value: str):
        """Set the classification level with validation."""
        if value not in self.VALID_CLASSIFICATIONS:
            raise ValueError(f"Classification must be one of: {', '.join(self.VALID_CLASSIFICATIONS)}")
        self._classification = value
    
    @property
    def format(self) -> str:
        """Get the data format."""
        return self._format
    
    @format.setter
    def format(self, value: str):
        """Set the data format with validation."""
        if value not in self.VALID_FORMATS:
            raise ValueError(f"Format must be one of: {', '.join(self.VALID_FORMATS)}")
        self._format = value
    
    @property
    def size_mb(self) -> Optional[float]:
        """Get the dataset size in MB."""
        return self._size_mb
    
    @size_mb.setter
    def size_mb(self, value: Optional[float]):
        """Set the dataset size with validation."""
        if value is not None and value < 0:
            raise ValueError("Size must be a positive number")
        self._size_mb = value
    
    @property
    def owner(self) -> Optional[str]:
        """Get the dataset owner."""
        return self._owner
    
    @owner.setter
    def owner(self, value: Optional[str]):
        """Set the dataset owner."""
        self._owner = value
    
    # Business Logic Methods
    def is_public(self) -> bool:
        """Check if dataset is publicly accessible."""
        return self._classification == 'public'
    
    def is_restricted(self) -> bool:
        """Check if dataset has restricted access."""
        return self._classification in ['confidential', 'restricted']
    
    def requires_approval(self) -> bool:
        """Check if dataset access requires approval."""
        return self._classification in ['restricted']
    
    def can_access(self, user_role: str) -> bool:
        """
        Check if user role can access this dataset.
        
        Args:
            user_role: User's role (user, analyst, admin)
            
        Returns:
            True if user can access, False otherwise
        """
        access_matrix = {
            'public': ['user', 'analyst', 'admin'],
            'internal': ['analyst', 'admin'],
            'confidential': ['admin'],
            'restricted': ['admin']
        }
        
        allowed_roles = access_matrix.get(self._classification, [])
        return user_role in allowed_roles
    
    def upgrade_classification(self):
        """Upgrade classification to next security level."""
        classification_order = ['public', 'internal', 'confidential', 'restricted']
        current_index = classification_order.index(self._classification)
        if current_index < len(classification_order) - 1:
            self._classification = classification_order[current_index + 1]
    
    def downgrade_classification(self):
        """Downgrade classification to previous security level."""
        classification_order = ['public', 'internal', 'confidential', 'restricted']
        current_index = classification_order.index(self._classification)
        if current_index > 0:
            self._classification = classification_order[current_index - 1]
    
    def get_size_category(self) -> str:
        """
        Get size category of the dataset.
        
        Returns:
            Size category (small, medium, large, very large)
        """
        if self._size_mb is None:
            return 'unknown'
        elif self._size_mb < 10:
            return 'small'
        elif self._size_mb < 100:
            return 'medium'
        elif self._size_mb < 1000:
            return 'large'
        else:
            return 'very large'
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert dataset to dictionary.
        
        Returns:
            Dictionary representation of the dataset
        """
        data = super().to_dict()
        data.update({
            'name': self._name,
            'description': self._description,
            'source': self._source,
            'classification': self._classification,
            'format': self._format,
            'size_mb': self._size_mb,
            'owner': self._owner
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Dataset':
        """
        Create Dataset instance from dictionary.
        
        Args:
            data: Dictionary containing dataset data
            
        Returns:
            Dataset instance
        """
        return cls(
            name=data['name'],
            description=data['description'],
            source=data['source'],
            classification=data.get('classification', 'internal'),
            format=data.get('format', 'csv'),
            size_mb=data.get('size_mb'),
            owner=data.get('owner'),
            id=data.get('id'),
            created_at=data.get('created_at')
        )
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Dataset':
        """
        Create Dataset instance from database row.
        
        Args:
            row: Database row tuple
            
        Returns:
            Dataset instance
        """
        return cls(
            id=row[0],
            name=row[1],
            description=row[2],
            source=row[3],
            classification=row[4] if len(row) > 4 else 'internal',
            format=row[5] if len(row) > 5 else 'csv',
            size_mb=row[6] if len(row) > 6 else None,
            owner=row[7] if len(row) > 7 else None,
            created_at=row[8] if len(row) > 8 else None
        )
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate dataset data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Call parent validation
        is_valid, error = super().validate()
        if not is_valid:
            return False, error
        
        # Name validation
        if not self._name or len(self._name.strip()) == 0:
            return False, "Name cannot be empty"
        if len(self._name) < 3:
            return False, "Name must be at least 3 characters long"
        
        # Description validation
        if not self._description or len(self._description.strip()) == 0:
            return False, "Description cannot be empty"
        
        # Source validation
        if not self._source or len(self._source.strip()) == 0:
            return False, "Source cannot be empty"
        
        # Classification validation
        if self._classification not in self.VALID_CLASSIFICATIONS:
            return False, f"Classification must be one of: {', '.join(self.VALID_CLASSIFICATIONS)}"
        
        # Format validation
        if self._format not in self.VALID_FORMATS:
            return False, f"Format must be one of: {', '.join(self.VALID_FORMATS)}"
        
        # Size validation
        if self._size_mb is not None and self._size_mb < 0:
            return False, "Size must be a positive number"
        
        return True, ""
    
    def __repr__(self) -> str:
        """String representation of the dataset."""
        return f"Dataset(id={self._id}, name='{self._name}', classification='{self._classification}')"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        size_str = f"{self._size_mb}MB" if self._size_mb else "unknown size"
        return f"{self._name} ({self._classification}) - {size_str}"
