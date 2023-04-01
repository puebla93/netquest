"""Module to add all records handlers
"""

import logging

from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.orm import Session

import models
import schemas
from dependencies import get_db, get_record


records_router = APIRouter(prefix="/records")


@records_router.get(
    "/", response_model=list[schemas.Record], status_code=status.HTTP_200_OK
)
def get_all_records(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[schemas.Record]:
    """Gets all records from db.

    Args:
        skip (int, optional): The offset where we want to start searching in the db. Defaults to 0.
        limit (int, optional): The number of records we want to retrieve from the db. Defaults to 100.
        db (Session, optional): The db session.
    Returns:
        list[schemas.Record]: A list with all records that we get from db.
    """

    logging.debug("Getting records from database (skip %d, limit %d" % (skip, limit))
    records = db.query(models.Record).offset(skip).limit(limit).all()

    return records


@records_router.post(
    "/", response_model=schemas.Record, status_code=status.HTTP_201_CREATED
)
def create_record(
    record: schemas.RecordCreate, db: Session = Depends(get_db)
) -> schemas.Record:
    """Creates a record in db.

    Args:
        record (schemas.RecordCreate): The data needed to create a record.
        db (Session, optional): The db session.
    Returns:
        schemas.Record: The new record entry in db.
    """

    db_record = models.Record(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    logging.debug("Created record with id %d" % db_record.id)

    return db_record


@records_router.get(
    "/{record_id}/", response_model=schemas.Record, status_code=status.HTTP_200_OK
)
def retrieve_record(db_record: models.Record = Depends(get_record)) -> schemas.Record:
    """Get a record entry from db.

    Args:
        db_record (models.Record, optional): The db record if exists otherwise None.

    Raises:
        HTTPException: Record not found.

    Returns:
        schemas.Record: The record entry in db.
    """

    if db_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
        )

    return db_record


@records_router.put(
    "/{record_id}/", response_model=schemas.Record, status_code=status.HTTP_200_OK
)
def update_record(
    record: schemas.RecordUpdate,
    db_record: models.Record = Depends(get_record),
    db: Session = Depends(get_db),
) -> schemas.Record:
    """Update a record entry in db.

    Args:
        record (schemas.RecordUpdate): The data to update the record.
        db_record (models.Record, optional): The db record if exists otherwise None.
        db (Session, optional): The db session.

    Raises:
        HTTPException: Record not found.

    Returns:
        schemas.Record: The updated record.
    """

    if db_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
        )

    for field, value in record.dict():
        setattr(db_record, field, value)

    # Commit the changes to the database session
    db.commit()

    logging.debug("Updated record with id %d" % db_record.id)

    return db_record


@records_router.patch(
    "/{record_id}/", response_model=schemas.Record, status_code=status.HTTP_200_OK
)
def partial_update_record(
    record: schemas.RecordUpdate,
    db_record: models.Record = Depends(get_record),
    db: Session = Depends(get_db),
) -> schemas.Record:
    """Partially update a record entry in db.

    Args:
        record (schemas.RecordUpdate): The data to update the record.
        db_record (models.Record, optional): The db record if exists otherwise None.
        db (Session, optional): The db session.

    Raises:
        HTTPException: Record not found.

    Returns:
        schemas.Record: The updated record.
    """

    if db_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
        )

    # Update the record fields with the values provided in the request body
    for field, value in record.dict(exclude_unset=True).items():
        setattr(db_record, field, value)

    # Commit the changes to the database session
    db.commit()

    logging.debug("Partially updated record with id %d" % db_record.id)

    return db_record


@records_router.delete("/{record_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(
    db_record: models.Record = Depends(get_record), db: Session = Depends(get_db)
) -> None:
    """Delete a record from db.

    Args:
        db_record (models.Record, optional): The db record if exists otherwise None.
        db (Session, optional): The db session.

    Raises:
        HTTPException: Record not found.
    """

    if db_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
        )

    db.delete(db_record)
    db.commit()

    logging.debug("Deleted record with id %d" % db_record.id)
