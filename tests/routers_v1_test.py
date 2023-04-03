"""
"""

import json

from pytest_mock import MockerFixture

from fastapi import status
from fastapi.testclient import TestClient

from sqlalchemy.orm import scoped_session

from . import client, user, record, db_session

from app.models import User, Record


class TestRecordRouter:
    def test_record_unauthenticated(self, client: TestClient):
        response = client.get("/api/v1/records/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        content = json.loads(response.content)

        assert "detail" in content
        assert content["detail"] == "User is not authenticated"

    def test_record_list(
        self,
        client: TestClient,
        user: User,
        record: Record,
        db_session: scoped_session,
        mocker: MockerFixture,
    ):
        mock_session_local = mocker.patch(
            "app.middlewares.database_session.SessionLocal"
        )
        mock_session_local.return_value = db_session

        headers = {"Authorization": f"Bearer {user.jwt}"}
        response = client.get("/api/v1/records/", headers=headers)

        assert response.status_code == status.HTTP_200_OK

        content = json.loads(response.content)

        assert isinstance(content, list)
        assert len(content) == 1
        assert content[0]["title"] == record.title
        assert content[0]["img"] == record.img

    def test_record_create_invalid_img(
        self,
        client: TestClient,
        user: User,
        db_session: scoped_session,
        mocker: MockerFixture,
    ):
        mock_session_local = mocker.patch(
            "app.middlewares.database_session.SessionLocal"
        )
        mock_session_local.return_value = db_session

        data = {"title": "Fake Title", "img": "invalid url"}
        post_data = json.dumps(data)
        headers = {"Authorization": f"Bearer {user.jwt}"}
        response = client.post("/api/v1/records/", data=post_data, headers=headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_record_create(
        self,
        client: TestClient,
        user: User,
        db_session: scoped_session,
        mocker: MockerFixture,
    ):
        mock_session_local = mocker.patch(
            "app.middlewares.database_session.SessionLocal"
        )
        mock_session_local.return_value = db_session

        data = {"title": "Fake Title", "img": "http://fake.img.com"}
        post_data = json.dumps(data)
        headers = {"Authorization": f"Bearer {user.jwt}"}
        response = client.post("/api/v1/records/", data=post_data, headers=headers)

        assert response.status_code == status.HTTP_201_CREATED

        content = json.loads(response.content)

        assert content["title"] == "Fake Title"
        assert content["img"] == "http://fake.img.com"

        record = (
            db_session.query(Record)
            .filter(Record.title == "Fake Title")
            .filter(Record.img == "http://fake.img.com")
            .first()
        )

        assert record is not None

    def test_record_retrieve(
        self,
        client: TestClient,
        user: User,
        record: Record,
        db_session: scoped_session,
        mocker: MockerFixture,
    ):
        mock_session_local = mocker.patch(
            "app.middlewares.database_session.SessionLocal"
        )
        mock_session_local.return_value = db_session

        headers = {"Authorization": f"Bearer {user.jwt}"}
        response = client.get(f"/api/v1/records/{record.id}/", headers=headers)

        assert response.status_code == status.HTTP_200_OK

        content = json.loads(response.content)

        assert content["title"] == record.title
        assert content["img"] == record.img

    def test_record_update_invalid_img(
        self,
        client: TestClient,
        user: User,
        record: Record,
        db_session: scoped_session,
        mocker: MockerFixture,
    ):
        mock_session_local = mocker.patch(
            "app.middlewares.database_session.SessionLocal"
        )
        mock_session_local.return_value = db_session

        data = {"title": "Fake Title", "img": "invalid url"}
        post_data = json.dumps(data)
        headers = {"Authorization": f"Bearer {user.jwt}"}
        response = client.put(
            f"/api/v1/records/{record.id}", data=post_data, headers=headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_record_update(
        self,
        client: TestClient,
        user: User,
        record: Record,
        db_session: scoped_session,
        mocker: MockerFixture,
    ):
        mock_session_local = mocker.patch(
            "app.middlewares.database_session.SessionLocal"
        )
        mock_session_local.return_value = db_session

        data = {"title": "Fake Title", "img": "http://fake.img.com"}
        post_data = json.dumps(data)
        headers = {"Authorization": f"Bearer {user.jwt}"}
        response = client.put(
            f"/api/v1/records/{record.id}", data=post_data, headers=headers
        )

        assert response.status_code == status.HTTP_200_OK

        content = json.loads(response.content)

        assert content["title"] == "Fake Title"
        assert content["img"] == "http://fake.img.com"

    def test_record_partially_update(
        self,
        client: TestClient,
        user: User,
        record: Record,
        db_session: scoped_session,
        mocker: MockerFixture,
    ):
        mock_session_local = mocker.patch(
            "app.middlewares.database_session.SessionLocal"
        )
        mock_session_local.return_value = db_session

        data = {"title": "Fake Title", "img": "http://fake.img.com"}
        post_data = json.dumps(data)
        headers = {"Authorization": f"Bearer {user.jwt}"}
        response = client.patch(
            f"/api/v1/records/{record.id}", data=post_data, headers=headers
        )

        assert response.status_code == status.HTTP_200_OK

        content = json.loads(response.content)

        assert content["title"] == "Fake Title"
        assert content["img"] == "http://fake.img.com"

    def test_record_delete(
        self,
        client: TestClient,
        user: User,
        record: Record,
        db_session: scoped_session,
        mocker: MockerFixture,
    ):
        mock_session_local = mocker.patch(
            "app.middlewares.database_session.SessionLocal"
        )
        mock_session_local.return_value = db_session

        headers = {"Authorization": f"Bearer {user.jwt}"}
        response = client.delete(f"/api/v1/records/{record.id}", headers=headers)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        record = db_session.query(Record).filter(Record.id == record.id).first()

        assert record is None


class TestAuthRouter:
    def test_signin(
        self,
        client: TestClient,
        db_session: scoped_session,
        mocker: MockerFixture,
    ):
        mock_session_local = mocker.patch(
            "app.middlewares.database_session.SessionLocal"
        )
        mock_session_local.return_value = db_session

        data = {
            "email": "test@example.com",
            "password": "123456",
        }
        post_data = json.dumps(data)
        response = client.post("/api/v1/signin/", data=post_data)

        assert response.status_code == status.HTTP_201_CREATED

        content = json.loads(response.content)

        assert content["email"] == "test@example.com"
        assert isinstance(content["jwt"], str)

        user = db_session.query(User).filter(User.email == "test@example.com").first()

        assert user is not None

    def test_login_invalid_email(
        self,
        client: TestClient,
        db_session: scoped_session,
        mocker: MockerFixture,
    ):
        mock_session_local = mocker.patch(
            "app.middlewares.database_session.SessionLocal"
        )
        mock_session_local.return_value = db_session

        data = {
            "email": "invalid email",
            "password": "123456",
        }
        post_data = json.dumps(data)
        response = client.post("/api/v1/login/", data=post_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_login_user_not_found(
        self,
        client: TestClient,
        db_session: scoped_session,
        mocker: MockerFixture,
    ):
        mock_session_local = mocker.patch(
            "app.middlewares.database_session.SessionLocal"
        )
        mock_session_local.return_value = db_session

        data = {
            "email": "fake@email.com",
            "password": "123456",
        }
        post_data = json.dumps(data)
        response = client.post("/api/v1/login/", data=post_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        content = json.loads(response.content)

        assert content["detail"] == "Incorrect email or password"

    def test_login(
        self,
        client: TestClient,
        user: User,
        db_session: scoped_session,
        mocker: MockerFixture,
    ):
        mock_session_local = mocker.patch(
            "app.middlewares.database_session.SessionLocal"
        )
        mock_session_local.return_value = db_session

        data = {
            "email": user.email,
            "password": "123456",
        }
        post_data = json.dumps(data)
        response = client.post("/api/v1/login/", data=post_data)

        assert response.status_code == status.HTTP_200_OK

        content = json.loads(response.content)

        assert content["token_type"] == "bearer"
        assert isinstance(content["jwt"], str)
