"""Module to add all records handlers
"""

import logging
from typing import Annotated

from passlib.context import CryptContext

from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.orm import Session

from app import models
from app import schemas
from app.dependencies import get_db, get_user


auth_router = APIRouter()


@auth_router.post(
    "/signin/", response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
def signin(
    user: schemas.UserAuth, db: Annotated[Session, Depends(get_db)]
) -> schemas.User:
    """Signin a user.

    Args:
        user (schemas.UserAuth): The data needed to create a user.
        db (Session): The db session.

    Returns:
        schemas.Record: The new user.
    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user_data = {
        "email": user.email,
        "hashed_password": pwd_context.hash(user.password),
    }

    db_user = models.User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    logging.debug("Created user with id %d" % db_user.id)

    return db_user


@auth_router.post(
    "/login/", response_model=schemas.Token, status_code=status.HTTP_200_OK
)
def login(
    user: schemas.UserAuth,
    db_user: Annotated[models.User, Depends(get_user)],
) -> schemas.Token:
    """User login.

    Args:
        user schemas.UserAuth: The user data.

    Raises:
        HTTPException: Incorrect email or password .

    Returns:
        schemas.Token: The access token.
    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"jwt": db_user.jwt, "token_type": "bearer"}
