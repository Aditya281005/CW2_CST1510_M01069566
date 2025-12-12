"""
Logger Class - Demonstrates OOP Singleton Pattern and Logging
"""
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime


class Logger:
    """
    Logger class using Singleton pattern.
    
    OOP Principles Demonstrated:
    - Singleton Pattern: Only one logger instance
    - Encapsulation: Hides logging complexity
    - Flexibility: Multiple log levels and outputs
    """
    
    _instance: Optional['Logger'] = None
    _initialized: bool = False
    
    # Log levels
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    
    def __new__(cls):
        """
        Implement Singleton pattern.
        Only one instance of Logger can exist.
        """
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, name: str = "IntelligencePlatform", log_dir: str = "logs"):
        """
        Initialize the logger.
        
        Args:
            name: Logger name
            log_dir: Directory for log files
        """
        if self._initialized:
            return
        
        self._name = name
        self._log_dir = Path(log_dir)
        self._log_dir.mkdir(exist_ok=True)
        
        # Create logger
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if not self._logger.handlers:
            self._setup_handlers()
        
        self._initialized = True
    
    def _setup_handlers(self):
        """Set up log handlers for console and file output."""
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        self._logger.addHandler(console_handler)
        
        # File handler (all logs)
        log_file = self._log_dir / f"{self._name.lower()}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        self._logger.addHandler(file_handler)
        
        # Error file handler (errors only)
        error_file = self._log_dir / f"{self._name.lower()}_errors.log"
        error_handler = logging.FileHandler(error_file)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_format)
        self._logger.addHandler(error_handler)
    
    def debug(self, message: str, **kwargs):
        """
        Log a debug message.
        
        Args:
            message: Log message
            **kwargs: Additional context
        """
        self._logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs):
        """
        Log an info message.
        
        Args:
            message: Log message
            **kwargs: Additional context
        """
        self._logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """
        Log a warning message.
        
        Args:
            message: Log message
            **kwargs: Additional context
        """
        self._logger.warning(message, extra=kwargs)
    
    def error(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """
        Log an error message.
        
        Args:
            message: Log message
            exception: Optional exception object
            **kwargs: Additional context
        """
        if exception:
            self._logger.error(f"{message}: {str(exception)}", exc_info=True, extra=kwargs)
        else:
            self._logger.error(message, extra=kwargs)
    
    def critical(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """
        Log a critical message.
        
        Args:
            message: Log message
            exception: Optional exception object
            **kwargs: Additional context
        """
        if exception:
            self._logger.critical(f"{message}: {str(exception)}", exc_info=True, extra=kwargs)
        else:
            self._logger.critical(message, extra=kwargs)
    
    def log_user_action(self, username: str, action: str, details: str = ""):
        """
        Log a user action.
        
        Args:
            username: Username performing the action
            action: Action performed
            details: Additional details
        """
        message = f"User '{username}' performed action: {action}"
        if details:
            message += f" - {details}"
        self.info(message)
    
    def log_database_operation(self, operation: str, table: str, success: bool, details: str = ""):
        """
        Log a database operation.
        
        Args:
            operation: Type of operation (INSERT, UPDATE, DELETE, SELECT)
            table: Table name
            success: Whether operation succeeded
            details: Additional details
        """
        status = "SUCCESS" if success else "FAILED"
        message = f"Database {operation} on '{table}': {status}"
        if details:
            message += f" - {details}"
        
        if success:
            self.info(message)
        else:
            self.error(message)
    
    def log_api_request(self, method: str, endpoint: str, status_code: int, duration_ms: float = 0):
        """
        Log an API request.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            status_code: Response status code
            duration_ms: Request duration in milliseconds
        """
        message = f"API {method} {endpoint} - Status: {status_code}"
        if duration_ms > 0:
            message += f" - Duration: {duration_ms:.2f}ms"
        
        if status_code < 400:
            self.info(message)
        elif status_code < 500:
            self.warning(message)
        else:
            self.error(message)
    
    def log_security_event(self, event_type: str, username: str, details: str, severity: str = "INFO"):
        """
        Log a security event.
        
        Args:
            event_type: Type of security event
            username: Username involved
            details: Event details
            severity: Severity level (INFO, WARNING, ERROR, CRITICAL)
        """
        message = f"SECURITY [{event_type}] User: {username} - {details}"
        
        severity_map = {
            "INFO": self.info,
            "WARNING": self.warning,
            "ERROR": self.error,
            "CRITICAL": self.critical
        }
        
        log_func = severity_map.get(severity.upper(), self.info)
        log_func(message)
    
    def set_level(self, level: int):
        """
        Set the logging level.
        
        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self._logger.setLevel(level)
    
    def get_log_file_path(self) -> Path:
        """
        Get the path to the main log file.
        
        Returns:
            Path to log file
        """
        return self._log_dir / f"{self._name.lower()}.log"
    
    def get_error_log_file_path(self) -> Path:
        """
        Get the path to the error log file.
        
        Returns:
            Path to error log file
        """
        return self._log_dir / f"{self._name.lower()}_errors.log"
    
    def clear_logs(self):
        """Clear all log files."""
        for log_file in self._log_dir.glob("*.log"):
            log_file.write_text("")
    
    @classmethod
    def get_instance(cls) -> 'Logger':
        """
        Get the singleton logger instance.
        
        Returns:
            Logger instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __repr__(self) -> str:
        """String representation of the logger."""
        return f"Logger(name='{self._name}', log_dir='{self._log_dir}')"


# Convenience function for getting logger instance
def get_logger() -> Logger:
    """
    Get the singleton logger instance.
    
    Returns:
        Logger instance
    """
    return Logger.get_instance()
