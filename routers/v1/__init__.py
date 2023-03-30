"""Module to add all api v1 routers
"""

from fastapi import APIRouter

from .records import records_router


v1_router = APIRouter(prefix="/v1")


v1_router.include_router(records_router)
