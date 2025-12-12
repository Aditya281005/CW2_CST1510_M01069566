"""
Repositories package for OOP implementation.
Contains data access layer classes.
"""
from .base_repository import BaseRepository
from .user_repository import UserRepository
from .incident_repository import IncidentRepository
from .dataset_repository import DatasetRepository
from .ticket_repository import TicketRepository

__all__ = [
    'BaseRepository',
    'UserRepository',
    'IncidentRepository',
    'DatasetRepository',
    'TicketRepository'
]
