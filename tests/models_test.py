"""Module to add all tests for models.
"""

from jose import jwt

from sqlalchemy.orm import scoped_session

from . import db_session, user

from app.models import Record, User
from app.config import settings


class TestRecordModel:
    def test_record_properties(self):
        record = Record(title="Test Record", img="http://test.record.image.com")
        assert record.title == "Test Record"
        assert record.img == "http://test.record.image.com"
        assert record.id is None

    def test_record_properties_in_db(self, db_session: scoped_session):
        record = Record(title="Test Record", img="http://test.record.image.com")

        db_session.add(record)
        db_session.commit()
        db_session.refresh(record)

        assert record.title == "Test Record"
        assert record.img == "http://test.record.image.com"
        assert record.id is not None


class TestUserModel:
    def test_record_properties(self):
        user = User(email="test@example.com", hashed_password="password")

        assert user.email == "test@example.com"
        assert user.hashed_password == "password"
        assert user.id is None

    def test_record_jwt_property(self, user: User):
        user_jwt = user.jwt
        payload = jwt.decode(
            user_jwt, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        assert user_jwt is not None
        assert isinstance(user_jwt, str)
        assert "user_id" in payload
        assert "exp" in payload
        assert payload["user_id"] == user.id

    def test_record_properties_in_db(self, db_session: scoped_session):
        user = User(email="test@example.com", hashed_password="password")

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.email == "test@example.com"
        assert user.hashed_password == "password"
        assert user.id is not None
