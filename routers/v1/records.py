"""Module to add all records endpionts
"""


from fastapi import APIRouter


records_router = APIRouter(prefix="/records")


@records_router.get("")
def get_all_records() -> dict:
    return {}


@records_router.post("")
def create_record(record_id: int) -> dict:
    return {"record_id": record_id}


@records_router.get("/{record_id}")
def get_record(record_id: int) -> dict:
    return {"record_id": record_id}


@records_router.put("/{record_id}")
def update_record(record_id: int) -> dict:
    return {"record_id": record_id}


@records_router.patch("/{record_id}")
def partial_update_record(record_id: int) -> dict:
    return {"record_id": record_id}


@records_router.delete("/{record_id}")
def delete_record(record_id: int) -> dict:
    return {"record_id": record_id}
