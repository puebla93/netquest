"""Module to add all dependencies
"""

from .user import get_user
from .database import get_db
from .record import get_record
from .auth import get_current_user, user_is_authenticated


__all__ = [
    "get_db",
    "get_user",
    "get_record",
    "get_current_user",
    "user_is_authenticated",
]
