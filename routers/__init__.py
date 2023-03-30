"""Module to add all api routers
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from routers.v1 import v1_router


api_router = APIRouter(prefix="/api", default_response_class=JSONResponse)


api_router.include_router(v1_router)
