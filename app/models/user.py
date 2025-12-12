"""
User Model Class - Demonstrates OOP Encapsulation and Data Validation
"""
from typing import Dict, Any, Optional
from .base_model import BaseModel


class User(BaseModel):
    """
    User model representing a system user.
    
    OOP Principles Demonstrated:
    - Inheritance: Extends BaseModel
    - Encapsulation: Private attributes with validation
    - Data Validation: Property setters with validation logic
    """
    
    # Class variable (shared across all instances)
    VALID_ROLES = ['user', 'analyst', 'admin']
    
    def __init__(
        self,
        username: str,
        password_hash: str,
        role: str = 'user',
        id: Optional[int] = None,
        created_at: Optional[str] = None
    ):
        """
        Initialize User model.
        
        Args:
            username: User's username
            password_hash: Hashed password
            role: User's role (user, analyst, admin)
            id: Unique identifier
            created_at: Creation timestamp
        """
        super().__init__(id, created_at)
        self._username = username
        self._password_hash = password_hash
        self._role = role
        
        # Validate on initialization
        is_valid, error = self.validate()
        if not is_valid:
            raise ValueError(f"Invalid user data: {error}")
    
    # Encapsulation: Getters and Setters with Validation
    @property
    def username(self) -> str:
        """Get the username."""
        return self._username
    
    @username.setter
    def username(self, value: str):
        """Set the username with validation."""
        if not value or len(value.strip()) == 0:
            raise ValueError("Username cannot be empty")
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters long")
        self._username = value.strip()
    
    @property
    def password_hash(self) -> str:
        """Get the password hash."""
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, value: str):
        """Set the password hash."""
        if not value:
            raise ValueError("Password hash cannot be empty")
        self._password_hash = value
    
    @property
    def role(self) -> str:
        """Get the user role."""
        return self._role
    
    @role.setter
    def role(self, value: str):
        """Set the user role with validation."""
        if value not in self.VALID_ROLES:
            raise ValueError(f"Role must be one of: {', '.join(self.VALID_ROLES)}")
        self._role = value
    
    def is_admin(self) -> bool:
        """Check if user is an admin."""
        return self._role == 'admin'
    
    def is_analyst(self) -> bool:
        """Check if user is an analyst."""
        return self._role == 'analyst'
    
    def has_permission(self, required_role: str) -> bool:
        """
        Check if user has required permission level.
        
        Args:
            required_role: Required role level
            
        Returns:
            True if user has permission, False otherwise
        """
        role_hierarchy = {'user': 0, 'analyst': 1, 'admin': 2}
        user_level = role_hierarchy.get(self._role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        return user_level >= required_level
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert user to dictionary.
        
        Returns:
            Dictionary representation of the user
        """
        data = super().to_dict()
        data.update({
            'username': self._username,
            'password_hash': self._password_hash,
            'role': self._role
        })
        return data
    
    def to_safe_dict(self) -> Dict[str, Any]:
        """
        Convert user to dictionary without sensitive data.
        
        Returns:
            Safe dictionary representation (no password hash)
        """
        return {
            'id': self._id,
            'username': self._username,
            'role': self._role,
            'created_at': self._created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """
        Create User instance from dictionary.
        
        Args:
            data: Dictionary containing user data
            
        Returns:
            User instance
        """
        return cls(
            username=data['username'],
            password_hash=data['password_hash'],
            role=data.get('role', 'user'),
            id=data.get('id'),
            created_at=data.get('created_at')
        )
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'User':
        """
        Create User instance from database row.
        
        Args:
            row: Database row tuple (id, username, password_hash, role, created_at)
            
        Returns:
            User instance
        """
        return cls(
            id=row[0],
            username=row[1],
            password_hash=row[2],
            role=row[3],
            created_at=row[4] if len(row) > 4 else None
        )
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate user data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Call parent validation
        is_valid, error = super().validate()
        if not is_valid:
            return False, error
        
        # Username validation
        if not self._username or len(self._username.strip()) == 0:
            return False, "Username cannot be empty"
        if len(self._username) < 3:
            return False, "Username must be at least 3 characters long"
        
        # Password hash validation
        if not self._password_hash:
            return False, "Password hash cannot be empty"
        
        # Role validation
        if self._role not in self.VALID_ROLES:
            return False, f"Role must be one of: {', '.join(self.VALID_ROLES)}"
        
        return True, ""
    
    def __repr__(self) -> str:
        """String representation of the user."""
        return f"User(id={self._id}, username='{self._username}', role='{self._role}')"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self._username} ({self._role})"
