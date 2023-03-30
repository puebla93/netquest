"""Module to add all records handlers
"""


from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


records_router = APIRouter(prefix="/records")


@records_router.get("")
def get_all_records() -> JSONResponse:
    response = [
        {
            "id": 1,
        },
    ]
    return JSONResponse(
        content=response,
        status_code=status.HTTP_200_OK,
    )


@records_router.post("")
def create_record() -> JSONResponse:
    response = {
        "id": 1,
    }
    return JSONResponse(
        content=response,
        status_code=status.HTTP_201_CREATED,
    )


@records_router.get("/{record_id}")
def get_record(record_id: int) -> JSONResponse:
    response = {
        "id": record_id,
    }
    return JSONResponse(
        content=response,
        status_code=status.HTTP_200_OK,
    )


@records_router.put("/{record_id}")
def update_record(record_id: int) -> JSONResponse:
    response = {
        "id": record_id,
    }
    return JSONResponse(
        content=response,
        status_code=status.HTTP_200_OK,
    )


@records_router.patch("/{record_id}")
def partial_update_record(record_id: int) -> JSONResponse:
    response = {
        "id": record_id,
    }
    return JSONResponse(
        content=response,
        status_code=status.HTTP_200_OK,
    )


@records_router.delete("/{record_id}")
def delete_record(record_id: int) -> JSONResponse:
    return JSONResponse(
        content={},
        status_code=status.HTTP_204_NO_CONTENT,
    )
