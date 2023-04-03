"""Module to add user model
"""

from datetime import datetime, timedelta
from jose import jwt

from sqlalchemy import Column, Integer, String

from app.database import Base
from app.config import settings


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    @property
    def jwt(self) -> str:
        to_encode = {
            "user_id": self.id,
            "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        access_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return access_token
