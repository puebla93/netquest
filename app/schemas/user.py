"""Module to add user schemas
"""

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserAuth(UserBase):
    password: str


class User(UserBase):
    jwt: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
