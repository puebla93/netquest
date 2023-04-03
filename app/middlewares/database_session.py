"""Module that defines the database session middleware class
"""

import logging

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.database import SessionLocal


class DatabaseSessionMiddleware(BaseHTTPMiddleware):
    """Database session middleware"""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = Response("Internal server error", status_code=500)
        try:
            logging.debug("Adding database connection SessionLocal to request state")
            request.state.db = SessionLocal()
            response = await call_next(request)
        finally:
            request.state.db.close()
        return response
