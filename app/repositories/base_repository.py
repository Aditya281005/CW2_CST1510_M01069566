"""
Base Repository Class - Demonstrates OOP Repository Pattern and CRUD Operations
"""
from typing import List, Optional, Dict, Any, Type, TypeVar
from abc import ABC, abstractmethod
from app.core.database_manager import DatabaseManager
from app.models.base_model import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseRepository(ABC):
    """
    Base repository class with common CRUD operations.
    
    OOP Principles Demonstrated:
    - Abstraction: Abstract base class with common interface
    - Inheritance: Subclasses implement specific table operations
    - Encapsulation: Hides database complexity
    - Repository Pattern: Separates data access from business logic
    """
    
    def __init__(self, table_name: str, model_class: Type[T]):
        """
        Initialize the repository.
        
        Args:
            table_name: Name of the database table
            model_class: Model class for this repository
        """
        self._table_name = table_name
        self._model_class = model_class
        self._db_manager = DatabaseManager()
    
    @property
    def table_name(self) -> str:
        """Get the table name."""
        return self._table_name
    
    @property
    def model_class(self) -> Type[T]:
        """Get the model class."""
        return self._model_class
    
    def find_by_id(self, id: int) -> Optional[T]:
        """
        Find a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            Model instance or None if not found
        """
        query = f"SELECT * FROM {self._table_name} WHERE id = ?"
        rows = self._db_manager.execute_query(query, (id,))
        
        if rows:
            return self._row_to_model(rows[0])
        return None
    
    def find_all(self, limit: Optional[int] = None, offset: int = 0) -> List[T]:
        """
        Find all records.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of model instances
        """
        query = f"SELECT * FROM {self._table_name}"
        
        if limit:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        rows = self._db_manager.execute_query(query)
        return [self._row_to_model(row) for row in rows]
    
    def find_by_field(self, field: str, value: Any) -> List[T]:
        """
        Find records by a specific field value.
        
        Args:
            field: Field name
            value: Field value
            
        Returns:
            List of model instances
        """
        query = f"SELECT * FROM {self._table_name} WHERE {field} = ?"
        rows = self._db_manager.execute_query(query, (value,))
        return [self._row_to_model(row) for row in rows]
    
    def find_one_by_field(self, field: str, value: Any) -> Optional[T]:
        """
        Find one record by a specific field value.
        
        Args:
            field: Field name
            value: Field value
            
        Returns:
            Model instance or None if not found
        """
        results = self.find_by_field(field, value)
        return results[0] if results else None
    
    def create(self, model: T) -> int:
        """
        Create a new record.
        
        Args:
            model: Model instance to create
            
        Returns:
            ID of the created record
        """
        # Validate model
        is_valid, error = model.validate()
        if not is_valid:
            raise ValueError(f"Invalid model data: {error}")
        
        # Get model data
        data = model.to_dict()
        data.pop('id', None)  # Remove ID as it's auto-generated
        
        # Build INSERT query
        fields = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {self._table_name} ({fields}) VALUES ({placeholders})"
        
        # Execute query
        record_id = self._db_manager.execute_insert(query, tuple(data.values()))
        model.id = record_id
        
        return record_id
    
    def update(self, model: T) -> bool:
        """
        Update an existing record.
        
        Args:
            model: Model instance to update
            
        Returns:
            True if updated successfully, False otherwise
        """
        if not model.id:
            raise ValueError("Cannot update model without ID")
        
        # Validate model
        is_valid, error = model.validate()
        if not is_valid:
            raise ValueError(f"Invalid model data: {error}")
        
        # Get model data
        data = model.to_dict()
        record_id = data.pop('id')
        
        # Build UPDATE query
        set_clause = ', '.join([f"{field} = ?" for field in data.keys()])
        query = f"UPDATE {self._table_name} SET {set_clause} WHERE id = ?"
        
        # Execute query
        values = list(data.values()) + [record_id]
        rows_affected = self._db_manager.execute_update(query, tuple(values))
        
        return rows_affected > 0
    
    def delete(self, id: int) -> bool:
        """
        Delete a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            True if deleted successfully, False otherwise
        """
        query = f"DELETE FROM {self._table_name} WHERE id = ?"
        rows_affected = self._db_manager.execute_update(query, (id,))
        return rows_affected > 0
    
    def delete_by_field(self, field: str, value: Any) -> int:
        """
        Delete records by a specific field value.
        
        Args:
            field: Field name
            value: Field value
            
        Returns:
            Number of records deleted
        """
        query = f"DELETE FROM {self._table_name} WHERE {field} = ?"
        return self._db_manager.execute_update(query, (value,))
    
    def count(self) -> int:
        """
        Count total records.
        
        Returns:
            Total number of records
        """
        return self._db_manager.get_row_count(self._table_name)
    
    def count_by_field(self, field: str, value: Any) -> int:
        """
        Count records by a specific field value.
        
        Args:
            field: Field name
            value: Field value
            
        Returns:
            Number of matching records
        """
        query = f"SELECT COUNT(*) as count FROM {self._table_name} WHERE {field} = ?"
        result = self._db_manager.execute_query(query, (value,))
        return result[0]['count'] if result else 0
    
    def exists(self, id: int) -> bool:
        """
        Check if a record exists by ID.
        
        Args:
            id: Record ID
            
        Returns:
            True if record exists, False otherwise
        """
        query = f"SELECT 1 FROM {self._table_name} WHERE id = ?"
        result = self._db_manager.execute_query(query, (id,))
        return len(result) > 0
    
    def exists_by_field(self, field: str, value: Any) -> bool:
        """
        Check if a record exists by field value.
        
        Args:
            field: Field name
            value: Field value
            
        Returns:
            True if record exists, False otherwise
        """
        query = f"SELECT 1 FROM {self._table_name} WHERE {field} = ?"
        result = self._db_manager.execute_query(query, (value,))
        return len(result) > 0
    
    @abstractmethod
    def _row_to_model(self, row) -> T:
        """
        Convert a database row to a model instance.
        Must be implemented by subclasses.
        
        Args:
            row: Database row
            
        Returns:
            Model instance
        """
        pass
    
    def execute_custom_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute a custom query and return results as dictionaries.
        
        Args:
            query: SQL query
            params: Query parameters
            
        Returns:
            List of result dictionaries
        """
        rows = self._db_manager.execute_query(query, params)
        return [dict(row) for row in rows]
    
    def __repr__(self) -> str:
        """String representation of the repository."""
        return f"{self.__class__.__name__}(table='{self._table_name}')"
