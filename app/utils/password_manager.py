"""
Password Manager Class - Demonstrates OOP Encapsulation for Security
"""
import bcrypt
from typing import Tuple


class PasswordManager:
    """
    Password Manager for hashing and verifying passwords.
    
    OOP Principles Demonstrated:
    - Encapsulation: Hides password hashing complexity
    - Static Methods: Utility functions for password operations
    - Security: Proper password handling
    """
    
    # Class variable for default rounds
    DEFAULT_ROUNDS = 12
    
    @staticmethod
    def hash_password(plain_password: str, rounds: int = DEFAULT_ROUNDS) -> str:
        """
        Hash a plain text password using bcrypt.
        
        Args:
            plain_password: Plain text password
            rounds: Number of bcrypt rounds (default: 12)
            
        Returns:
            Hashed password string
        """
        if not plain_password:
            raise ValueError("Password cannot be empty")
        
        # Convert password to bytes
        password_bytes = plain_password.encode('utf-8')
        
        # Generate salt and hash
        salt = bcrypt.gensalt(rounds=rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # Return as string
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain text password against a hashed password.
        
        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password to compare against
            
        Returns:
            True if password matches, False otherwise
        """
        if not plain_password or not hashed_password:
            return False
        
        try:
            # Convert to bytes
            password_bytes = plain_password.encode('utf-8')
            hashed_bytes = hashed_password.encode('utf-8')
            
            # Verify password
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception:
            return False
    
    @staticmethod
    def needs_rehash(hashed_password: str, rounds: int = DEFAULT_ROUNDS) -> bool:
        """
        Check if a hashed password needs to be rehashed with more rounds.
        
        Args:
            hashed_password: Hashed password to check
            rounds: Desired number of rounds
            
        Returns:
            True if password needs rehashing, False otherwise
        """
        try:
            hashed_bytes = hashed_password.encode('utf-8')
            # Extract the cost factor from the hash
            cost = int(hashed_bytes.split(b'$')[2])
            return cost < rounds
        except Exception:
            return True
    
    @classmethod
    def hash_and_verify(cls, plain_password: str) -> Tuple[str, bool]:
        """
        Hash a password and immediately verify it (for testing).
        
        Args:
            plain_password: Plain text password
            
        Returns:
            Tuple of (hashed_password, verification_result)
        """
        hashed = cls.hash_password(plain_password)
        verified = cls.verify_password(plain_password, hashed)
        return hashed, verified
    
    @staticmethod
    def generate_temporary_password(length: int = 12) -> str:
        """
        Generate a temporary random password.
        
        Args:
            length: Length of the password (default: 12)
            
        Returns:
            Random password string
        """
        import secrets
        import string
        
        # Define character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*"
        
        # Ensure at least one of each type
        password = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits),
            secrets.choice(special)
        ]
        
        # Fill the rest randomly
        all_chars = lowercase + uppercase + digits + special
        password.extend(secrets.choice(all_chars) for _ in range(length - 4))
        
        # Shuffle the password
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    @staticmethod
    def calculate_password_strength(password: str) -> Tuple[int, str]:
        """
        Calculate password strength score.
        
        Args:
            password: Password to evaluate
            
        Returns:
            Tuple of (strength_score, strength_label)
            Score: 0-100
            Label: 'weak', 'fair', 'good', 'strong', 'very strong'
        """
        if not password:
            return 0, "weak"
        
        score = 0
        
        # Length score (max 30 points)
        length = len(password)
        if length >= 8:
            score += min(30, length * 2)
        
        # Character variety (max 40 points)
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        variety_score = sum([has_lower, has_upper, has_digit, has_special]) * 10
        score += variety_score
        
        # Complexity bonus (max 30 points)
        unique_chars = len(set(password))
        complexity_score = min(30, unique_chars * 2)
        score += complexity_score
        
        # Determine label
        if score < 30:
            label = "weak"
        elif score < 50:
            label = "fair"
        elif score < 70:
            label = "good"
        elif score < 90:
            label = "strong"
        else:
            label = "very strong"
        
        return score, label
    
    @staticmethod
    def mask_password(password: str, visible_chars: int = 0) -> str:
        """
        Mask a password for display purposes.
        
        Args:
            password: Password to mask
            visible_chars: Number of characters to show at the end
            
        Returns:
            Masked password string
        """
        if not password:
            return ""
        
        if visible_chars <= 0:
            return "*" * len(password)
        
        if visible_chars >= len(password):
            return password
        
        masked_length = len(password) - visible_chars
        return "*" * masked_length + password[-visible_chars:]
