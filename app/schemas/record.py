from pydantic import BaseModel


class RecordBase(BaseModel):
    title: str
    img: str | None = None


class RecordCreate(RecordBase):
    pass


class Record(RecordBase):
    class Config:
        orm_mode = True
