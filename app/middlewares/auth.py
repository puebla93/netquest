"""Module that defines the auth middleware class
"""

import logging

from jose import jwt, JWTError

from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

import models

from config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    """Validates the JWT and sets user on the request.
    """

    def handle_token(
        self, request: Request, token: str
    ) -> models.User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get("user_id")
        except JWTError:
            logging.exception("INVALID_JWT_TOKEN: Could not verify token")
            raise credentials_exception

        if user_id is None:
            logging.error(f"Invalid user id: {user_id}")
            raise credentials_exception

        logging.debug("Getting user with id %d from database" % user_id)
        user = request.state.db.query(models.User).get(user_id)

        if not user:
            logging.error(f"INVALID_JWT_TOKEN: User with id {user_id} not found")
            raise credentials_exception

        return user

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        token: str = None
        user: models.User = None

        if auth_header := request.headers.get("Authorization"):
            try:
                # Get token from the header
                token = auth_header.split(" ")[1]
            except IndexError:
                logging.error(f"Invalid Authorization header: {auth_header}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        if token:
            user = self.handle_token(request=request, token=token)

        request.state.user = user

        return await call_next(request)
