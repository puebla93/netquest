"""Module to add all tests for middlewares.
"""

import pytest
from pytest_mock import MockerFixture

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from sqlalchemy.orm import scoped_session, Session

from . import user, db_session

from app.models import User
from app.database import SessionLocal
from app.middlewares import AuthMiddleware, DatabaseSessionMiddleware


@pytest.fixture
def app() -> FastAPI:
    _app = FastAPI(title="Middleware Test App")

    @_app.get("/")
    async def handler(request: Request):
        return {"test": "test"}

    return _app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def auth_middleware(app: FastAPI):
    app.add_middleware(AuthMiddleware)


@pytest.fixture
def database_session_middleware(app: FastAPI):
    app.add_middleware(DatabaseSessionMiddleware)


@pytest.fixture
def all_middlewares(app):
    app.add_middleware(AuthMiddleware)
    app.add_middleware(DatabaseSessionMiddleware)


class TestAuthMiddleware:
    def test_auth_middleware_unauthenticated_user(
        self, app: FastAPI, client: TestClient, auth_middleware
    ):
        @app.get("/anonymous")
        async def user(request: Request):
            assert request.state.user is None
            return {"test": "test"}

        response = client.get("/anonymous")
        assert response.status_code == 200

    def test_auth_middleware_invalid_auth_header(
        self, client: TestClient, auth_middleware
    ):
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/", headers=headers)
        assert response.status_code == 401

    def test_auth_middleware_valid_jwt(
        self,
        mocker: MockerFixture,
        app: FastAPI,
        client: TestClient,
        user: User,
        db_session: scoped_session,
        all_middlewares,
    ):
        mock_session_local = mocker.patch(
            "app.middlewares.database_session.SessionLocal"
        )
        mock_session_local.return_value = db_session

        @app.get("/me")
        async def get_me(request: Request):
            assert isinstance(request.state.user, User)
            return {"test": "test"}

        headers = {"Authorization": f"Bearer {user.jwt}"}
        response = client.get("/me", headers=headers)
        assert response.status_code == 200


class TestDatabaseSessionMiddleware:
    def test_data_base_session_middleware(
        self, app: FastAPI, client: TestClient, database_session_middleware
    ):
        @app.get("/db")
        async def db(request: Request):
            assert isinstance(request.state.db, Session)
            return {"test": "test"}

        response = client.get("/db")
        assert response.status_code == 200
