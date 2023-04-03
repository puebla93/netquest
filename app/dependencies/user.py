"""Module to add user dependencies
"""

import logging
from typing import Annotated

from fastapi import Depends

from sqlalchemy.orm import Session

import models
import schemas

from .database import get_db


def get_user(
    user: schemas.UserAuth,
    db: Annotated[Session, Depends(get_db)]
) -> models.User | None:
    """Get user from database.

    Args:
        user (schemas.UserAuth): The user data.
        db (Session): The databse session.

    Returns:
        models.User | None: The user if exists otherwise None.
    """

    logging.debug("Getting user with email %s from database" % user.email)
    user = db.query(models.User).filter(models.User == user.email).first()

    return user