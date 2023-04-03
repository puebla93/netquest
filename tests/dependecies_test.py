"""Module to all tests to dependecies.
"""

import pytest
from pytest_mock import MockerFixture

from fastapi import Request, HTTPException

from sqlalchemy.orm import Session

from . import user, db_session, record

from app.models import User, Record
from app.schemas import UserAuth
from app.dependencies import get_current_user, user_is_authenticated, get_db, get_record, get_user


class TestAuthDependencies:
    def test_get_current_user(self, user: User):
        request = Request(scope={"type": "http"})

        request.state.user = user

        assert get_current_user(request=request) == user

    def test_user_is_authenticated(self, user: User):
        assert True == user_is_authenticated(user=user)

    def test_user_is_authenticated_raises_error_if_user_not_authenticated(self):
        with pytest.raises(HTTPException) as cm:
            user_is_authenticated(user=None)

        exc = cm.value
        assert exc.status_code == 401
        assert exc.detail == "User is not authenticated"


class TestDatabaseDependencies:
    def test_get_db(self, db_session: Session):
        request = Request(scope={"type": "http"})

        request.state.db = db_session

        assert get_db(request=request) == db_session


class TestRecordDependencies:
    def test_get_record(self, record: Record, db_session: Session):
        assert get_record(record_id=record.id, db=db_session) == record


class TestUserDependencies:
    def test_get_record(self, user: User, db_session: Session):
        user_auth = UserAuth(email=user.email, password="password")
        assert get_user(user=user_auth, db=db_session) == user
