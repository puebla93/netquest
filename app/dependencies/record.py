"""Module to add record dependencies
"""

import logging
from typing import Annotated

from fastapi import Depends

from sqlalchemy.orm import Session

from app.models import Record

from .database import get_db


def get_record(
    record_id: int, db: Annotated[Session, Depends(get_db)]
) -> Record | None:
    """Get record from database

    Args:
        record_id (int): The record's id
        db (Session): The databse session.

    Returns:
        Record | None: The record if exists otherwise None.
    """

    logging.debug("Getting record with id %d from database" % record_id)
    record = db.query(Record).get(record_id)

    return record
