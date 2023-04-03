"""Module to add auth dependencies
"""

from typing import Annotated

from fastapi import Request, HTTPException, status, Depends

from app import models


def get_current_user(request: Request) -> models.User | None:
    """Dependency that returns the user stored in request.state.

    See AuthMiddleware for details of what is stored in request.state.

    Args:
        request (Request): The request.

    Returns:
        models.User | None: If the user making the request is authenticated
        it returns a User, otherwise, it returns None.
    """

    return request.state.user


def user_is_authenticated(
    user: Annotated[models.User, Depends(get_current_user)],
) -> bool:
    """Dependency to validate that the user making the request is authenticated.

    Args:
        user models.User: The current user.

    Raises:
        HTTPException: 401 error if the user is not authenticated.

    Returns:
        bool: True if the user is authenticated.
    """

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")

    return True
