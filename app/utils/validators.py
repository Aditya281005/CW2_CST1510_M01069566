"""
Validator Class - Demonstrates OOP Static Methods and Validation Logic
"""
import re
from typing import Tuple
from datetime import datetime


class Validator:
    """
    Validator class with static methods for data validation.
    
    OOP Principles Demonstrated:
    - Static Methods: Utility functions that don't need instance state
    - Single Responsibility: Each method validates one thing
    - Reusability: Can be used across the application
    """
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """
        Validate username format.
        
        Args:
            username: Username to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not username:
            return False, "Username cannot be empty"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if len(username) > 50:
            return False, "Username must be less than 50 characters"
        
        # Only alphanumeric and underscore allowed
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        return True, ""
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Validate password strength.
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not password:
            return False, "Password cannot be empty"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if len(password) > 128:
            return False, "Password must be less than 128 characters"
        
        # Check for uppercase letter
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        # Check for lowercase letter
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        # Check for digit
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        
        # Check for special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"
        
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Validate email format.
        
        Args:
            email: Email to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email:
            return False, "Email cannot be empty"
        
        # Basic email regex pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format"
        
        return True, ""
    
    @staticmethod
    def validate_date(date_str: str, format: str = "%Y-%m-%d") -> Tuple[bool, str]:
        """
        Validate date format.
        
        Args:
            date_str: Date string to validate
            format: Expected date format (default: YYYY-MM-DD)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not date_str:
            return False, "Date cannot be empty"
        
        try:
            datetime.strptime(date_str, format)
            return True, ""
        except ValueError:
            return False, f"Invalid date format. Expected: {format}"
    
    @staticmethod
    def validate_not_empty(value: str, field_name: str = "Field") -> Tuple[bool, str]:
        """
        Validate that a string is not empty.
        
        Args:
            value: Value to validate
            field_name: Name of the field for error message
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not value or len(value.strip()) == 0:
            return False, f"{field_name} cannot be empty"
        return True, ""
    
    @staticmethod
    def validate_min_length(value: str, min_length: int, field_name: str = "Field") -> Tuple[bool, str]:
        """
        Validate minimum string length.
        
        Args:
            value: Value to validate
            min_length: Minimum required length
            field_name: Name of the field for error message
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(value) < min_length:
            return False, f"{field_name} must be at least {min_length} characters long"
        return True, ""
    
    @staticmethod
    def validate_max_length(value: str, max_length: int, field_name: str = "Field") -> Tuple[bool, str]:
        """
        Validate maximum string length.
        
        Args:
            value: Value to validate
            max_length: Maximum allowed length
            field_name: Name of the field for error message
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(value) > max_length:
            return False, f"{field_name} must be less than {max_length} characters"
        return True, ""
    
    @staticmethod
    def validate_in_list(value: str, valid_values: list, field_name: str = "Field") -> Tuple[bool, str]:
        """
        Validate that value is in a list of valid values.
        
        Args:
            value: Value to validate
            valid_values: List of valid values
            field_name: Name of the field for error message
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if value not in valid_values:
            return False, f"{field_name} must be one of: {', '.join(valid_values)}"
        return True, ""
    
    @staticmethod
    def validate_positive_number(value: float, field_name: str = "Field") -> Tuple[bool, str]:
        """
        Validate that a number is positive.
        
        Args:
            value: Value to validate
            field_name: Name of the field for error message
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if value < 0:
            return False, f"{field_name} must be a positive number"
        return True, ""
    
    @staticmethod
    def validate_url(url: str) -> Tuple[bool, str]:
        """
        Validate URL format.
        
        Args:
            url: URL to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not url:
            return False, "URL cannot be empty"
        
        # Basic URL regex pattern
        pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
        if not re.match(pattern, url):
            return False, "Invalid URL format"
        
        return True, ""
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """
        Validate phone number format.
        
        Args:
            phone: Phone number to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not phone:
            return False, "Phone number cannot be empty"
        
        # Remove common separators
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        
        # Check if it's all digits and has reasonable length
        if not cleaned.isdigit() or len(cleaned) < 10 or len(cleaned) > 15:
            return False, "Invalid phone number format"
        
        return True, ""
    
    @classmethod
    def validate_all(cls, validations: list) -> Tuple[bool, str]:
        """
        Run multiple validations and return first error.
        
        Args:
            validations: List of (is_valid, error_message) tuples
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        for is_valid, error_message in validations:
            if not is_valid:
                return False, error_message
        return True, ""
