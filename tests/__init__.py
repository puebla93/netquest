"""
"""

import pytest
from pytest_postgresql.factories import postgresql

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.pool import NullPool

from app.main import app
from app.models import User, Record
from app.database import Base


@pytest.fixture
def db_session(postgresql):
    """Create a clean database instance for testing."""

    connection = f"postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}"

    engine = create_engine(connection, echo=False, poolclass=NullPool)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

    Base.metadata.create_all(bind=engine)

    try:
        yield session
    finally:
        session.close()



@pytest.fixture(scope="module")
def client() -> TestClient:
    """Create a FastAPI test client."""

    return TestClient(app)


@pytest.fixture
def user(db_session: Session) -> User:
    user = User(id=1, email="test@example.com", hashed_password="password")

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def record(db_session: Session) -> User:
    record = Record(id=1, title="test title", img="http://test.record.image.com")

    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)

    return record
