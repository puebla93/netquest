"""Module to add all dependencies
"""

from .database import get_db
from .record import get_record


__all__ = [
    "get_db",
    "get_record",
]
