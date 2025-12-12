"""
Database Manager Class - Demonstrates Singleton Pattern and Connection Management
"""
import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager


class DatabaseManager:
    """
    Database Manager using Singleton pattern.
    
    OOP Principles Demonstrated:
    - Singleton Pattern: Only one instance exists
    - Encapsulation: Private connection management
    - Context Manager: Automatic resource cleanup
    """
    
    _instance: Optional['DatabaseManager'] = None
    _db_path: Path = Path("DATA") / "intelligence_platform.db"
    
    def __new__(cls):
        """
        Implement Singleton pattern.
        Only one instance of DatabaseManager can exist.
        """
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the database manager."""
        if self._initialized:
            return
        
        self._connection: Optional[sqlite3.Connection] = None
        self._initialized = True
    
    @classmethod
    def set_database_path(cls, path: Path):
        """
        Set the database path.
        
        Args:
            path: Path to the database file
        """
        cls._db_path = path
    
    @classmethod
    def get_database_path(cls) -> Path:
        """
        Get the database path.
        
        Returns:
            Path to the database file
        """
        return cls._db_path
    
    def connect(self) -> sqlite3.Connection:
        """
        Get or create a database connection.
        
        Returns:
            SQLite connection object
        """
        if self._connection is None:
            self._connection = sqlite3.connect(str(self._db_path))
            self._connection.row_factory = sqlite3.Row  # Enable column access by name
        return self._connection
    
    def disconnect(self):
        """Close the database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        Automatically handles connection cleanup.
        
        Usage:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")
        
        Yields:
            SQLite connection object
        """
        conn = sqlite3.connect(str(self._db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    @contextmanager
    def transaction(self):
        """
        Context manager for database transactions.
        Automatically commits on success or rolls back on error.
        
        Usage:
            with db_manager.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users ...")
                # Automatically commits if no exception
        
        Yields:
            SQLite connection object
        """
        conn = sqlite3.connect(str(self._db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> list:
        """
        Execute a SELECT query and return results.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of rows
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        with self.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.rowcount
    
    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """
        Execute an INSERT query and return the last inserted ID.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Last inserted row ID
        """
        with self.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.lastrowid
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.
        
        Args:
            table_name: Name of the table
            
        Returns:
            True if table exists, False otherwise
        """
        query = """
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """
        result = self.execute_query(query, (table_name,))
        return len(result) > 0
    
    def get_table_info(self, table_name: str) -> list:
        """
        Get information about table columns.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of column information
        """
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query)
    
    def get_row_count(self, table_name: str) -> int:
        """
        Get the number of rows in a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Number of rows
        """
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        result = self.execute_query(query)
        return result[0]['count'] if result else 0
    
    def backup_database(self, backup_path: Path):
        """
        Create a backup of the database.
        
        Args:
            backup_path: Path for the backup file
        """
        import shutil
        shutil.copy2(self._db_path, backup_path)
    
    def __repr__(self) -> str:
        """String representation of the database manager."""
        return f"DatabaseManager(db_path='{self._db_path}')"
    
    def __enter__(self):
        """Context manager entry."""
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


# Convenience function for backward compatibility
def connect_database(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """
    Connect to the database using DatabaseManager.
    
    Args:
        db_path: Optional path to database file
        
    Returns:
        SQLite connection object
    """
    db_manager = DatabaseManager()
    if db_path:
        DatabaseManager.set_database_path(db_path)
    return db_manager.connect()
