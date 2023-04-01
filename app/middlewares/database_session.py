"""Module that defines the database session middleware class
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from database import SessionLocal


class DatabaseSessionMiddleware(BaseHTTPMiddleware):
    """Database session middleware
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = Response("Internal server error", status_code=500)
        try:
            request.state.db = SessionLocal()
            response = await call_next(request)
        finally:
            request.state.db.close()
        return response
