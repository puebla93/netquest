"""Module to add record schemas
"""

from urllib.parse import urlparse

from pydantic import BaseModel, validator


class RecordBase(BaseModel):
    title: str
    img: str

    @validator("img")
    def validate_img(cls, value):
        parsed = urlparse(value)
        if not all([parsed.scheme, parsed.netloc]):
            raise ValueError("Invalid img value")
        return value


class RecordCreate(RecordBase):
    pass


class RecordUpdate(RecordBase):
    pass


class RecordPartialUpdate(RecordBase):
    title: str | None
    img: str | None


class Record(RecordBase):
    id: int

    class Config:
        orm_mode = True
