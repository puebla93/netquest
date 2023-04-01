"""Module to add all middlewares
"""

from .database_session import DatabaseSessionMiddleware


__all__ = [
    "DatabaseSessionMiddleware",
]
