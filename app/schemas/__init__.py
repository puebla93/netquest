"""Module to add all schemas
"""

from .user import User, UserAuth, Token
from .record import Record, RecordCreate, RecordUpdate, RecordPartialUpdate

__all__ = [
    "User",
    "UserAuth",
    "Token",
    "Record",
    "RecordCreate",
    "RecordUpdate",
    "RecordPartialUpdate",
]
