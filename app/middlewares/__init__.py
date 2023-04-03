"""Module to add all middlewares
"""

from .auth import AuthMiddleware
from .database_session import DatabaseSessionMiddleware


__all__ = [
    "AuthMiddleware",
    "DatabaseSessionMiddleware",
]
