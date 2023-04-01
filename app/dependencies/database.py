"""Module to add database dependencies
"""

from fastapi import Request
from sqlalchemy.orm import Session


def get_db(request: Request) -> Session:
    """Get database session from request state

    Args:
        request (Request): The request

    Returns:
        Session: The database session
    """

    return request.state.db
