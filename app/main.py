"""Main module
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middlewares import AuthMiddleware, DatabaseSessionMiddleware

from app.config import settings
from app.routers import api_router
from app.database import Base, engine


app = FastAPI(title=settings.PROJECT_NAME)


# Middlewares are executed in LIFO order,
# RequestData needs to be initialized before everything else.
app.add_middleware(AuthMiddleware)
app.add_middleware(DatabaseSessionMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)


@app.on_event("startup")
def startup_event():
    # Create all tables defined in the database models
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
